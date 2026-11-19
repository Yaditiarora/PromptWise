"""
ALL TEAM-FILLED CONTENT FOR THE MILESTONE 2 PDF LIVES HERE.
Anything written as F("...") (shown in red in the PDF as [FILL: ...]) must be replaced by your REAL information.
Prompt text is NOT typed here: it is read from the prompts/ folder so the repo, app and PDF always match.
After editing, run:  python build_m2_pdf.py
"""
def F(hint):
    return f"[FILL: {hint}]"

# ---------------- Section 1: cover page ----------------
TEAM = dict(
    team_id=F("Team ID given after Milestone 1"),
    team_name="Cognivance",
    title="PromptWise: AI Study Assistant Using Prompt Engineering",
    batch=F("your batch group, e.g. B13-24"),
    faculty=F("faculty name"),
    members=[("S24CSEU0166", "Vanshika Beniwal (Team Leader)"),
             ("S24CSEU0241", "Yaditi Arora"),
             ("S24CSEU0340", "Mohita Purohit")],
)
LINKS = dict(
    prototype="https://promptwise-a7i9rzr9og3ef8hqi26nub.streamlit.app/",
    repo="https://github.com/Yaditiarora/PromptWise",
    reel=F("reel link (Drive / unlisted YouTube)"),
    reel_seconds=F("exact reel length in seconds (90-150)"),
)

# ---------------- Section 2(a): half to one page ----------------
SECTION2_TEXT = [
 ("Problem and users",
  "Students struggle to understand complex topics and to make short revision notes before exams. A general AI answer is often too long, "
  "too hard, or in the wrong format for the student's level. PromptWise is for school and college students (and teachers who need practice questions)."),
 ("Input and output",
  "Input: topic, academic level (School / Undergraduate / Postgraduate), task (Explain / Notes / Quiz / Exam answer), language (English or Hinglish), "
  "marks (2, 5 or 10) for exam answers, and the student's quiz answers. Output: a short explanation, revision notes, a 5-question quiz, an exam-style answer, "
  "or graded feedback with weak concepts and a short revision."),
 ("Number of prompts and why",
  "{n_prompts} prompts, one LLM call each. P1 is a system prompt (role, refusal of non-academic requests, accuracy and privacy rules) used in every call. "
  "P2 to P5 each produce one kind of study material with a fixed format, because one long prompt for everything gave uncontrolled length and structure. "
  "P6 grades the quiz answers, which closes a learn, test, fix loop."),
 ("Tool and model",
  "Gemini 3.5 Flash Lite through the Gemini API (Google AI Studio), called from a Streamlit web app. Gemini was chosen because it is available free in AI Studio "
  "and responds quickly; Streamlit lets us expose the prompt variables (topic, level, task, language) as simple inputs and share one link with evaluators."),
 ("What changed since Milestone 1",
  "Milestone 1 planned to compare ChatGPT and Gemini and keep a web app or no-code builder as options. We narrowed to one model (Gemini) and one coded app, "
  "split the single baseline prompt into six prompts with fixed formats, and added three features beyond the proposal: marks-based exam answers, a Hinglish option, "
  "and quiz answer checking with targeted revision."),
]

# ---------------- Section 2(c): prompt sheets (templates are read from prompts/final) ----------------
PROMPT_SHEETS = [
 dict(id="P1", name="System prompt", file="P1_system.txt", step="Applied to every call (steps 1 to 5)",
      purpose="Sets the role, refuses non-academic requests, enforces honesty and privacy.",
      variables=[], output="Not applicable (instruction only)", examples=0, is_system=True,
      sample_in=F("example user request this prompt shaped, e.g. 'Recommend a good movie'"),
      sample_out=F("actual output copied from the app")),
 dict(id="P2", name="Explain", file="P2_explain.txt", step="Step 2: generate explanation",
      purpose="Short, level-appropriate explanation with one example.",
      variables=[("topic", "study topic typed by the student"), ("level", "School, Undergraduate or Postgraduate"),
                 ("language_note", "empty for English, or the Hinglish instruction line")],
      output="Definition, simple explanation, real-life example, key takeaway; max 150 words", examples=0,
      sample_in=F("real input, e.g. Mealy and Moore machines / Undergraduate"), sample_out=F("actual output copied from the app")),
 dict(id="P3", name="Revision notes", file="P3_notes.txt", step="Step 2: generate notes",
      purpose="Concise revision notes for quick exam revision.",
      variables=[("topic", "study topic"), ("level", "academic level"), ("language_note", "empty or the Hinglish instruction line")],
      output="Max 10 bullets: key terms, important points, formulas/rules, memory tip", examples=0,
      sample_in=F("real input"), sample_out=F("actual output copied from the app")),
 dict(id="P4", name="Quiz", file="P4_quiz.txt", step="Step 2: generate quiz",
      purpose="Five practice questions without answers.",
      variables=[("topic", "study topic"), ("level", "academic level"), ("language_note", "empty or the Hinglish instruction line")],
      output="3 MCQs, 1 short answer, 1 application question, numbered, no answers", examples=0,
      sample_in=F("real input"), sample_out=F("actual output copied from the app")),
 dict(id="P5", name="Marks-based exam answer", file="P5_marks_answer.txt", step="Step 2: generate exam answer",
      purpose="Exam-style answer whose length and depth match the marks.",
      variables=[("topic", "study topic"), ("level", "academic level"), ("marks", "2, 5 or 10"),
                 ("language_note", "empty or the Hinglish instruction line")],
      output="2 marks: 2-3 lines; 5 marks: about 120 words; 10 marks: about 250 words with sections", examples=0,
      sample_in=F("real input"), sample_out=F("actual output copied from the app")),
 dict(id="P6", name="Quiz grading", file="P6_grading.txt", step="Step 3: check learning",
      purpose="Marks the student's quiz answers and gives targeted revision.",
      variables=[("topic", "quiz topic"), ("level", "academic level"), ("quiz", "full quiz text generated by P4"),
                 ("answers", "answers typed by the student"), ("language_note", "empty or the Hinglish instruction line")],
      output="Correct/incorrect per answer with reason, score out of 5, weak concepts, 5-line revision", examples=0,
      sample_in=F("real quiz answers typed"), sample_out=F("actual output copied from the app")),
]
TOOL_AND_SETTINGS = "Gemini 3.5 Flash Lite via Gemini API (Google AI Studio)", "default (temperature=0.7)"

# ---------------- Section 3: modules and iteration log ----------------
# Status must be exactly: Working / Partly working / Not started. Q20 lists only Working modules, same names.
MODULES = [
 ("Input form", "Takes topic, level, task, language, marks; warns on empty topic", F("Working / Partly working / Not started"), F("note")),
 ("Explain mode", "Generates a short explanation (P2)", F("status"), F("note")),
 ("Revision notes mode", "Generates concise notes (P3)", F("status"), F("note")),
 ("Practice quiz mode", "Generates a 5-question quiz (P4)", F("status"), F("note")),
 ("Marks-based exam answer", "Generates a 2/5/10-mark answer (P5)", F("status"), F("note")),
 ("Hinglish language option", "Switches outputs to Roman-script Hinglish", F("status"), F("note")),
 ("Quiz answer checking", "Grades typed answers and gives revision (P6)", F("status"), F("note")),
]
# Result column must say what you OBSERVED, with numbers (e.g. average word count over 3 runs, format followed x of 3).
ITERATION = [
 dict(v="v1", changed="First prompt (baseline from Milestone 1): explain the topic in simple language with examples",
      why="Starting point", result=F("what you observed, with numbers"), files=["v1/P_baseline.txt"]),
 dict(v="v2", changed="Added student level, a 150-word limit and one example",
      why="v1 length and difficulty were not controlled", result=F("what you observed, with numbers"), files=["v2/P_explain.txt"]),
 dict(v="v3", changed="Split into Explain, Notes and Quiz prompts, each with a fixed output format",
      why="Milestone 1 feedback asked for explanations, notes and exam practice questions", result=F("what you observed, with numbers"),
      files=["v3/explain.txt", "v3/notes.txt", "v3/quiz.txt"]),
 dict(v="v4", changed="Added system prompt (role, refuse non-academic input, admit uncertainty, no personal data)",
      why="Invalid input and possible wrong facts needed handling", result=F("what you observed, with numbers"),
      files=["v4/system.txt", "v4/explain.txt", "v4/notes.txt", "v4/quiz.txt"]),
 dict(v="v5 (final)", changed="Added marks-based answers (P5), grading prompt (P6) and the Hinglish option; prompts moved to files",
      why="Match exam needs and close the learn, test, fix loop", result=F("what you observed, with numbers"),
      files=["final/P1_system.txt", "final/P2_explain.txt", "final/P3_notes.txt", "final/P4_quiz.txt", "final/P5_marks_answer.txt", "final/P6_grading.txt"]),
]

# ---------------- Section 4: tests ----------------
# Type must be Normal, Edge or Invalid. Need >= 10 rows and >= 3 Edge. Record failures honestly.
TESTS = [
 (1, "Mealy and Moore machines / Undergraduate / Explain", "Normal", "Definition, explanation, example, takeaway; under 150 words"),
 (2, "Mealy and Moore machines / Undergraduate / Notes", "Normal", "Max 10 bullets with key terms and memory tip"),
 (3, "Mealy and Moore machines / Undergraduate / Quiz", "Normal", "5 questions (3 MCQ, 1 short, 1 application), no answers shown"),
 (4, "Photosynthesis / School / Explain", "Normal", "Simple school-level explanation with real-life example"),
 (5, "Operating systems / Undergraduate / Exam answer, 5 marks", "Normal", "About 120 words, heading and 4 points"),
 (6, "Photosynthesis / School / Explain / Hinglish", "Normal", "Roman-script Hinglish, technical terms in English"),
 (7, "Answers to the quiz from test 3: 1-B, 2-A, 3-C, short and application answers", "Normal", "Correct/incorrect per answer, score out of 5, weak concepts, 5-line revision"),
 (8, "Entropy (one word) / Undergraduate / Explain", "Edge", "Still a valid explanation; states which meaning it assumes"),
 (9, "Physics (very broad) / School / Notes", "Edge", "Overview notes within 10 bullets"),
 (10, "Quantum field theory / School / Explain", "Edge", "Simplified for school level, no heavy maths"),
 (11, "Quiz answers typed as: idk", "Edge", "Score 0, asks the student to try again"),
 (12, "Recommend a good movie / Undergraduate / Explain", "Invalid", "Polite refusal, asks for an academic topic"),
]
# Fill these with what REALLY happened, same length/order as TESTS: (actual_output_short, "Pass" or "Fail")
TEST_RESULTS = {n: (F("actual output, short"), F("Pass or Fail")) for n, *_ in TESTS}
# 2-3 screenshots of real runs: (test number, caption, file under test-data/screenshots/)
SCREENSHOTS = [
 (3, "Quiz generated for Mealy and Moore machines", "test3_quiz.png"),
 (7, "Quiz answers graded with weak concepts", "test7_grading.png"),
 (12, "Refusal of a non-academic request", "test12_invalid.png"),
]
LIMITATIONS = [
 ("The model can state wrong facts and PromptWise does not check them against a source.",
  "Add document grounding (the student's own notes or syllabus) and a confidence line at the end of each answer."),
 ("Quiz grading depends on free-text answers, so unusual answer formats may be graded wrongly.",
  "Use structured answer inputs (one box per question) instead of one text box."),
 ("Hinglish quality was checked only by the team, not by a wider group of users.",
  "Ask classmates to rate Hinglish outputs and adjust the instruction line."),
 ("Nothing is saved between sessions, so progress and weak concepts are lost on refresh.",
  "Keep a simple history of scores per topic."),
]

# ---------------- Section 5: repository ----------------
REPO_SCREENSHOT = "repo.png"
REPO_LINES = [
 "Milestone 1 had only a proposal and one baseline prompt; the repository now holds all prompt versions, the app code, test data and diagrams.",
 "prompts/ contains v1 to v4 and the six final prompts, one file per prompt; the app reads prompts/final/ directly.",
 "code/app.py is the Streamlit app; it was deployed on Streamlit Community Cloud with the API key stored in Secrets only.",
 "test-data/ holds the test inputs, saved outputs and screenshots; CHANGELOG.md lists dated changes since Milestone 1.",
]

# ---------------- Section 7: contribution (percentages must add up to 100) ----------------
CONTRIB = [
 ("Vanshika Beniwal", "S24CSEU0166", "Prompt design",
  "Wrote P1 to P6 and prompt versions v1 to v5; kept the iteration log", "prompts/ folder, prompts/final/P1 to P6", 34),
 ("Yaditi Arora", "S24CSEU0241", "App building and deployment",
  "Built the Streamlit app, connected the Gemini API, set up the repository and deployed it", "code/app.py, requirements.txt, deployed app link", 33),
 ("Mohita Purohit", "S24CSEU0340", "Testing, reel and documents",
  "Ran the 12 tests, saved outputs and screenshots, recorded the reel, wrote the synopsis", "test-data/, Section 4 of this PDF, reel link", 33),
]

# ---------------- Section 6: synopsis (also uploaded separately as Cognivance_Synopsis.pdf) ----------------
SYNOPSIS = dict(
 problem="Students often struggle to understand complex academic topics and to prepare concise revision notes before examinations. "
         "Generic AI responses can be too long, confusing, or unsuitable for the student's academic level, and the quality of an answer depends "
         "heavily on how the instruction is written. Students need a simple way to get clear explanations, concise summaries, and relevant practice questions.",
 objectives=["Design structured prompts that produce clear, level-appropriate study material from a topic, academic level and task type.",
             "Provide separate modes for explanation, revision notes, quiz and marks-based exam answers.",
             "Close the learning loop by grading quiz answers and giving targeted revision on weak concepts.",
             "Compare a baseline prompt with the structured prompts using the iteration log and a test table."],
 scope=["Users: school and college students preparing for examinations; teachers who need practice questions.",
        "Inputs: topic, academic level, task type, language (English or Hinglish), marks (2, 5, 10), and the student's quiz answers.",
        "Outputs: explanation, revision notes, 5-question quiz, exam-style answer, and graded feedback.",
        "Out of scope: model training, storing student data, and non-academic requests (refused by the system prompt). No personal data is collected."],
 method=["Baseline: a simple prompt (explain the topic in simple language with examples) is run first.",
         "Prompt design: role prompting (system prompt), fixed output formats, length limits, level targeting, a refusal rule and an accuracy rule. {n_prompts} prompts are used in the final solution.",
         "Iteration: {n_versions} prompt versions are recorded with the change, the reason and the observed result.",
         "Implementation: a Streamlit web app calls Gemini 4 Hydrogen through the Gemini API; code and prompts are kept in a public repository.",
         "Evaluation: a test table of {n_tests} inputs (normal, edge and invalid) records expected output, actual output and Pass/Fail."],
 outcome="A working web application, PromptWise, that gives students concise, level-appropriate study material and practice questions, with evidence "
         "(iteration log and test table) that structured prompts give more consistent and useful results than a basic prompt.",
 source="Problem source: self-defined, from observation of students' exam preparation needs. Reference: OpenAI Prompt Engineering Guide, "
        "https://platform.openai.com/docs/guides/prompt-engineering",
)
