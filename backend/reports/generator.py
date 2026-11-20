from __future__ import annotations

import argparse
import base64
import json
from datetime import datetime
from html import escape
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor
ROOT = Path(__file__).resolve().parents[2]
DETAILS_PATH = ROOT / "config" / "report_details.json"


def local_datetime(value: str) -> str:
    try:
        return datetime.fromisoformat(value).strftime("%d/%m/%Y %H:%M:%S %z")
    except (TypeError, ValueError):
        return value or "N/A"


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd")) or OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}")) or OxmlElement(f"w:{margin}")
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")
        tc_mar.append(node)


def set_repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def format_table(table, header_fill="10263A", header_text="FFFFFF", font_size=8.5) -> None:
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    set_repeat_table_header(table.rows[0])
    for row_index, row in enumerate(table.rows):
        for cell in row.cells:
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(cell)
            if row_index == 0:
                set_cell_shading(cell, header_fill)
            elif row_index % 2 == 0:
                set_cell_shading(cell, "F3F6F8")
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(0)
                for run in paragraph.runs:
                    run.font.name = "Aptos"
                    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Aptos")
                    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Aptos")
                    run.font.size = Pt(font_size)
                    if row_index == 0:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor.from_string(header_text)


def set_col_widths(table, widths_cm: list[float]) -> None:
    for row in table.rows:
        for index, width in enumerate(widths_cm):
            row.cells[index].width = Cm(width)


def load_report_data(result_path: Path, email: str) -> dict:
    result = json.loads(result_path.read_text(encoding="utf-8"))
    display_status = result.get("test_status") or result["status"]
    details = json.loads(DETAILS_PATH.read_text(encoding="utf-8"))
    selection = result.get("selection", {})
    suite = ", ".join(selection.get("suites") or selection.get("case_ids") or ["all"])
    raw_summary = result.get("summary", {})
    total = int(raw_summary.get("total", len(result.get("cases", []))))
    passed = int(raw_summary.get("pass", 0))
    summary = {
        "total": total,
        "pass": passed,
        "fail": int(raw_summary.get("fail", 0)),
        "skipped": int(raw_summary.get("skipped", 0)),
        "not_run": int(raw_summary.get("not_run", 0)),
        "success_rate": round((passed / total * 100) if total else 0, 2),
    }
    cases = []
    for raw in result.get("cases", []):
        detail = details[raw["id"]]
        steps = []
        for index, item in enumerate(detail["steps"]):
            is_failed_step = raw["status"] == "FAIL" and index == len(detail["steps"]) - 1
            step_status = "FAIL" if is_failed_step else (raw["status"] if raw["status"] in {"SKIPPED", "NOT RUN"} else "PASS")
            observed = raw.get("observation", "") if is_failed_step else (
                "Paso ejecutado y aserción satisfecha" if step_status == "PASS" else "Paso no ejecutado"
            )
            steps.append({**item, "observed": observed, "status": step_status})
        evidence_dir = ROOT / "evidencias" / result["run_id"] / raw["id"]
        images = []
        if evidence_dir.exists():
            for image_path in sorted(evidence_dir.glob("*.png")):
                images.append({"path": image_path, "base64": base64.b64encode(image_path.read_bytes()).decode("ascii")})
        cases.append({
            **raw,
            "priority": detail["priority"],
            "objective": detail["objective"],
            "preconditions": detail["preconditions"],
            "data": detail["data"],
            "expected": detail["expected"],
            "steps": steps,
            "images": images,
        })
    selection_type = selection.get("type", "funcional")
    return {
        "general": {
            "project": "IPAS - IUS PUNIENDI",
            "environment": "local-qa / ius_puniendi_qa",
            "type": "No funcional - rendimiento" if selection_type == "no_funcional" else "Funcional automatizada",
            "suite": suite,
            "run_id": result["run_id"],
            "status": display_status,
            "started_at": local_datetime(result.get("started_at")),
            "finished_at": local_datetime(result.get("finished_at")),
            "duration": f"{result.get('duration_seconds', 0):.2f} segundos",
            "email": email or "N/A - ejecución local",
        },
        "summary": summary,
        "performance": result.get("performance"),
        "cases": cases,
    }


def add_label_paragraph(document: Document, label: str, text: str) -> None:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(5)
    run = paragraph.add_run(f"{label} ")
    run.bold = True
    paragraph.add_run(text)


def build_docx(data: dict, output_path: Path) -> None:
    document = Document()
    section = document.sections[0]
    section.top_margin = Cm(1.8)
    section.bottom_margin = Cm(1.7)
    section.left_margin = Cm(2)
    section.right_margin = Cm(2)
    styles = document.styles
    normal = styles["Normal"]
    normal.font.name = "Aptos"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    normal.font.size = Pt(10)
    normal.paragraph_format.space_after = Pt(6)
    for style_name, size in (("Title", 25), ("Heading 1", 17), ("Heading 2", 13)):
        style = styles[style_name]
        style.font.name = "Aptos Display"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Aptos Display")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos Display")
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.font.bold = True
    title_ppr = styles["Title"]._element.get_or_add_pPr()
    title_border = title_ppr.find(qn("w:pBdr"))
    if title_border is not None:
        title_ppr.remove(title_border)

    title = document.add_paragraph(style="Title")
    title.add_run("Informe detallado de automatización IPAS")
    intro = document.add_paragraph(
        f"La corrida {data['general']['run_id']} terminó con estado {data['general']['status']}. "
        f"Se ejecutaron {data['summary']['total']} casos en el ambiente local QA, con "
        f"{data['summary']['pass']} PASS y {data['summary']['fail']} FAIL."
    )
    intro.paragraph_format.space_after = Pt(12)

    document.add_heading("Datos generales", level=1)
    general = data["general"]
    table = document.add_table(rows=5, cols=4)
    rows = [
        ("Proyecto", general["project"], "Ambiente", general["environment"]),
        ("Tipo", general["type"], "Suite", general["suite"]),
        ("Inicio", general["started_at"], "Fin", general["finished_at"]),
        ("Duración", general["duration"], "Correo", general["email"]),
        ("Run ID", general["run_id"], "Estado", general["status"]),
    ]
    for row, values in zip(table.rows, rows):
        for cell, value in zip(row.cells, values):
            cell.text = str(value)
    format_table(table, header_fill="E7EEF3", header_text="000000", font_size=9)
    for row in table.rows:
        row.cells[0].paragraphs[0].runs[0].bold = True
        row.cells[2].paragraphs[0].runs[0].bold = True
    set_col_widths(table, [2.6, 5.4, 2.4, 5.6])

    document.add_heading("Resumen de resultados", level=1)
    summary = data["summary"]
    summary_table = document.add_table(rows=2, cols=6)
    headers = ["Total", "PASS", "FAIL", "SKIPPED", "NOT RUN", "Éxito"]
    values = [summary["total"], summary["pass"], summary["fail"], summary["skipped"], summary["not_run"], f"{summary['success_rate']}%"]
    for index, value in enumerate(headers):
        summary_table.cell(0, index).text = str(value)
    for index, value in enumerate(values):
        summary_table.cell(1, index).text = str(value)
        summary_table.cell(1, index).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_table(summary_table, font_size=9)
    set_col_widths(summary_table, [2.3] * 6)

    performance = data.get("performance")
    if performance:
        document.add_heading("Métricas de rendimiento", level=1)
        profile = performance["profile"]
        criteria = performance["criteria"]
        aggregate = performance["aggregate"]
        add_label_paragraph(
            document,
            "Perfil",
            f"{profile['users']} usuarios, incremento {profile['spawn_rate']} usuario/s, "
            f"duración {profile['duration_seconds']} segundos",
        )
        add_label_paragraph(
            document,
            "Criterio",
            f"p95 < {criteria['p95_limit_ms']} ms y errores < {criteria['error_rate_limit'] * 100:.2f}%",
        )
        perf_table = document.add_table(rows=2, cols=8)
        perf_headers = ["Solicitudes", "Req/s", "Promedio", "Mediana", "p95", "Mín", "Máx", "Errores"]
        perf_values = [
            aggregate.get("requests", 0), aggregate.get("throughput_rps", 0),
            f"{aggregate.get('average_ms', 0)} ms", f"{aggregate.get('median_ms', 0)} ms",
            f"{aggregate.get('p95_ms', 0)} ms", f"{aggregate.get('min_ms', 0)} ms",
            f"{aggregate.get('max_ms', 0)} ms", f"{aggregate.get('error_rate', 0) * 100:.2f}%",
        ]
        for index, value in enumerate(perf_headers):
            perf_table.cell(0, index).text = str(value)
        for index, value in enumerate(perf_values):
            perf_table.cell(1, index).text = str(value)
        format_table(perf_table, font_size=7.5)

    separator = document.add_paragraph()
    separator.paragraph_format.space_after = Pt(2)
    separator.add_run(" ").font.size = Pt(1)

    overview = document.add_table(rows=1, cols=5)
    for index, value in enumerate(["ID", "Nombre", "Tipo y módulo", "Estado", "Observación"]):
        overview.cell(0, index).text = value
    for case in data["cases"]:
        cells = overview.add_row().cells
        values = [case["id"], case["name"], f"{case['type']}\n{case['module']}", case["status"], case["observation"]]
        for cell, value in zip(cells, values):
            cell.text = str(value)
    format_table(overview, font_size=8)
    set_col_widths(overview, [2.1, 4.3, 3.5, 1.7, 4.4])

    if performance:
        document.add_page_break()
    detail_heading = document.add_heading("Detalle por caso", level=1)
    detail_heading.paragraph_format.keep_with_next = True
    for case_index, case in enumerate(data["cases"]):
        if case_index:
            document.add_page_break()
        document.add_heading(f"{case['id']} {case['name']}", level=2)
        add_label_paragraph(document, "Estado", f"{case['status']}    Prioridad {case['priority']}    Módulo {case['module']}")
        add_label_paragraph(document, "Objetivo", case["objective"])
        paragraph = document.add_paragraph()
        paragraph.add_run("Precondiciones").bold = True
        for item in case["preconditions"]:
            document.add_paragraph(item, style="List Bullet")

        document.add_paragraph().add_run("Datos de prueba").bold = True
        data_table = document.add_table(rows=1, cols=4)
        for index, value in enumerate(["Dato", "Valor", "Origen", "Observación"]):
            data_table.cell(0, index).text = value
        for item in case["data"]:
            cells = data_table.add_row().cells
            for cell, value in zip(cells, [item["name"], item["value"], item["source"], item["observation"]]):
                cell.text = str(value)
        format_table(data_table, header_fill="386CC7", font_size=8.5)
        set_col_widths(data_table, [2.7, 4.8, 3.5, 4.9])
        add_label_paragraph(document, "Resultado esperado", case["expected"])

        steps = document.add_table(rows=1, cols=5)
        for index, value in enumerate(["#", "Paso ejecutado", "Esperado", "Observado", "Estado"]):
            steps.cell(0, index).text = value
        for number, step in enumerate(case["steps"], 1):
            cells = steps.add_row().cells
            for cell, value in zip(cells, [number, step["action"], step["expected"], step["observed"], step["status"]]):
                cell.text = str(value)
        format_table(steps, font_size=7.7)
        set_col_widths(steps, [0.8, 4.3, 4.0, 4.5, 1.7])

        if case["status"] == "FAIL":
            add_label_paragraph(document, "Error y reproducción", case["observation"])
            if case.get("defect"):
                add_label_paragraph(document, "Defecto relacionado", case["defect"])
        if case["images"]:
            for image_index, image in enumerate(case["images"], 1):
                paragraph = document.add_paragraph()
                paragraph.paragraph_format.keep_with_next = True
                paragraph.add_run(f"Evidencia {image_index}").bold = True
                picture = document.add_paragraph()
                picture.alignment = WD_ALIGN_PARAGRAPH.CENTER
                picture.paragraph_format.keep_together = True
                picture.add_run().add_picture(str(image["path"]), width=Inches(6.15))
        else:
            evidence_text = (
                "Registro técnico en CSV de métricas, locust.log y result.json del run."
                if performance else
                "Registro técnico en JUnit, pytest.log y result.json del run."
            )
            add_label_paragraph(document, "Evidencia", evidence_text)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run(f"IPAS QA    Run {general['run_id']}").font.size = Pt(8)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(output_path)


def build_html(data: dict, output_path: Path) -> None:
    e = lambda value: escape(str(value), quote=True)
    general = data["general"]
    summary = data["summary"]
    css = """
    :root{--navy:#10263a;--teal:#258477;--ink:#17212b;--line:#d9e0e6;--soft:#f3f6f8;--pass:#147a55;--fail:#b42318;--skip:#8a6116;--notrun:#59636e}
    *{box-sizing:border-box}body{margin:0;background:#eef2f5;color:var(--ink);font:15px/1.5 Segoe UI,Arial,sans-serif}.page{max-width:1100px;margin:28px auto;background:white;padding:48px 56px;box-shadow:0 12px 36px #10263a18}h1,h2,h3{color:#000;margin:0 0 14px}h1{font-size:34px;line-height:1.12}h2{font-size:23px;margin-top:34px}h3{font-size:18px;margin-top:24px}.lead{font-size:17px;color:#344454;max-width:850px}table{width:100%;border-collapse:collapse;margin:14px 0 22px}th,td{border:1px solid var(--line);padding:10px 12px;vertical-align:top}.meta th{width:19%;background:#edf3f6;text-align:left}.summary th,.cases th{background:var(--navy);color:white;text-align:left}.summary td{text-align:center;font-size:18px;font-weight:700}.status{display:inline-block;border-radius:999px;padding:3px 10px;font-size:12px;font-weight:800}.PASS{background:#dff4e9;color:var(--pass)}.FAIL{background:#fde7e5;color:var(--fail)}.SKIPPED{background:#fff3d6;color:var(--skip)}.NOT-RUN{background:#eceff2;color:var(--notrun)}.case{border-top:4px solid var(--teal);margin-top:38px;padding-top:20px}.label{font-weight:700;color:#344454}.data-table th,.steps th{background:#e9f0f5;text-align:left}.steps td:first-child{width:42px;text-align:center}.evidence{max-width:100%;border:1px solid var(--line);margin:8px 0 18px}.error{color:var(--fail);background:#fff5f4;padding:12px;border-left:4px solid var(--fail);white-space:pre-wrap}.footer{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);color:#607080;font-size:12px}@media print{body{background:white}.page{box-shadow:none;margin:0;max-width:none;padding:20mm}.case{break-before:page}.evidence{break-inside:avoid}}
    """
    parts = [
        "<!doctype html><html lang='es'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width,initial-scale=1'>",
        f"<title>Informe de automatización {e(general['suite'])}</title><style>{css}</style></head><body><main class='page'>",
        "<h1>Informe detallado de automatización IPAS</h1>",
        f"<p class='lead'>La corrida {e(general['run_id'])} terminó con estado <strong>{e(general['status'])}</strong>. Se ejecutaron {summary['total']} casos sobre el ambiente local QA, con {summary['pass']} PASS y {summary['fail']} FAIL.</p>",
        "<h2>Datos generales</h2><table class='meta'>",
        f"<tr><th>Proyecto</th><td>{e(general['project'])}</td><th>Ambiente</th><td>{e(general['environment'])}</td></tr>",
        f"<tr><th>Tipo</th><td>{e(general['type'])}</td><th>Suite</th><td>{e(general['suite'])}</td></tr>",
        f"<tr><th>Inicio</th><td>{e(general['started_at'])}</td><th>Fin</th><td>{e(general['finished_at'])}</td></tr>",
        f"<tr><th>Duración</th><td>{e(general['duration'])}</td><th>Correo</th><td>{e(general['email'])}</td></tr>",
        f"<tr><th>Run ID</th><td colspan='3'>{e(general['run_id'])}</td></tr></table>",
        "<h2>Resumen de resultados</h2><table class='summary'><tr><th>Total</th><th>PASS</th><th>FAIL</th><th>SKIPPED</th><th>NOT RUN</th><th>Éxito</th></tr>",
        f"<tr><td>{summary['total']}</td><td>{summary['pass']}</td><td>{summary['fail']}</td><td>{summary['skipped']}</td><td>{summary['not_run']}</td><td>{summary['success_rate']}%</td></tr></table>",
    ]
    performance = data.get("performance")
    if performance:
        profile = performance["profile"]
        criteria = performance["criteria"]
        aggregate = performance["aggregate"]
        parts.extend([
            "<h2>Métricas de rendimiento</h2>",
            f"<p><span class='label'>Perfil</span> {e(profile['users'])} usuarios, incremento {e(profile['spawn_rate'])} usuario/s, duración {e(profile['duration_seconds'])} segundos.</p>",
            f"<p><span class='label'>Criterio</span> p95 &lt; {e(criteria['p95_limit_ms'])} ms y errores &lt; {criteria['error_rate_limit'] * 100:.2f}%.</p>",
            "<table class='summary'><tr><th>Solicitudes</th><th>Req/s</th><th>Promedio</th><th>Mediana</th><th>p95</th><th>Mín</th><th>Máx</th><th>Errores</th></tr>",
            f"<tr><td>{e(aggregate.get('requests', 0))}</td><td>{e(aggregate.get('throughput_rps', 0))}</td><td>{e(aggregate.get('average_ms', 0))} ms</td><td>{e(aggregate.get('median_ms', 0))} ms</td><td>{e(aggregate.get('p95_ms', 0))} ms</td><td>{e(aggregate.get('min_ms', 0))} ms</td><td>{e(aggregate.get('max_ms', 0))} ms</td><td>{aggregate.get('error_rate', 0) * 100:.2f}%</td></tr></table>",
        ])
    parts.append("<table class='cases'><tr><th>ID</th><th>Nombre</th><th>Tipo y suite</th><th>Estado</th><th>Observación</th></tr>")
    for case in data["cases"]:
        status_class = case["status"].replace(" ", "-")
        parts.append(
            f"<tr><td>{e(case['id'])}</td><td>{e(case['name'])}</td><td>{e(case['type'])}<br>{e(case['module'])}</td><td><span class='status {e(status_class)}'>{e(case['status'])}</span></td><td>{e(case['observation'])}</td></tr>"
        )
    parts.append("</table><h2>Detalle por caso</h2>")
    for case in data["cases"]:
        status_class = case["status"].replace(" ", "-")
        parts.extend([
            "<section class='case'>",
            f"<h3>{e(case['id'])} {e(case['name'])}</h3>",
            f"<p><span class='label'>Prioridad</span> {e(case['priority'])} &nbsp; <span class='label'>Módulo</span> {e(case['module'])} &nbsp; <span class='label'>Estado</span> <span class='status {e(status_class)}'>{e(case['status'])}</span></p>",
            f"<p><span class='label'>Objetivo</span> {e(case['objective'])}</p>",
            "<p><span class='label'>Precondiciones</span></p><ul>",
        ])
        parts.extend(f"<li>{e(item)}</li>" for item in case["preconditions"])
        parts.append("</ul><p><span class='label'>Datos de prueba</span></p><table class='data-table'><tr><th>Dato</th><th>Valor</th><th>Origen</th><th>Observación</th></tr>")
        for item in case["data"]:
            parts.append(f"<tr><td>{e(item['name'])}</td><td>{e(item['value'])}</td><td>{e(item['source'])}</td><td>{e(item['observation'])}</td></tr>")
        parts.extend([
            "</table>",
            f"<p><span class='label'>Resultado esperado</span> {e(case['expected'])}</p>",
            "<table class='steps'><tr><th>#</th><th>Paso ejecutado</th><th>Resultado esperado</th><th>Resultado observado</th><th>Estado</th></tr>",
        ])
        for number, step in enumerate(case["steps"], 1):
            step_class = step["status"].replace(" ", "-")
            parts.append(f"<tr><td>{number}</td><td>{e(step['action'])}</td><td>{e(step['expected'])}</td><td>{e(step['observed'])}</td><td><span class='status {e(step_class)}'>{e(step['status'])}</span></td></tr>")
        parts.append("</table>")
        if case["status"] == "FAIL":
            defect = f"<br>Defecto relacionado: {e(case['defect'])}" if case.get("defect") else ""
            parts.append(f"<div class='error'><strong>Error y reproducción</strong> {e(case['observation'])}{defect}</div>")
        if case["images"]:
            for number, image in enumerate(case["images"], 1):
                parts.append(f"<p class='label'>Evidencia {number}</p><img class='evidence' src='data:image/png;base64,{image['base64']}' alt='Evidencia {e(case['id'])} {number}'>")
        else:
            evidence_text = (
                "Registro técnico en CSV de métricas, locust.log y result.json del run."
                if performance else
                "Registro técnico en JUnit, pytest.log y result.json del run."
            )
            parts.append(f"<p><span class='label'>Evidencia</span> {e(evidence_text)}</p>")
        parts.append("</section>")
    parts.append("<p class='footer'>Generado desde resultados reales de pytest. Los datos de prueba son ficticios y pertenecen exclusivamente a ius_puniendi_qa.</p></main></body></html>")
    output_path.write_text("".join(parts), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera DOCX y HTML autocontenido desde result.json")
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--email", default="")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output_dir = args.output_dir or args.result.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    data = load_report_data(args.result, args.email)
    docx_path = output_dir / "informe_detallado.docx"
    html_path = output_dir / "reporte_autocontenido.html"
    build_docx(data, docx_path)
    build_html(data, html_path)
    print(json.dumps({"docx": str(docx_path), "html": str(html_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

