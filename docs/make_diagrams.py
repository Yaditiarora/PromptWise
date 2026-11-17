"""Draws the 4 diagrams for Section 2 of the Milestone 2 PDF. Run: python make_diagrams.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BLUE, GREEN, ORANGE, GREY, PINK = "#dbe8f7", "#dcf2e0", "#fde8cf", "#ececec", "#f9dde3"

def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h)); ax.set_xlim(0, w); ax.set_ylim(-0.4, h); ax.axis("off"); return fig, ax

def box(ax, cx, cy, w, h, text, color=BLUE, fs=9, bold=False):
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=color, ec="#33415c", lw=1.2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal", wrap=True)
    return (cx, cy, w, h)

def arrow(ax, a, b, label="", side="r2l", fs=8):
    (x1, y1, w1, h1), (x2, y2, w2, h2) = a, b
    if side == "r2l": p, q = (x1+w1/2, y1), (x2-w2/2, y2)
    elif side == "b2t": p, q = (x1, y1-h1/2), (x2, y2+h2/2)
    elif side == "t2b": p, q = (x1, y1+h1/2), (x2, y2-h2/2)
    else: p, q = (x1-w1/2, y1), (x2+w2/2, y2)
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color="#33415c", lw=1.4))
    if label:
        if side in ("b2t", "t2b"): ax.text((p[0]+q[0])/2+0.12, (p[1]+q[1])/2, label, ha="left", va="center", fontsize=fs, color="#33415c")
        else: ax.text((p[0]+q[0])/2, (p[1]+q[1])/2+0.13, label, ha="center", fontsize=fs, color="#33415c")

def save(fig, name):
    fig.savefig(name, dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)

# 1. Prompt workflow
fig, ax = canvas(10, 5.6)
a = box(ax, 1.3, 4.6, 2.1, .9, "Student input\ntopic, level, task,\nlanguage, marks", GREY)
b = box(ax, 4.0, 4.6, 2.2, .9, "App check:\nis the topic empty?", ORANGE)
c = box(ax, 7.0, 4.6, 2.6, .9, "Pick prompt template\nP2 Explain / P3 Notes /\nP4 Quiz / P5 Marks answer")
d = box(ax, 7.0, 3.1, 2.6, .9, "Gemini 4 Hydrogen\nsystem prompt P1 +\nfilled template", GREEN, bold=True)
e = box(ax, 3.9, 3.1, 2.6, .9, "Show output\n(Explain / Notes / Quiz /\nExam answer)", BLUE)
f = box(ax, 3.9, 1.6, 2.6, .9, "Student types\nquiz answers", GREY)
g = box(ax, 7.0, 1.6, 2.6, .9, "P6 Grading prompt\n+ system prompt P1", GREEN, bold=True)
h = box(ax, 7.0, 0.35, 2.6, .8, "Score, weak concepts,\n5-line revision", BLUE)
arrow(ax, a, b); arrow(ax, b, c, "valid"); arrow(ax, c, d, side="t2b" if False else "b2t"); arrow(ax, d, e, side="l2r")
arrow(ax, e, f, "if Quiz", side="b2t"); arrow(ax, f, g); arrow(ax, g, h, side="b2t")
ax.text(4.0, 5.3, "else: show 'Please enter a topic'", ha="center", fontsize=7.5, color="#a33")
ax.set_title("Prompt workflow of PromptWise", fontsize=11, fontweight="bold"); save(fig, "diagrams/1_prompt_workflow.png")

# 2. Task decomposition
fig, ax = canvas(10, 4.6)
root = box(ax, 5, 4.0, 3.4, .8, "PromptWise: turn a topic into\nuseful study material", ORANGE, bold=True)
kids = [("1. Understand\nthe request", "topic, academic level,\ntask, language", 1.4),
        ("2. Generate\nstudy material", "P2 Explain, P3 Notes,\nP4 Quiz, P5 Marks answer", 3.8),
        ("3. Check\nlearning", "P6 grades quiz answers,\nlists weak concepts", 6.2),
        ("4. Stay safe\nand honest", "P1 system prompt: refuse\nnon-academic, admit doubt", 8.6)]
for t, sub, x in kids:
    k = box(ax, x, 2.4, 2.2, .9, t, BLUE, bold=True); s = box(ax, x, .9, 2.2, 1.0, sub, GREY, fs=8)
    arrow(ax, root, k, side="b2t"); arrow(ax, k, s, side="b2t")
ax.set_title("Task decomposition", fontsize=11, fontweight="bold"); save(fig, "diagrams/2_task_decomposition.png")

# 3. Input-output flow
fig, ax = canvas(11, 4.6)
ins = ["Topic (text)", "Academic level", "Task type", "Language (English / Hinglish)", "Marks (2 / 5 / 10)", "Student's quiz answers"]
outs = ["Explanation (max 150 words)", "Revision notes (max 10 bullets)", "Quiz (5 questions)", "Exam-style answer", "Score + weak concepts + revision"]
mid = box(ax, 5.5, 2.2, 2.4, 1.2, "Prompt builder\n+ Gemini 4 Hydrogen", GREEN, bold=True)
for i, t in enumerate(ins):
    y = 3.9 - i*0.7; bb = box(ax, 1.6, y, 2.8, .5, t, GREY, fs=8); arrow(ax, bb, mid)
for i, t in enumerate(outs):
    y = 3.8 - i*0.8; bb = box(ax, 9.3, y, 3.0, .55, t, BLUE, fs=8); arrow(ax, mid, bb)
ax.text(1.6, 4.4, "INPUTS", ha="center", fontweight="bold"); ax.text(9.3, 4.35, "OUTPUTS", ha="center", fontweight="bold")
ax.set_title("Input-output flow", fontsize=11, fontweight="bold", y=1.03); save(fig, "diagrams/3_input_output_flow.png")

# 4. System architecture
fig, ax = canvas(10, 4.6)
u = box(ax, 1.3, 3.4, 1.9, .9, "Student\n(web browser)", GREY)
app = box(ax, 4.6, 3.4, 2.8, 1.1, "Streamlit app\ncode/app.py\n(hosted on Streamlit Cloud)", BLUE, bold=True)
api = box(ax, 8.3, 3.4, 2.5, 1.0, "Gemini API\nGemini 4 Hydrogen", GREEN, bold=True)
gh = box(ax, 2.2, 1.0, 2.8, .9, "GitHub repository\n(code + prompts)", GREY)
pf = box(ax, 6.8, 1.0, 2.8, .9, "prompts/final/\nP1 to P6 text files", ORANGE)
ax.annotate("", xy=(app[0]-app[2]/2, 3.4), xytext=(u[0]+u[2]/2, 3.4), arrowprops=dict(arrowstyle="<|-|>", color="#33415c", lw=1.4))
ax.text(2.95, 3.53, "input / output", ha="center", fontsize=7.5, color="#33415c")
arrow(ax, app, api, "prompt, reply")
ax.annotate("", xy=(3.9, 2.85), xytext=(2.5, 1.45), arrowprops=dict(arrowstyle="-|>", color="#33415c", lw=1.4))
ax.text(2.7, 2.3, "deploy", fontsize=7.5, color="#33415c")
ax.annotate("", xy=(5.3, 2.85), xytext=(6.5, 1.45), arrowprops=dict(arrowstyle="-|>", color="#33415c", lw=1.4))
ax.text(6.3, 2.3, "loaded at start", fontsize=7.5, color="#33415c")
ax.text(8.3, 2.5, "API key kept in\nStreamlit Secrets", ha="center", fontsize=7.5, color="#a33")
ax.set_title("System architecture", fontsize=11, fontweight="bold"); save(fig, "diagrams/4_system_architecture.png")
print("diagrams done")
