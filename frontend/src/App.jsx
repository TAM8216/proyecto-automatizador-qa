import { useEffect, useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Checkbox,
  Chip,
  CircularProgress,
  Container,
  Divider,
  FormControl,
  FormControlLabel,
  FormHelperText,
  Grid2 as Grid,
  InputLabel,
  LinearProgress,
  MenuItem,
  Paper,
  Radio,
  RadioGroup,
  Select,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import {
  ArticleOutlined,
  BoltOutlined,
  CheckCircleOutline,
  CloudDoneOutlined,
  DownloadOutlined,
  ErrorOutline,
  PlayArrowRounded,
  ScienceOutlined,
  ShieldOutlined,
  AutoAwesomeOutlined,
} from "@mui/icons-material";
import { createRun, getCatalog, getRun, reportUrl } from "./api";
import AIAssistant from "./AIAssistant";

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const terminalStates = new Set(["FINALIZADA", "FALLIDA"]);

const statusColor = {
  PENDIENTE: "warning",
  "EN CURSO": "info",
  FINALIZADA: "success",
  FALLIDA: "error",
};

function TypeCard({ active, disabled, icon, title, description, badge, onClick }) {
  return (
    <Paper
      component="button"
      type="button"
      disabled={disabled}
      onClick={onClick}
      elevation={0}
      sx={{
        width: "100%",
        p: 2.25,
        textAlign: "left",
        border: "1px solid",
        borderColor: active ? "secondary.main" : "divider",
        bgcolor: active ? "rgba(43,154,134,.07)" : "background.paper",
        cursor: disabled ? "not-allowed" : "pointer",
        opacity: disabled ? 0.58 : 1,
        transition: "150ms ease",
        "&:hover": disabled ? {} : { borderColor: "secondary.main", transform: "translateY(-1px)" },
      }}
    >
      <Stack direction="row" spacing={1.5} alignItems="flex-start">
        <Box sx={{ color: active ? "secondary.main" : "primary.main", mt: 0.25 }}>{icon}</Box>
        <Box sx={{ flex: 1 }}>
          <Stack direction="row" justifyContent="space-between" alignItems="center" gap={1}>
            <Typography fontWeight={800}>{title}</Typography>
            {badge && <Chip size="small" label={badge} />}
          </Stack>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
            {description}
          </Typography>
        </Box>
      </Stack>
    </Paper>
  );
}

function Metric({ label, value, color = "text.primary" }) {
  return (
    <Box>
      <Typography variant="caption" color="text.secondary" fontWeight={700}>
        {label}
      </Typography>
      <Typography variant="h5" fontWeight={800} color={color}>
        {value ?? 0}
      </Typography>
    </Box>
  );
}

export default function App() {
  const [activeView, setActiveView] = useState("execution");
  const [catalog, setCatalog] = useState(null);
  const [catalogError, setCatalogError] = useState("");
  const [email, setEmail] = useState("");
  const [touchedEmail, setTouchedEmail] = useState(false);
  const [testType, setTestType] = useState("funcional");
  const [flowId, setFlowId] = useState("");
  const [suiteId, setSuiteId] = useState("");
  const [selectionMode, setSelectionMode] = useState("suite");
  const [caseIds, setCaseIds] = useState([]);
  const [loadProfile, setLoadProfile] = useState({ users: 5, spawnRate: 1, duration: 30 });
  const [submitting, setSubmitting] = useState(false);
  const [run, setRun] = useState(null);
  const [actionError, setActionError] = useState("");

  useEffect(() => {
    let mounted = true;
    getCatalog()
      .then((data) => {
        if (!mounted) return;
        setCatalog(data);
        const firstAvailable = data.suites.find((suite) => suite.type === "funcional");
        const firstFlow = data.flows?.find((flow) => flow.type === "funcional");
        setFlowId(firstFlow?.id || firstAvailable?.flow || "");
        setSuiteId(firstAvailable?.id || "");
      })
      .catch((error) => mounted && setCatalogError(error.message));
    return () => { mounted = false; };
  }, []);

  useEffect(() => {
    if (!run?.run_id || terminalStates.has(run.status)) return undefined;
    const timer = window.setInterval(async () => {
      try {
        const current = await getRun(run.run_id);
        setRun(current);
        if (terminalStates.has(current.status)) window.clearInterval(timer);
      } catch (error) {
        setActionError(`No se pudo actualizar la corrida: ${error.message}`);
        window.clearInterval(timer);
      }
    }, 1500);
    return () => window.clearInterval(timer);
  }, [run?.run_id, run?.status]);

  const flows = catalog?.flows?.filter((flow) => flow.type === testType) || [];
  const typedSuites = catalog?.suites.filter((suite) => suite.type === testType) || [];
  const suites = flowId ? typedSuites.filter((suite) => suite.flow === flowId) : typedSuites;
  const selectedFlow = flows.find((flow) => flow.id === flowId);
  const selectedSuite = suites.find((suite) => suite.id === suiteId);
  const emailValid = emailPattern.test(email);
  const selectionValid = selectionMode === "suite" ? Boolean(suiteId) : caseIds.length > 0;
  const canSubmit = emailValid && selectionValid && !submitting && !run?.run_id;

  const selectedCount = useMemo(
    () => (selectionMode === "suite" ? selectedSuite?.cases.length || 0 : caseIds.length),
    [selectionMode, selectedSuite, caseIds],
  );

  const handleSuiteChange = (value) => {
    setSuiteId(value);
    setCaseIds([]);
  };

  const toggleCase = (caseId) => {
    setCaseIds((current) =>
      current.includes(caseId) ? current.filter((id) => id !== caseId) : [...current, caseId],
    );
  };

  const handleTypeChange = (value) => {
    setTestType(value);
    const firstFlow = catalog?.flows?.find((flow) => flow.type === value);
    const firstSuite = catalog?.suites.find(
      (suite) => suite.type === value && (!firstFlow || suite.flow === firstFlow.id),
    );
    setFlowId(firstFlow?.id || firstSuite?.flow || "");
    setSuiteId(firstSuite?.id || "");
    setCaseIds([]);
  };

  const handleFlowChange = (value) => {
    setFlowId(value);
    const firstSuite = catalog?.suites.find(
      (suite) => suite.type === testType && suite.flow === value,
    );
    setSuiteId(firstSuite?.id || "");
    setCaseIds([]);
  };

  const execute = async () => {
    setTouchedEmail(true);
    if (!emailValid || !selectionValid) return;
    setSubmitting(true);
    setActionError("");
    try {
      const accepted = await createRun({
        email,
        type: testType,
        suite: selectionMode === "suite" ? suiteId : null,
        case_ids: selectionMode === "cases" ? caseIds : [],
        all_cases: false,
        users: loadProfile.users,
        spawn_rate: loadProfile.spawnRate,
        duration_seconds: loadProfile.duration,
      });
      setRun(accepted);
    } catch (error) {
      setActionError(error.message);
    } finally {
      setSubmitting(false);
    }
  };

  const reset = () => {
    setRun(null);
    setActionError("");
    setCaseIds([]);
  };

  return (
    <Box minHeight="100vh">
      <Box sx={{ bgcolor: "primary.dark", color: "white", py: { xs: 4, md: 5.5 } }}>
        <Container maxWidth="lg">
          <Stack direction={{ xs: "column", sm: "row" }} justifyContent="space-between" gap={3}>
            <Box maxWidth={720}>
              <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1.5 }}>
                <ShieldOutlined sx={{ color: "secondary.main" }} />
                <Typography variant="overline" fontWeight={800} letterSpacing={1.6}>
                  IPAS · IUS PUNIENDI
                </Typography>
              </Stack>
              <Typography variant="h1" sx={{ fontSize: { xs: 36, md: 52 }, lineHeight: 1.05 }}>
                Centro de automatización QA
              </Typography>
              <Typography sx={{ mt: 2, color: "rgba(255,255,255,.72)", fontSize: 17 }}>
                Ejecuta pruebas trazables contra el ambiente jurídico local y recibe evidencias listas para revisión.
              </Typography>
            </Box>
            <Stack direction="row" spacing={1.25} alignItems="center">
              <CloudDoneOutlined color="secondary" />
              <Box>
                <Typography variant="caption" sx={{ color: "rgba(255,255,255,.6)" }}>AMBIENTE</Typography>
                <Typography fontWeight={800}>local-qa</Typography>
              </Box>
            </Stack>
          </Stack>
        </Container>
      </Box>

      <Container maxWidth="lg" sx={{ py: { xs: 3, md: 5 } }}>
        <Stack direction="row" spacing={1} mb={3}>
          <Button variant={activeView === "execution" ? "contained" : "outlined"}
            startIcon={<ScienceOutlined />} onClick={() => setActiveView("execution")}>Ejecución</Button>
          <Button variant={activeView === "ai" ? "contained" : "outlined"}
            startIcon={<AutoAwesomeOutlined />} onClick={() => setActiveView("ai")}>Asistente IA</Button>
        </Stack>
        {activeView === "execution" ? <>
        {catalogError && <Alert severity="error" sx={{ mb: 3 }}>{catalogError}</Alert>}
        {!catalog && !catalogError && (
          <Stack alignItems="center" py={8} spacing={2}>
            <CircularProgress color="secondary" />
            <Typography color="text.secondary">Cargando catálogo real de pruebas…</Typography>
          </Stack>
        )}

        {catalog && (
          <Grid container spacing={3} alignItems="flex-start">
            <Grid size={{ xs: 12, md: 7.4 }}>
              <Card>
                <CardContent sx={{ p: { xs: 2.5, md: 4 } }}>
                  <Stack direction="row" spacing={1.25} alignItems="center" mb={3}>
                    <ScienceOutlined color="secondary" />
                    <Box>
                      <Typography variant="h2" fontSize={24}>Configura la ejecución</Typography>
                      <Typography variant="body2" color="text.secondary">Los casos provienen del catálogo versionado.</Typography>
                    </Box>
                  </Stack>

                  <Typography fontWeight={800} mb={1.25}>1. Tipo de prueba</Typography>
                  <Grid container spacing={1.5} mb={3}>
                    <Grid size={{ xs: 12, sm: 6 }}>
                      <TypeCard
                        active={testType === "funcional"}
                        icon={<ScienceOutlined />}
                        title="Funcionales"
                        description="UI, API, reglas de negocio, roles y E2E."
                        onClick={() => handleTypeChange("funcional")}
                      />
                    </Grid>
                    <Grid size={{ xs: 12, sm: 6 }}>
                      <TypeCard
                        active={testType === "no_funcional"}
                        disabled={!catalog.types.find((item) => item.id === "no_funcional")?.available}
                        icon={<BoltOutlined />}
                        title="No funcionales"
                        description="Carga, estrés y rendimiento de endpoints locales."
                        badge="Local"
                        onClick={() => handleTypeChange("no_funcional")}
                      />
                    </Grid>
                  </Grid>

                  {flows.length > 0 && <>
                    <Typography fontWeight={800} mb={1.25}>2. Flujo funcional</Typography>
                    <FormControl fullWidth sx={{ mb: 2 }}>
                      <InputLabel id="flow-label">Flujo</InputLabel>
                      <Select
                        labelId="flow-label"
                        label="Flujo"
                        value={flowId}
                        onChange={(event) => handleFlowChange(event.target.value)}
                      >
                        {flows.map((flow) => (
                          <MenuItem key={flow.id} value={flow.id}>{flow.name}</MenuItem>
                        ))}
                      </Select>
                      <FormHelperText>{selectedFlow?.description}</FormHelperText>
                    </FormControl>
                  </>}

                  <Typography fontWeight={800} mb={1.25}>{flows.length > 0 ? "3" : "2"}. Suite de pruebas</Typography>
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel id="suite-label">Suite</InputLabel>
                    <Select
                      labelId="suite-label"
                      label="Suite"
                      value={suiteId}
                      onChange={(event) => handleSuiteChange(event.target.value)}
                    >
                      {suites.map((suite) => (
                        <MenuItem key={suite.id} value={suite.id}>{suite.name}</MenuItem>
                      ))}
                    </Select>
                    <FormHelperText>{selectedSuite?.description}</FormHelperText>
                  </FormControl>

                  <RadioGroup row value={selectionMode} onChange={(event) => setSelectionMode(event.target.value)}>
                    <FormControlLabel value="suite" control={<Radio />} label="Ejecutar suite completa" />
                    <FormControlLabel value="cases" control={<Radio />} label="Elegir casos específicos" />
                  </RadioGroup>

                  {testType === "no_funcional" && (
                    <Grid container spacing={1.5} sx={{ mt: 1.5 }}>
                      <Grid size={{ xs: 12, sm: 4 }}>
                        <TextField
                          fullWidth label="Usuarios" type="number" value={loadProfile.users}
                          inputProps={{ min: 1, max: 50 }}
                          onChange={(event) => setLoadProfile((current) => ({ ...current, users: Number(event.target.value) }))}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, sm: 4 }}>
                        <TextField
                          fullWidth label="Usuarios/segundo" type="number" value={loadProfile.spawnRate}
                          inputProps={{ min: 0.1, max: 10, step: 0.1 }}
                          onChange={(event) => setLoadProfile((current) => ({ ...current, spawnRate: Number(event.target.value) }))}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, sm: 4 }}>
                        <TextField
                          fullWidth label="Duración (s)" type="number" value={loadProfile.duration}
                          inputProps={{ min: 10, max: 600 }}
                          onChange={(event) => setLoadProfile((current) => ({ ...current, duration: Number(event.target.value) }))}
                        />
                      </Grid>
                      <Grid size={12}>
                        <Alert severity="info">Criterio: p95 &lt; 2000 ms y errores &lt; 1%. IA excluida.</Alert>
                      </Grid>
                    </Grid>
                  )}

                  {selectionMode === "cases" && (
                    <Paper variant="outlined" sx={{ mt: 1.5, maxHeight: 300, overflow: "auto" }}>
                      {selectedSuite?.cases.map((testCase, index) => (
                        <Box key={testCase.id}>
                          <FormControlLabel
                            sx={{ width: "100%", m: 0, px: 1.5, py: 0.75, alignItems: "flex-start" }}
                            control={
                              <Checkbox
                                checked={caseIds.includes(testCase.id)}
                                onChange={() => toggleCase(testCase.id)}
                              />
                            }
                            label={
                              <Box pt={0.75}>
                                <Typography variant="body2" fontWeight={800}>{testCase.id} · {testCase.name}</Typography>
                                <Typography variant="caption" color="text.secondary">{testCase.module} · prioridad {testCase.priority}</Typography>
                              </Box>
                            }
                          />
                          {index < selectedSuite.cases.length - 1 && <Divider />}
                        </Box>
                      ))}
                    </Paper>
                  )}

                  <Typography fontWeight={800} mt={3} mb={1.25}>{flows.length > 0 ? "4" : "3"}. Entrega del reporte</Typography>
                  {!(catalog.delivery?.smtp_ready ?? catalog.delivery?.smtp_configured) && (
                    <Alert severity="warning" sx={{ mb: 1.5 }}>
                      {catalog.delivery?.message || "SMTP no está listo. Configura el servicio y reinicia la API antes de solicitar el envío."}
                    </Alert>
                  )}
                  <TextField
                    fullWidth
                    label="Correo destinatario"
                    placeholder="nombre@dominio.com"
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    onBlur={() => setTouchedEmail(true)}
                    error={touchedEmail && !emailValid}
                    helperText={touchedEmail && !emailValid ? "Ingresa un correo con formato válido." : "Recibirá el DOCX y el HTML autocontenido."}
                  />

                  {actionError && <Alert severity="error" sx={{ mt: 2 }}>{actionError}</Alert>}
                  <Button
                    fullWidth
                    variant="contained"
                    color="secondary"
                    size="large"
                    startIcon={submitting ? <CircularProgress size={19} color="inherit" /> : <PlayArrowRounded />}
                    disabled={!canSubmit}
                    onClick={execute}
                    sx={{ mt: 3, py: 1.25, color: "white" }}
                  >
                    Ejecutar {selectedCount} {selectedCount === 1 ? "caso" : "casos"}
                  </Button>
                </CardContent>
              </Card>
            </Grid>

            <Grid size={{ xs: 12, md: 4.6 }}>
              <Card sx={{ position: { md: "sticky" }, top: 24 }}>
                <CardContent sx={{ p: { xs: 2.5, md: 3 } }}>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h2" fontSize={22}>Estado de corrida</Typography>
                    {run?.status && <Chip label={run.status} color={statusColor[run.status]} size="small" />}
                  </Stack>

                  {!run && (
                    <Box sx={{ textAlign: "center", py: 5 }}>
                      <ArticleOutlined sx={{ fontSize: 48, color: "text.disabled" }} />
                      <Typography fontWeight={800} mt={1}>Aún no hay una ejecución</Typography>
                      <Typography variant="body2" color="text.secondary" mt={0.75}>
                        Completa la configuración para generar un run trazable.
                      </Typography>
                    </Box>
                  )}

                  {run && (
                    <Stack spacing={2.25}>
                      {!terminalStates.has(run.status) && <LinearProgress color="secondary" />}
                      <Box>
                        <Typography variant="caption" color="text.secondary" fontWeight={700}>RUN ID</Typography>
                        <Typography variant="body2" fontFamily="monospace" sx={{ overflowWrap: "anywhere" }}>{run.run_id}</Typography>
                      </Box>

                      {run.summary && (
                        <Grid container spacing={2}>
                          <Grid size={3}><Metric label="TOTAL" value={run.summary.total} /></Grid>
                          <Grid size={3}><Metric label="PASS" value={run.summary.pass} color="success.main" /></Grid>
                          <Grid size={3}><Metric label="FAIL" value={run.summary.fail} color="error.main" /></Grid>
                          <Grid size={3}><Metric label="N/R" value={run.summary.not_run} /></Grid>
                        </Grid>
                      )}

                      {run.status === "FINALIZADA" && (
                        <Alert icon={<CheckCircleOutline />} severity="success">Ejecución y entrega completadas.</Alert>
                      )}
                      {run.status === "FALLIDA" && (
                        <Alert icon={<ErrorOutline />} severity="error">
                          {run.email_delivery?.error || run.error || "La corrida terminó con un fallo."}
                        </Alert>
                      )}

                      {run.email_delivery && (
                        <Paper variant="outlined" sx={{ p: 1.75 }}>
                          <Typography variant="caption" color="text.secondary" fontWeight={700}>CORREO</Typography>
                          <Typography fontWeight={800}>{run.email_delivery.status}</Typography>
                          <Typography variant="body2" color="text.secondary">{run.email_delivery.recipient}</Typography>
                        </Paper>
                      )}

                      {run.performance?.aggregate && (
                        <Paper variant="outlined" sx={{ p: 1.75 }}>
                          <Typography variant="caption" color="text.secondary" fontWeight={700}>RENDIMIENTO</Typography>
                          <Grid container spacing={1.5} sx={{ mt: 0.5 }}>
                            <Grid size={6}><Metric label="p95" value={`${run.performance.aggregate.p95_ms} ms`} /></Grid>
                            <Grid size={6}><Metric label="REQ/S" value={run.performance.aggregate.throughput_rps} /></Grid>
                            <Grid size={6}><Metric label="SOLICITUDES" value={run.performance.aggregate.requests} /></Grid>
                            <Grid size={6}><Metric label="ERRORES" value={`${(run.performance.aggregate.error_rate * 100).toFixed(2)}%`} color="error.main" /></Grid>
                          </Grid>
                        </Paper>
                      )}

                      {run.reports?.status === "GENERADOS" && (
                        <Stack direction={{ xs: "column", sm: "row", md: "column" }} spacing={1}>
                          <Button component="a" href={reportUrl(run.run_id, "docx")} startIcon={<DownloadOutlined />} variant="outlined">Descargar DOCX</Button>
                          <Button component="a" href={reportUrl(run.run_id, "html")} startIcon={<DownloadOutlined />} variant="outlined">Descargar HTML</Button>
                        </Stack>
                      )}

                      {terminalStates.has(run.status) && <Button onClick={reset}>Preparar otra ejecución</Button>}
                    </Stack>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
        </> : <AIAssistant />}
      </Container>
    </Box>
  );
}
