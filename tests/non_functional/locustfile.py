from __future__ import annotations

from locust import HttpUser, between, task

from backend.config import get_settings


class IPASLocalUser(HttpUser):
    wait_time = between(0.4, 1.0)

    def on_start(self) -> None:
        settings = get_settings()
        self.headers = {}
        self.case_id = None
        with self.client.post(
            "/auth/login",
            json={
                "email": settings.qa_abogado_email,
                "password": settings.qa_abogado_password,
            },
            name="POST /auth/login",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Login QA devolvió HTTP {response.status_code}")
                return
            token = response.json().get("token")
            if not token:
                response.failure("Login QA no devolvió token")
                return
            self.headers = {"Authorization": f"Bearer {token}"}

        with self.client.get(
            "/casos",
            headers=self.headers,
            name="GET /casos",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Listado devolvió HTTP {response.status_code}")
                return
            case = next(
                (item for item in response.json() if item.get("nurej_cud") == "QA-EXP-0001"),
                None,
            )
            if case is None:
                response.failure("No existe el expediente ficticio QA-EXP-0001")
                return
            self.case_id = case["id"]

    @task(4)
    def list_cases(self) -> None:
        if self.headers:
            self.client.get("/casos", headers=self.headers, name="GET /casos")

    @task(3)
    def case_detail(self) -> None:
        if self.case_id:
            self.client.get(
                f"/casos/{self.case_id}",
                headers=self.headers,
                name="GET /casos/:id",
            )

    @task(2)
    def case_documents(self) -> None:
        if self.case_id:
            self.client.get(
                f"/documentos/casos/{self.case_id}",
                headers=self.headers,
                name="GET /documentos/casos/:id",
            )
