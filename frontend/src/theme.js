import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#123047", dark: "#0A1F30", light: "#31556F" },
    secondary: { main: "#2B9A86", dark: "#18715F" },
    background: { default: "#F2F5F7", paper: "#FFFFFF" },
    text: { primary: "#16232E", secondary: "#5A6975" },
    success: { main: "#187A58" },
    error: { main: "#B9382E" },
    warning: { main: "#A66A18" },
  },
  typography: {
    fontFamily: '"Segoe UI", Inter, Arial, sans-serif',
    h1: { fontWeight: 800, letterSpacing: "-0.04em" },
    h2: { fontWeight: 750, letterSpacing: "-0.025em" },
    h3: { fontWeight: 700 },
    button: { fontWeight: 700, textTransform: "none" },
  },
  shape: { borderRadius: 14 },
  components: {
    MuiButton: { styleOverrides: { root: { borderRadius: 10, minHeight: 44 } } },
    MuiCard: { styleOverrides: { root: { boxShadow: "0 14px 42px rgba(18,48,71,.08)" } } },
  },
});
