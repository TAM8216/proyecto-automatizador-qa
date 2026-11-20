from __future__ import annotations

import smtplib

from backend.config import Settings
from backend.mailer.service import send_reports


class FakeSMTP:
    sent = []

    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def ehlo(self):
        return 250, b"ok"

    def starttls(self):
        return 220, b"ready"

    def login(self, user, password):
        return 235, b"ok"

    def send_message(self, message):
        self.sent.append(message)


def smtp_settings(**overrides) -> Settings:
    values = {
        "smtp_host": "127.0.0.1",
        "smtp_port": 1025,
        "smtp_from": "qa@example.com",
        "smtp_use_starttls": False,
    }
    values.update(overrides)
    return Settings(**values)


def test_envio_adjunta_docx_y_html(monkeypatch, tmp_path) -> None:
    FakeSMTP.sent.clear()
    monkeypatch.setattr(smtplib, "SMTP", FakeSMTP)
    docx = tmp_path / "informe_detallado.docx"
    html = tmp_path / "reporte_autocontenido.html"
    docx.write_bytes(b"PK-docx")
    html.write_text("<html>ok</html>", encoding="utf-8")

    result = send_reports(
        recipient="destino@example.com",
        suite_name="Smoke",
        docx_path=docx,
        html_path=html,
        run_id="run-123",
        settings=smtp_settings(),
    )

    assert result.status == "ENVIADO"
    assert len(FakeSMTP.sent) == 1
    attachments = list(FakeSMTP.sent[0].iter_attachments())
    assert [item.get_filename() for item in attachments] == [docx.name, html.name]


def test_smtp_no_configurado_no_elimina_reportes(tmp_path) -> None:
    docx = tmp_path / "informe_detallado.docx"
    html = tmp_path / "reporte_autocontenido.html"
    docx.write_bytes(b"docx")
    html.write_text("html", encoding="utf-8")

    result = send_reports(
        recipient="destino@example.com",
        suite_name="Smoke",
        docx_path=docx,
        html_path=html,
        run_id="run-123",
        settings=smtp_settings(smtp_host="", smtp_from=""),
    )

    assert result.status == "FALLIDA"
    assert result.failure_type == "infraestructura"
    assert docx.exists() and html.exists()


def test_credencial_smtp_no_ascii_falla_con_mensaje_claro(tmp_path) -> None:
    docx = tmp_path / "informe_detallado.docx"
    html = tmp_path / "reporte_autocontenido.html"
    docx.write_bytes(b"docx")
    html.write_text("html", encoding="utf-8")

    result = send_reports(
        recipient="destino@example.com",
        suite_name="Smoke",
        docx_path=docx,
        html_path=html,
        run_id="run-123",
        settings=smtp_settings(smtp_user="qa@example.com", smtp_password="contraseña"),
    )

    assert result.status == "FALLIDA"
    assert "SMTP_PASSWORD" in result.error
    assert "contraseña de aplicación" in result.error


def test_gmail_requiere_contrasena_de_aplicacion_de_16_caracteres(tmp_path) -> None:
    docx = tmp_path / "informe_detallado.docx"
    html = tmp_path / "reporte_autocontenido.html"
    docx.write_bytes(b"docx")
    html.write_text("html", encoding="utf-8")

    result = send_reports(
        recipient="destino@gmail.com",
        suite_name="Smoke",
        docx_path=docx,
        html_path=html,
        run_id="run-123",
        settings=smtp_settings(
            smtp_host="smtp.gmail.com",
            smtp_user="qa@gmail.com",
            smtp_password="clave-corta",
        ),
    )

    assert result.status == "FALLIDA"
    assert "16 caracteres" in result.error
    assert "contraseña normal" in result.error
