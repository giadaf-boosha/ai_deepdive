from __future__ import annotations

import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path


class DeliveryBlocked(RuntimeError):
    """Raised when a delivery violates an explicit safety gate."""


@dataclass(frozen=True)
class SMTPConfig:
    host: str
    port: int
    username: str
    password: str
    sender: str
    recipient_allowlist: tuple[str, ...]


def build_message(sender: str, recipient: str, subject: str, html_body: str) -> EmailMessage:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content("Questo digest richiede un client email con supporto HTML.")
    message.add_alternative(html_body, subtype="html")
    return message


def deliver_email(
    config: SMTPConfig,
    *,
    recipient: str,
    subject: str,
    html_body: str,
    send: bool,
    outbox: Path,
) -> Path:
    if recipient not in config.recipient_allowlist:
        raise DeliveryBlocked(f"Destinatario non autorizzato: {recipient}")
    message = build_message(config.sender, recipient, subject, html_body)
    outbox.mkdir(mode=0o700, parents=True, exist_ok=True)
    draft_path = outbox / "email-preview.eml"
    draft_path.write_bytes(message.as_bytes())
    if not send:
        return draft_path
    if not config.username or not config.password:
        raise DeliveryBlocked("Credenziali SMTP mancanti")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config.host, config.port, context=context, timeout=30) as client:
        client.login(config.username, config.password)
        client.send_message(message)
    return draft_path
