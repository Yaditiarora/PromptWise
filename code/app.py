
from pathlib import Path
import time

import streamlit as st
from google import genai
from google.genai import types


# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="PromptWise",
    page_icon="📚",
    layout="centered"
)

# Primary model followed by fallback candidates.
# These must be supported by your API key.
MODELS = [
    "gemini-3.5-flash-lite"
]

PROMPT_DIR = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "final"
)


# ---------------- LOAD PROMPTS ----------------

def load(name):
    return (PROMPT_DIR / name).read_text(
        encoding="utf-8"
    ).strip()


SYSTEM_PROMPT = load("P1_system.txt")
EXPLAIN_PROMPT = load("P2_explain.txt")
NOTES_PROMPT = load("P3_notes.txt")
QUIZ_PROMPT = load("P4_quiz.txt")
MARKS_PROMPT = load("P5_marks_answer.txt")
GRADE_PROMPT = load("P6_grading.txt")


LANG_NOTE = {
    "English": "",
    "Hinglish": (
        "\nRespond in simple Hinglish (Roman script) "
        "and keep technical terms in English."
    ),
}


# ---------------- GEMINI CLIENT ----------------

try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options=types.HttpOptions(
            timeout=60000
        )
    )

except Exception as e:
    st.error(
        f"Gemini client initialization failed: {e}"
    )
    st.stop()


# ---------------- AI RESPONSE WITH MODEL FALLBACK ----------------

def ask(prompt):

    errors = []

    for model in MODELS:

        try:
            st.info(f"Connecting to {model}...")

            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
            )

            if response.text:
                st.success(
                    f"Generated successfully using {model}"
                )
                return response.text

            errors.append(
                f"{model}: Empty response"
            )

        except Exception as e:

            error_message = str(e).upper()

            errors.append(
                f"{model}: {e}"
            )

            retryable = any(
                code in error_message
                for code in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "500",
                    "502",
                    "504",
                    "404",
                    "NOT_FOUND"
                ]
            )

            if not retryable:
                raise

            st.warning(
                f"{model} is unavailable. "
                "Trying the next model..."
            )

            time.sleep(1)

    raise RuntimeError(
        "All available models failed. Details:\n"
        + "\n".join(errors)
    )


# ---------------- STREAMLIT APP ----------------

st.title("📚 PromptWise")

st.caption(
    "AI study assistant: it teaches, tests, and fixes your weak spots."
)


# ---------------- USER INPUTS ----------------

topic = st.text_input(
    "Topic",
    placeholder="e.g. Mealy and Moore machines"
)

level = st.selectbox(
    "Academic level",
    [
        "School",
        "Undergraduate",
        "Postgraduate"
    ]
)

task = st.selectbox(
    "Task",
    [
        "Explain",
        "Notes",
        "Quiz",
        "Exam answer (marks-based)"
    ]
)

language = st.selectbox(
    "Language",
    [
        "English",
        "Hinglish"
    ]
)

marks = None

if task.startswith("Exam"):
    marks = st.selectbox(
        "Marks",
        [2, 5, 10]
    )

note = LANG_NOTE[language]


# ---------------- GENERATE CONTENT ----------------

if st.button("Generate", type="primary"):

    if not topic.strip():

        st.warning(
            "Please enter a topic."
        )

    else:

        if task == "Explain":

            prompt = EXPLAIN_PROMPT.format(
                topic=topic,
                level=level,
                language_note=note
            )

        elif task == "Notes":

            prompt = NOTES_PROMPT.format(
                topic=topic,
                level=level,
                language_note=note
            )

        elif task == "Quiz":

            prompt = QUIZ_PROMPT.format(
                topic=topic,
                level=level,
                language_note=note
            )

        else:

            prompt = MARKS_PROMPT.format(
                topic=topic,
                level=level,
                marks=marks,
                language_note=note
            )

        try:

            with st.spinner(
                "Thinking... PromptWise is generating your content."
            ):

                output = ask(prompt)

            st.session_state["output"] = output

            if task == "Quiz":

                st.session_state["quiz"] = output
                st.session_state["quiz_topic"] = topic
                st.session_state["quiz_level"] = level

            else:

                for key in (
                    "quiz",
                    "quiz_topic",
                    "quiz_level"
                ):
                    st.session_state.pop(
                        key,
                        None
                    )

            st.success(
                "Content generated successfully!"
            )

        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )


# ---------------- DISPLAY LATEST OUTPUT ----------------

if "output" in st.session_state:

    st.divider()

    st.subheader(
        "Generated Content"
    )

    st.markdown(
        st.session_state["output"]
    )


# ---------------- QUIZ GRADING ----------------

if "quiz" in st.session_state:

    st.divider()

    st.subheader(
        "Submit your quiz answers"
    )

    answers = st.text_area(
        "Type your answers (e.g. 1-B, 2-A, 3-C, 4-..., 5-...)"
    )

    if st.button("Check my answers"):

        if not answers.strip():

            st.warning(
                "Please type your answers first."
            )

        else:

            try:

                with st.spinner(
                    "Checking your answers..."
                ):

                    result = ask(
                        GRADE_PROMPT.format(
                            topic=st.session_state["quiz_topic"],
                            level=st.session_state["quiz_level"],
                            quiz=st.session_state["quiz"],
                            answers=answers,
                            language_note=note
                        )
                    )

                st.success(
                    "Quiz checked successfully!"
                )

                st.subheader(
                    "Your Quiz Results"
                )

                st.markdown(result)

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )
