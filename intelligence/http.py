from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Mapping, Protocol, Sequence, TypeAlias
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen


QueryValue: TypeAlias = str | int | Sequence[str]


@dataclass(frozen=True)
class HTTPResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes

    def json_object(self) -> dict[str, object]:
        try:
            value = json.loads(self.body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("La risposta HTTP non contiene JSON UTF-8 valido") from exc
        if not isinstance(value, dict):
            raise ValueError("La risposta HTTP JSON deve essere un oggetto")
        return value


class HTTPTransport(Protocol):
    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        query: Mapping[str, QueryValue] | None = None,
    ) -> HTTPResponse: ...


class HTTPStatusError(RuntimeError):
    def __init__(self, status: int, url: str, body: bytes = b"") -> None:
        self.status = status
        self.url = url
        self.body = body
        super().__init__(f"HTTP {status} da {url}")


def require_success(response: HTTPResponse, url: str) -> HTTPResponse:
    if not 200 <= response.status < 300:
        raise HTTPStatusError(response.status, url, response.body)
    return response


class UrllibHTTPTransport:
    """Small stdlib transport; inject a fake implementation in connector tests."""

    def __init__(self, *, timeout: float = 30.0) -> None:
        if timeout <= 0:
            raise ValueError("timeout deve essere positivo")
        self._timeout = timeout

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        query: Mapping[str, QueryValue] | None = None,
    ) -> HTTPResponse:
        parts = urlsplit(url)
        if parts.scheme != "https" or not parts.netloc:
            raise ValueError("Il transport accetta solo URL HTTPS assoluti")
        if parts.username or parts.password:
            raise ValueError("Le credenziali non possono essere inserite nell'URL")

        encoded_query = parts.query
        if query:
            addition = urlencode(query, doseq=True)
            encoded_query = f"{encoded_query}&{addition}" if encoded_query else addition
        target = urlunsplit(
            (parts.scheme, parts.netloc, parts.path, encoded_query, parts.fragment)
        )
        request = Request(target, headers=dict(headers or {}), method=method.upper())
        try:
            with urlopen(request, timeout=self._timeout) as response:  # nosec B310
                return HTTPResponse(
                    status=int(response.status),
                    headers={key.lower(): value for key, value in response.headers.items()},
                    body=response.read(),
                )
        except HTTPError as exc:
            return HTTPResponse(
                status=exc.code,
                headers={key.lower(): value for key, value in exc.headers.items()},
                body=exc.read(),
            )
