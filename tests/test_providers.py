import pytest

from intelligence.providers import Candidate, DeterministicProvider, StructuredHTTPProvider


CANDIDATE = Candidate("event-1", "Titolo", "Un fatto verificato", ("https://example.com",), "research")


def test_deterministic_provider_is_safe_offline_baseline() -> None:
    result = DeterministicProvider().analyze([CANDIDATE])
    assert result[0].event_id == "event-1"
    assert result[0].confidence == "low"


def test_structured_provider_validates_complete_response() -> None:
    def post_json(endpoint, headers, payload):
        return {
            "analyses": [
                {
                    "event_id": "event-1",
                    "tldr": "Sintesi",
                    "why_it_matters": "Motivo",
                    "lane": "research",
                    "confidence": "high",
                    "read_decision": "read_full",
                    "read_minutes": 15,
                    "bridge": None,
                }
            ]
        }

    provider = StructuredHTTPProvider(
        name="test", endpoint="https://gateway.example/analyze", bearer_token="secret", post_json=post_json
    )
    assert provider.analyze([CANDIDATE])[0].read_minutes == 15


def test_structured_provider_rejects_incomplete_response() -> None:
    provider = StructuredHTTPProvider(
        name="test",
        endpoint="https://gateway.example/analyze",
        bearer_token="secret",
        post_json=lambda *_: {"analyses": []},
    )
    with pytest.raises(ValueError):
        provider.analyze([CANDIDATE])
