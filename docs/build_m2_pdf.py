"""Builds the Milestone 2 PDF (7 sections) and the synopsis PDF from m2_data.py. Run: python build_m2_pdf.py"""
import re, sys, textwrap
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
                                Preformatted, Image, KeepTogether)
import m2_data as D

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
SHOTS = ROOT / "test-data" / "screenshots"
DIAG = Path(__file__).resolve().parent / "diagrams"

n_prompts, n_tests, n_versions = len(D.PROMPT_SHEETS), len(D.TESTS), len(D.ITERATION)
fmt = dict(n_prompts=n_prompts, n_tests=n_tests, n_versions=n_versions)

# ---------- helpers ----------
UNI = {"\u2013": "-", "\u2014": "-", "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2022": "*",
       "\u2192": "->", "\u2713": "ok", "\u2264": "<=", "\u2265": ">=", "\u00d7": "x", "\u2026": "..."}
def clean(s):
    for k, v in UNI.items(): s = s.replace(k, v)
    return s.encode("latin-1", "replace").decode("latin-1")

FILLS = []
def rich(text):
    text = clean(str(text)); FILLS.extend(re.findall(r"\[FILL:[^\]]*\]", text))
    t = escape(text).replace("\n", "<br/>")
    return re.sub(r"(\[FILL:[^\]]*\])", r'<font color="#c00000"><b>\1</b></font>', t)

ss = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=ss["Normal"], fontSize=9.5, leading=13)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8, leading=10)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8, leading=10)
H1 = ParagraphStyle("h1", parent=ss["Heading1"], fontSize=15, textColor=colors.HexColor("#1f3a5f"), spaceAfter=6)
H2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=11.5, textColor=colors.HexColor("#1f3a5f"), spaceBefore=8, spaceAfter=3)
H3 = ParagraphStyle("h3", parent=ss["Heading3"], fontSize=10, spaceBefore=6, spaceAfter=2)
TITLE = ParagraphStyle("title", parent=ss["Title"], fontSize=21, leading=26)
CAP = ParagraphStyle("cap", parent=SMALL, alignment=1, textColor=colors.HexColor("#444444"))
BUL = ParagraphStyle("bul", parent=BODY, leftIndent=12)
CODE = ParagraphStyle("code", fontName="Courier", fontSize=7.3, leading=9, backColor=colors.HexColor("#f3f5f8"),
                      borderPadding=4, leftIndent=2, rightIndent=2)

def P(t, st=BODY): return Paragraph(rich(t), st)
def BL(t, st=None): return Paragraph("<b>%s</b>" % escape(clean(str(t))), st or CELL)
def bullets(items): return [Paragraph(rich(i), BUL, bulletText="\u2022") for i in items]
def code(text):
    lines = []
    for ln in clean(text).rstrip().split("\n"):
        lines += textwrap.wrap(ln, 100, break_long_words=True, replace_whitespace=False) or [""]
    FILLS.extend(re.findall(r"\[FILL:[^\]]*\]", "\n".join(lines)))
    return Preformatted("\n".join(lines), CODE)
def grid(data, widths, header=True, font=8):
    t = Table(data, colWidths=[w*cm for w in widths], repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    if header: st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbe8f7")))
    t.setStyle(TableStyle(st)); return t
def hdr(*c): return [Paragraph("<b>%s</b>" % escape(x), CELL) for x in c]
def img(path, maxw=16.5, maxh=11):
    from PIL import Image as PI
    w, h = PI.open(path).size; r = min(maxw*cm/w, maxh*cm/h); return Image(str(path), w*r, h*r)
def shot(path, caption, maxh=8):
    if Path(path).exists(): return KeepTogether([img(path, 15, maxh), Paragraph(rich(caption), CAP)])
    return KeepTogether([grid([[P(f"[FILL: add screenshot file {Path(path).name} in test-data/screenshots/]", SMALL)]], [16]),
                         Paragraph(rich(caption), CAP)])
def read_prompt(rel): return (PROMPTS / rel).read_text(encoding="utf-8").strip()

# ---------- synopsis (used in Section 6 AND as the separate PDF) ----------
def synopsis_flow():
    S = D.SYNOPSIS; T = D.TEAM; tool, _ = D.TOOL_AND_SETTINGS
    f = []
    f.append(Paragraph(rich(T["title"]), ParagraphStyle("t2", parent=TITLE, fontSize=16, leading=20)))
    f.append(Paragraph(rich("Synopsis | Team %s | SCSE4041 Prompt Engineering Milestone 2" % T["team_name"]), CAP))
    f.append(Spacer(1, 5))
    f.append(grid([[BL("Team"), P(T["team_name"], CELL)],
                   [BL("Members"), P("; ".join(f"{n} ({e})" for e, n in T["members"]), CELL)],
                   [BL("Tool / model"), P(tool + ", Streamlit web app", CELL)]], [3, 14], header=False))
    for head, key in [("1. Problem statement", "problem")]:
        f += [Paragraph(head, H2), P(S[key])]
    f += [Paragraph("2. Objectives", H2)] + bullets(S["objectives"])
    f += [Paragraph("3. Scope", H2)] + bullets(S["scope"])
    f += [Paragraph("4. Methodology", H2)] + bullets([m.format(**fmt) for m in S["method"]])
    f += [Paragraph("5. Expected outcome", H2), P(S["outcome"])]
    f += [Paragraph("6. Source", H2), P(S["source"])]
    return f

# ---------- page footer ----------
def footer(c, d):
    c.saveState(); c.setFont("Helvetica", 7.5); c.setFillColor(colors.grey)
    c.drawString(1.8*cm, 1.0*cm, clean(f"{D.TEAM['team_name']} | {D.TEAM['title']}"))
    c.drawRightString(A4[0]-1.8*cm, 1.0*cm, f"Page {d.page}"); c.restoreState()

def new_doc(path, title):
    return SimpleDocTemplate(str(path), pagesize=A4, leftMargin=1.8*cm, rightMargin=1.8*cm, topMargin=1.6*cm,
                             bottomMargin=1.8*cm, title=clean(title), author=D.TEAM["team_name"])

# ---------- Milestone 2 PDF ----------
def build_m2():
    T, L = D.TEAM, D.LINKS; tool, settings = D.TOOL_AND_SETTINGS
    s = []
    # 1 Cover
    s += [Spacer(1, 1.2*cm), Paragraph(rich(T["title"]), TITLE),
          Paragraph("SCSE4041 Prompt Engineering | Mini Project | Milestone 2", CAP), Spacer(1, 0.5*cm),
          Paragraph("1. Cover page", H1)]
    rows = [["Team ID", T["team_id"]], ["Team name", T["team_name"]], ["Project title", T["title"]],
            ["Batch", T["batch"]], ["Faculty name", T["faculty"]]]
    rows += [[("Member %d" % (i+1)), f"{e} - {n}"] for i, (e, n) in enumerate(T["members"])]
    rows += [["Prototype link", L["prototype"]], ["Repository link", L["repo"]], ["Reel link", L["reel"]],
             ["Reel length (seconds)", L["reel_seconds"]]]
    s.append(grid([[BL(a), P(b, CELL)] for a, b in rows], [4.2, 13], header=False))
    s += [Spacer(1, 0.4*cm), Paragraph("Numbers used in the submission form", H3),
          grid([hdr("Final prompts (Q10)", "Test inputs (Q17)", "Prompt versions (Q18)"),
                [P(str(n_prompts), CELL), P(str(n_tests), CELL), P(str(n_versions), CELL)]], [5.7, 5.7, 5.8])]
    s.append(PageBreak())

    # 2 Prompt and solution design
    s.append(Paragraph("2. Prompt and solution design", H1))
    s.append(Paragraph("(a) Overview", H2))
    for h, t in D.SECTION2_TEXT:
        s.append(Paragraph("<b>%s.</b> %s" % (escape(h), rich(t.format(**fmt))), BODY)); s.append(Spacer(1, 3))
    s.append(Paragraph("(b) Diagrams", H2))
    for i, (f, c) in enumerate([("1_prompt_workflow.png", "Figure 1: Prompt workflow"), ("2_task_decomposition.png", "Figure 2: Task decomposition"),
                                ("3_input_output_flow.png", "Figure 3: Input-output flow"), ("4_system_architecture.png", "Figure 4: System architecture (app)")]):
        s.append(KeepTogether([img(DIAG / f, 16, 9.5), Paragraph(c, CAP), Spacer(1, 6)]))
    s.append(Paragraph("(c) Prompt sheets", H2))
    sys_text = read_prompt("final/" + D.PROMPT_SHEETS[0]["file"])
    for p in D.PROMPT_SHEETS:
        tmpl = read_prompt("final/" + p["file"])
        vars_txt = "\n".join(f"{{{k}}}: {v}" for k, v in p["variables"]) or "none"
        info = [["Prompt ID and name", f"{p['id']} - {p['name']}"], ["Step in the workflow", p["step"]], ["Purpose", p["purpose"]],
                ["Tool and model", tool], ["Settings", settings], ["Number of examples included", str(p["examples"])],
                ["Output format", p["output"]], ["What each variable holds", vars_txt]]
        block = [Paragraph(f"{p['id']} - {p['name']}", H3),
                 grid([[BL(a), P(b, CELL)] for a, b in info], [4.6, 12.6], header=False),
                 Paragraph("<b>Full system prompt</b>" if not p.get("is_system", False) else "<b>Full system prompt (this prompt)</b>", SMALL),
                 code(sys_text if not p.get("is_system", False) else tmpl)]
        if not p.get("is_system", False):
            block += [Paragraph("<b>Full user prompt template</b>", SMALL), code(tmpl)]
        else:
            block += [Paragraph("<b>Full user prompt template</b>: none (sent as the system instruction with every call)", SMALL)]
        block += [Paragraph("<b>Sample run (real input and actual output)</b>", SMALL),
                  Paragraph("Input: " + rich(p["sample_in"]), CELL), code("Output:\n" + p["sample_out"]), Spacer(1, 6)]
        s += block
    s.append(PageBreak())

    # 3 Implementation
    s.append(Paragraph("3. Implementation", H1))
    s.append(P("PromptWise is a Streamlit web app (code/app.py). The student enters a topic, level, task and language; the app fills the matching prompt template "
               "from prompts/final/, sends it with the system prompt P1 to Gemini 4 Hydrogen, and shows the reply. After a quiz, the student's answers and the quiz are sent with P6 for grading."))
    s.append(Paragraph("Module status", H2))
    s.append(grid([hdr("Module", "What it does", "Status", "Notes")] +
                  [[P(a, CELL), P(b, CELL), P(c, CELL), P(d, CELL)] for a, b, c, d in D.MODULES], [3.6, 6.2, 3.0, 4.4]))
    s.append(Paragraph("Prompt iteration log (%d versions)" % n_versions, H2))
    s.append(grid([hdr("Version", "What changed", "Why it was changed", "Result after the change")] +
                  [[P(i["v"], CELL), P(i["changed"], CELL), P(i["why"], CELL), P(i["result"], CELL)] for i in D.ITERATION], [1.9, 5.3, 4.2, 5.8]))
    s.append(Paragraph("Full text of each version", H2))
    for i in D.ITERATION:
        s.append(Paragraph(i["v"], H3))
        for rel in i["files"]:
            s += [Paragraph("File: prompts/" + rel, SMALL), code(read_prompt(rel)), Spacer(1, 3)]
    s.append(PageBreak())

    # 4 Demonstration and testing
    s.append(Paragraph("4. Demonstration and testing", H1))
    s.append(Paragraph("Test table (%d inputs)" % n_tests, H2))
    rows = [hdr("Test no.", "Input (short)", "Type", "Expected output", "Actual output (short)", "Pass / Fail")]
    for n, inp, typ, exp in D.TESTS:
        act, res = D.TEST_RESULTS[n]
        rows.append([P(str(n), CELL), P(inp, CELL), P(typ, CELL), P(exp, CELL), P(act, CELL), P(res, CELL)])
    s.append(grid(rows, [1.2, 4.3, 1.4, 4.0, 4.6, 1.7]))
    s.append(Paragraph("Screenshots of real runs", H2))
    for n, cap, fn in D.SCREENSHOTS: s += [shot(SHOTS / fn, f"Test {n}: {cap}"), Spacer(1, 6)]
    s.append(Paragraph("Known limitations and next steps", H2))
    s.append(grid([hdr("Limitation", "What we will try next")] + [[P(a, CELL), P(b, CELL)] for a, b in D.LIMITATIONS], [8.6, 8.6]))
    s.append(PageBreak())

    # 5 Repository
    s.append(Paragraph("5. Repository", H1))
    s.append(P("Repository / folder link: " + L["repo"]))
    s.append(Spacer(1, 4)); s.append(shot(SHOTS / D.REPO_SCREENSHOT, "Screenshot of the repository or project folder", maxh=9))
    s.append(Paragraph("What changed since Milestone 1", H2)); s += bullets(D.REPO_LINES)
    s.append(PageBreak())

    # 6 Supporting document
    s.append(Paragraph("6. Supporting document", H1))
    s.append(P("Document type: Synopsis (also uploaded as a separate PDF named %s_Synopsis.pdf)." % T["team_name"], SMALL)); s.append(Spacer(1, 4))
    s += synopsis_flow()
    s.append(PageBreak())

    # 7 Contribution
    s.append(Paragraph("7. Team contribution", H1))
    s.append(grid([hdr("Member name", "Enrollment no.", "Role", "Tasks done in Milestone 2", "Evidence", "Contribution (%)")] +
                  [[P(a, CELL), P(b, CELL), P(c, CELL), P(d, CELL), P(e, CELL), P(str(f), CELL)] for a, b, c, d, e, f in D.CONTRIB],
                  [2.5, 2.3, 2.2, 4.4, 3.6, 2.2]))
    s.append(Spacer(1, 6)); s.append(P("Total: %d%%. All members agree with this table." % sum(c[5] for c in D.CONTRIB), SMALL))

    doc = new_doc(OUT_M2, f"Milestone 2 - {T['title']}"); doc.build(s, onFirstPage=footer, onLaterPages=footer)

def build_syn():
    doc = new_doc(OUT_SYN, "Synopsis - " + D.TEAM["title"]); doc.build(synopsis_flow(), onFirstPage=footer, onLaterPages=footer)

# ---------- checks ----------
def check():
    problems = []
    if n_tests < 10: problems.append(f"Need at least 10 test inputs (have {n_tests})")
    if sum(1 for t in D.TESTS if t[2] == "Edge") < 3: problems.append("Need at least 3 Edge tests")
    if any(t[2] not in ("Normal", "Edge", "Invalid") for t in D.TESTS): problems.append("Test type must be Normal, Edge or Invalid")
    if n_versions < 3: problems.append("Need at least 3 prompt versions")
    if sum(c[5] for c in D.CONTRIB) != 100: problems.append("Contribution percentages must add up to 100")
    ids = [p["id"] for p in D.PROMPT_SHEETS]
    if len(set(ids)) != len(ids): problems.append("Duplicate prompt IDs")
    return problems

if __name__ == "__main__":
    tid = re.sub(r"[^A-Za-z0-9]", "", D.TEAM["team_id"]) if "[FILL" not in D.TEAM["team_id"] else "TEAMID"
    ptitle = "PromptWise"
    OUT_M2 = Path(__file__).resolve().parent / f"M2_{tid}_{ptitle}.pdf"
    OUT_SYN = Path(__file__).resolve().parent / f"{D.TEAM['team_name']}_Synopsis.pdf"
    build_m2(); build_syn()
    uniq = sorted(set(FILLS))
    print(f"Built: {OUT_M2.name}, {OUT_SYN.name}")
    print(f"Form numbers -> Q10 prompts: {n_prompts} | Q17 test inputs: {n_tests} | Q18 prompt versions: {n_versions}")
    for p in check(): print("PROBLEM:", p)
    print(f"Items still to fill (red in the PDF): {len(uniq)}")
    if "--list" in sys.argv:
        for u in uniq: print("  ", u)
