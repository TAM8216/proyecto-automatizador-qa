import { useState } from "react";
import {
  Alert, Box, Button, Card, CardContent, Chip, CircularProgress, Divider,
  Grid2 as Grid, MenuItem, Paper, Stack, TextField, Typography,
} from "@mui/material";
import { AutoAwesomeOutlined, CheckCircleOutline, ContentCopyOutlined, FactCheckOutlined } from "@mui/icons-material";
import { analyzeRequirement, generateDraft, reviewDraft } from "./api";

const initialRequirement = "";

function ListBlock({ title, items = [], severity = "warning" }) {
  if (!items.length) return null;
  return (
    <Alert severity={severity}>
      <Typography fontWeight={800}>{title}</Typography>
      <Box component="ul" sx={{ my: 0.5, pl: 2.5 }}>
        {items.map((item) => <li key={item}>{item}</li>)}
      </Box>
    </Alert>
  );
}

export default function AIAssistant() {
  const [sourceType, setSourceType] = useState("requisito");
  const [requirement, setRequirement] = useState(initialRequirement);
  const [analysis, setAnalysis] = useState(null);
  const [clarifications, setClarifications] = useState("");
  const [draft, setDraft] = useState(null);
  const [corrections, setCorrections] = useState("");
  const [review, setReview] = useState(null);
  const [gherkinCopied, setGherkinCopied] = useState(false);
  const [loading, setLoading] = useState("");
  const [error, setError] = useState("");

  const analyze = async () => {
    setLoading("analysis"); setError(""); setDraft(null); setReview(null);
    try { setAnalysis(await analyzeRequirement({ requirement, source_type: sourceType })); }
    catch (exception) { setError(exception.message); }
    finally { setLoading(""); }
  };

  const generate = async () => {
    setLoading("draft"); setError("");
    try {
      setDraft(await generateDraft({
        analysis_id: analysis.analysis_id,
        clarifications: clarifications.trim() ? { respuesta_general: clarifications.trim() } : {},
      }));
    } catch (exception) { setError(exception.message); }
    finally { setLoading(""); }
  };

  const approve = async (approved) => {
    setLoading("review"); setError("");
    try {
      setReview(await reviewDraft(analysis.analysis_id, {
        approved, reviewer: "Revisor QA", corrections: corrections.trim() ? [corrections.trim()] : [],
      }));
    } catch (exception) { setError(exception.message); }
    finally { setLoading(""); }
  };

  const copyGherkin = async () => {
    if (!draft?.gherkin) return;
    await navigator.clipboard.writeText(draft.gherkin);
    setGherkinCopied(true);
    window.setTimeout(() => setGherkinCopied(false), 1800);
  };

  return (
    <Grid container spacing={3} alignItems="flex-start">
      <Grid size={{ xs: 12, md: 7.2 }}>
        <Card><CardContent sx={{ p: { xs: 2.5, md: 4 } }}>
          <Stack direction="row" spacing={1.25} alignItems="center" mb={1}>
            <AutoAwesomeOutlined color="secondary" />
            <Typography variant="h2" fontSize={24}>Asistente IA para diseño de pruebas</Typography>
          </Stack>
          <Typography color="text.secondary" mb={3}>
            Analiza primero, pregunta cuando falten datos y genera un borrador. Nunca ejecuta ni decide PASS/FAIL.
          </Typography>
          <TextField select fullWidth label="Tipo de entrada" value={sourceType}
            onChange={(event) => setSourceType(event.target.value)} sx={{ mb: 2 }}>
            <MenuItem value="requisito">Requisito</MenuItem>
            <MenuItem value="caso_prueba">Caso de prueba existente</MenuItem>
          </TextField>
          <TextField fullWidth multiline minRows={8} label="Requisito o caso de prueba"
            placeholder="Describe actor, objetivo, precondiciones, datos y resultado esperado…"
            value={requirement} onChange={(event) => setRequirement(event.target.value)} />
          <Button fullWidth variant="contained" color="secondary" sx={{ mt: 2, color: "white" }}
            disabled={requirement.trim().length < 20 || Boolean(loading)} onClick={analyze}
            startIcon={loading === "analysis" ? <CircularProgress size={18} color="inherit" /> : <FactCheckOutlined />}>
            Analizar ambigüedades
          </Button>

          {analysis && <Stack spacing={1.5} mt={3}>
            <Divider />
            <Stack direction="row" justifyContent="space-between" alignItems="center">
              <Typography fontWeight={800}>Resultado del análisis</Typography>
              <Chip size="small" label={analysis.status} color={analysis.ready_for_generation ? "success" : "warning"} />
            </Stack>
            <Typography>{analysis.summary}</Typography>
            <ListBlock title="Ambigüedades" items={analysis.ambiguities} />
            <ListBlock title="Datos faltantes" items={analysis.missing_data} />
            <ListBlock title="Preguntas que debes responder" items={analysis.questions} severity="info" />
            {!analysis.ready_for_generation && <TextField fullWidth multiline minRows={4}
              label="Aclaraciones humanas" value={clarifications}
              onChange={(event) => setClarifications(event.target.value)} />}
            <Button variant="outlined" onClick={generate} disabled={Boolean(loading) || (!analysis.ready_for_generation && !clarifications.trim())}
              startIcon={loading === "draft" ? <CircularProgress size={18} /> : <AutoAwesomeOutlined />}>
              Generar Gherkin, Page Object y pytest
            </Button>
          </Stack>}
          {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
        </CardContent></Card>
      </Grid>

      <Grid size={{ xs: 12, md: 4.8 }}>
        <Card sx={{ position: { md: "sticky" }, top: 24 }}><CardContent sx={{ p: 3 }}>
          <Typography variant="h2" fontSize={22}>Borrador para revisión</Typography>
          {!draft && <Typography color="text.secondary" mt={2}>Aún no se generó código. Primero completa el análisis.</Typography>}
          {draft && <Stack spacing={2} mt={2}>
            <Chip label={draft.status} color={draft.unverified_selectors.length ? "warning" : "info"} />
            <Box>
              <Stack direction="row" justifyContent="space-between" alignItems="center" mb={0.75}>
                <Typography fontWeight={800}>Escenario Gherkin</Typography>
                <Button size="small" startIcon={<ContentCopyOutlined />} onClick={copyGherkin} disabled={!draft.gherkin}>
                  {gherkinCopied ? "Copiado" : "Copiar"}
                </Button>
              </Stack>
              <Paper variant="outlined" sx={{ p: 1.5, bgcolor: "grey.50", maxHeight: 320, overflow: "auto" }}>
                <Typography component="pre" fontFamily="monospace" fontSize={12} whiteSpace="pre-wrap">
                  {draft.gherkin || [draft.feature, ...draft.scenarios, ...draft.proposed_steps].filter(Boolean).join("\n")}
                </Typography>
              </Paper>
            </Box>
            <ListBlock title="Selectores no verificables" items={draft.unverified_selectors} />
            <ListBlock title="Problemas de validación del código" items={draft.validation_issues} />
            <ListBlock title="Preguntas pendientes del borrador" items={draft.questions} severity="info" />
            {draft.pom_code && <Box><Typography fontWeight={800}>Page Object</Typography><Paper variant="outlined" sx={{ p: 1.5, maxHeight: 220, overflow: "auto" }}><Typography component="pre" fontFamily="monospace" fontSize={11} whiteSpace="pre-wrap">{draft.pom_code}</Typography></Paper></Box>}
            {draft.pytest_code && <Box><Typography fontWeight={800}>pytest</Typography><Paper variant="outlined" sx={{ p: 1.5, maxHeight: 220, overflow: "auto" }}><Typography component="pre" fontFamily="monospace" fontSize={11} whiteSpace="pre-wrap">{draft.pytest_code}</Typography></Paper></Box>}
            <TextField multiline minRows={2} label="Correcciones del revisor" value={corrections}
              onChange={(event) => setCorrections(event.target.value)} />
            <Stack direction={{ xs: "column", sm: "row" }} spacing={1}>
              <Button fullWidth variant="contained" color="secondary" onClick={() => approve(true)}
                disabled={Boolean(loading) || draft.unverified_selectors.length > 0 || draft.validation_issues?.length > 0}>Aprobar borrador</Button>
              <Button fullWidth variant="outlined" onClick={() => approve(false)} disabled={Boolean(loading)}>Solicitar cambios</Button>
            </Stack>
          </Stack>}
          {review && <Alert severity={review.approved ? "success" : "info"} icon={<CheckCircleOutline />} sx={{ mt: 2 }}>
            {review.status}. No se inició ninguna ejecución.
          </Alert>}
        </CardContent></Card>
      </Grid>
    </Grid>
  );
}
