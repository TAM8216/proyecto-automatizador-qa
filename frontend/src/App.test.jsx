import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ThemeProvider } from "@mui/material";
import App from "./App";
import { theme } from "./theme";

const catalog = {
  types: [{ id: "funcional", name: "Funcionales", available: true }],
  flows: [{ id: "acceso", name: "Acceso y sesión", description: "Ingreso al sistema.", type: "funcional" }],
  delivery: { smtp_configured: true, smtp_ready: true },
  suites: [
    {
      id: "smoke",
      name: "Smoke",
      description: "Disponibilidad mínima.",
      type: "funcional",
      flow: "acceso",
      cases: [
        { id: "TC-SMK-001", name: "Disponibilidad", module: "infraestructura", priority: "Alta" },
        { id: "TC-LOG-001", name: "Login válido", module: "autenticación", priority: "Alta" },
      ],
    },
  ],
};

function renderApp() {
  return render(<ThemeProvider theme={theme}><App /></ThemeProvider>);
}

afterEach(() => vi.restoreAllMocks());

test("carga el catálogo y bloquea correo inválido", async () => {
  vi.spyOn(globalThis, "fetch").mockResolvedValue({ ok: true, json: async () => catalog });
  renderApp();
  expect(await screen.findByText("Smoke")).toBeInTheDocument();
  expect(screen.getByText("Acceso y sesión")).toBeInTheDocument();
  const email = screen.getByLabelText("Correo destinatario");
  await userEvent.type(email, "correo-invalido");
  await userEvent.tab();
  expect(screen.getByText("Ingresa un correo con formato válido.")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /Ejecutar 2 casos/i })).toBeDisabled();
});

test("envía una suite válida y muestra el run id", async () => {
  const fetchMock = vi.spyOn(globalThis, "fetch");
  fetchMock
    .mockResolvedValueOnce({ ok: true, json: async () => catalog })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ run_id: "run-ui-123", status: "PENDIENTE", status_url: "http://test" }),
    });
  renderApp();
  await screen.findByText("Smoke");
  await userEvent.type(screen.getByLabelText("Correo destinatario"), "qa@example.com");
  await userEvent.click(screen.getByRole("button", { name: /Ejecutar 2 casos/i }));
  await waitFor(() => expect(screen.getByText("run-ui-123")).toBeInTheDocument());
  const post = fetchMock.mock.calls[1];
  expect(JSON.parse(post[1].body)).toMatchObject({ email: "qa@example.com", suite: "smoke", type: "funcional" });
});
