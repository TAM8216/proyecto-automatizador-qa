from __future__ import annotations

import smtplib
from dataclasses import asdict, dataclass
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from backend.config import Settings, get_settings


@dataclass(frozen=True)
class DeliveryResult:
    status: str
    recipient: str
    subject: str
    sent_at: str | None = None
    failure_type: str | None = None
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def build_subject(suite_name: str, when: datetime | None = None) -> str:
    timestamp = (when or datetime.now().astimezone()).strftime("%d/%m/%Y %H:%M")
    return f"Reporte de automatización – {suite_name} – {timestamp}"


def _smtp_configuration_error(config: Settings) -> str | None:
    """Return an actionable error before smtplib attempts SMTP AUTH."""
    for field_name, value in (
        ("SMTP_USER", config.smtp_user),
        ("SMTP_PASSWORD", config.smtp_password),
    ):
        if value and not value.isascii():
            return (
                f"{field_name} contiene caracteres no compatibles con SMTP AUTH "
                "(por ejemplo, tildes o ñ). Usa credenciales ASCII; para correo real, "
                "configura una contraseña de aplicación."
            )
    if (
        config.smtp_host.strip().lower() in {"smtp.gmail.com", "smtp.googlemail.com"}
        and config.smtp_user
        and len(config.smtp_password_for_auth) != 16
    ):
        return (
            "Gmail requiere una contraseña de aplicación de 16 caracteres para SMTP. "
            "Activa la verificación en dos pasos, genera una contraseña de aplicación "
            "y colócala en SMTP_PASSWORD; no uses la contraseña normal de la cuenta."
        )
    return None


def send_reports(
    *,
    recipient: str,
    suite_name: str,
    docx_path: Path,
    html_path: Path,
    run_id: str,
    settings: Settings | None = None,
) -> DeliveryResult:
    config = settings or get_settings()
    subject = build_subject(suite_name)
    if not config.smtp_configured:
        return DeliveryResult(
            status="FALLIDA",
            recipient=recipient,
            subject=subject,
            failure_type="infraestructura",
            error="SMTP no configurado: se requieren SMTP_HOST y SMTP_FROM.",
        )
    if configuration_error := _smtp_configuration_error(config):
        return DeliveryResult(
            status="FALLIDA",
            recipient=recipient,
            subject=subject,
            failure_type="infraestructura",
            error=configuration_error,
        )
    missing = [str(path) for path in (docx_path, html_path) if not path.is_file()]
    if missing:
        return DeliveryResult(
            status="FALLIDA",
            recipient=recipient,
            subject=subject,
            failure_type="infraestructura",
            error="No se encontraron ambos reportes; el envío fue bloqueado.",
        )

    message = EmailMessage()
    message["From"] = config.smtp_from
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(
        "Adjuntamos los reportes de la corrida automatizada de IPAS.\n\n"
        f"Run ID: {run_id}\n"
        "Archivos: informe detallado DOCX y reporte HTML autocontenido.\n"
    )
    message.add_attachment(
        docx_path.read_bytes(),
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=docx_path.name,
    )
    message.add_attachment(
        html_path.read_bytes(),
        maintype="text",
        subtype="html",
        filename=html_path.name,
    )

    try:
        with smtplib.SMTP(
            config.smtp_host,
            config.smtp_port,
            timeout=config.smtp_timeout_seconds,
        ) as smtp:
            smtp.ehlo()
            if config.smtp_use_starttls:
                smtp.starttls()
                smtp.ehlo()
            if config.smtp_user:
                smtp.login(config.smtp_user, config.smtp_password_for_auth)
            smtp.send_message(message)
    except smtplib.SMTPAuthenticationError:
        return DeliveryResult(
            status="FALLIDA",
            recipient=recipient,
            subject=subject,
            failure_type="infraestructura",
            error="Autenticación SMTP rechazada. Verifica SMTP_USER y la contraseña de aplicación.",
        )
    except smtplib.SMTPServerDisconnected:
        return DeliveryResult(
            status="FALLIDA",
            recipient=recipient,
            subject=subject,
            failure_type="infraestructura",
            error=(
                "El servidor SMTP cerró la conexión durante la autenticación. "
                "Verifica el usuario, la contraseña de aplicación, STARTTLS y el puerto."
            ),
        )
    except (OSError, UnicodeError, smtplib.SMTPException) as exc:
        return DeliveryResult(
            status="FALLIDA",
            recipient=recipient,
            subject=subject,
            failure_type="infraestructura",
            error=f"{exc.__class__.__name__}: no fue posible entregar el correo.",
        )

    return DeliveryResult(
        status="ENVIADO",
        recipient=recipient,
        subject=subject,
        sent_at=datetime.now().astimezone().isoformat(timespec="seconds"),
    )
