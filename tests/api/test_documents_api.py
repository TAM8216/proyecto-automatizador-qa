import io

import pytest


@pytest.mark.api
@pytest.mark.documentos
@pytest.mark.case_id("TC-DOC-001")
def test_cargar_documento_pdf_valido(api_client, auth_headers, qa_case_id):
    response = api_client.post(
        f"/documentos/casos/{qa_case_id}",
        headers=auth_headers("abogado"),
        files={"documento": ("evidencia_qa.pdf", io.BytesIO(b"%PDF-1.4\n% QA ficticio\n%%EOF"), "application/pdf")},
    )
    assert response.status_code == 201, response.text
    document_id = response.json()["id"]
    cleanup = api_client.delete(f"/documentos/{document_id}", headers=auth_headers("abogado"))
    assert cleanup.status_code == 204


@pytest.mark.api
@pytest.mark.documentos
@pytest.mark.case_id("TC-DOC-002")
def test_rechazar_extension_no_permitida(api_client, auth_headers, qa_case_id):
    response = api_client.post(
        f"/documentos/casos/{qa_case_id}",
        headers=auth_headers("abogado"),
        files={"documento": ("malware.exe", io.BytesIO(b"contenido inerte"), "application/octet-stream")},
    )
    assert response.status_code == 400
    assert "Solo se permiten" in response.json()["message"]


@pytest.mark.api
@pytest.mark.documentos
@pytest.mark.case_id("TC-DOC-003")
def test_rechazar_archivo_superior_a_10mb(api_client, auth_headers, qa_case_id):
    oversized = io.BytesIO(b"%PDF-1.4\n" + b"0" * (10 * 1024 * 1024 + 1))
    response = api_client.post(
        f"/documentos/casos/{qa_case_id}",
        headers=auth_headers("abogado"),
        files={"documento": ("limite_10mb.pdf", oversized, "application/pdf")},
    )
    assert response.status_code == 400
    assert "File too large" in response.json()["message"]

