"""
Study Assistant view for PromptWise.
Supports 5 interactive study modes (Explain, Summarize, Quiz, Flashcards, Practice Test)
plus preserves original marks-based exam answers and bilingual English/Hinglish options.
"""

import json
import random
import time
from typing import Any, Dict, List

import streamlit as st
from prompts.templates import (
    DIFFICULTY_GUIDELINES,
    ENHANCED_EXPLAIN_PROMPT,
    ENHANCED_SUMMARIZE_PROMPT,
    LANG_NOTE,
    MARKS_PROMPT,
    STRUCTURED_FLASHCARDS_PROMPT,
    STRUCTURED_QUIZ_PROMPT,
    STRUCTURED_TEST_PROMPT,
    TEST_EVALUATION_PROMPT,
)
from services import db_service
from services.gemini_service import call_gemini, parse_json_response
from ui.components import render_hero


def render_study_assistant():
    """Main rendering function for Study Assistant."""
    render_hero(
        title="🎓 Study Assistant",
        subtitle="Adaptive learning across 5 specialized modes tailored to your academic level.",
        badge_text="Interactive Learning Hub",
    )

    # ---------------- USER CONTROLS ----------------
    col_input1, col_input2 = st.columns([3, 2])

    with col_input1:
        topic = st.text_input(
            "Study Topic or Concept",
            value=st.session_state.get("current_topic", ""),
            placeholder="e.g. Photosynthesis, Binary Search Trees, Mealy and Moore machines...",
            help="Enter the exact academic subject or concept you want to study.",
            key="sa_topic_input",
        )

    with col_input2:
        # Preselect mode if coming from dashboard
        default_mode = st.session_state.get("active_study_mode", "Explain")
        modes_list = [
            "Explain",
            "Summarize",
            "Quiz",
            "Flashcards",
            "Test",
            "Exam Answer (Marks-based)",
        ]
        default_idx = modes_list.index(default_mode) if default_mode in modes_list else 0

        mode = st.selectbox(
            "Study Mode",
            modes_list,
            index=default_idx,
            key="sa_mode_select",
        )

    # Secondary options
    col_opt1, col_opt2, col_opt3 = st.columns(3)

    with col_opt1:
        difficulty = st.selectbox(
            "Difficulty Level",
            ["Beginner", "Intermediate", "Advanced"],
            index=1,
            help="Beginner: Simple language & intuitive examples | Intermediate: In-depth concepts | Advanced: Technical depth & edge cases",
            key="sa_difficulty_select",
        )

    with col_opt2:
        language = st.selectbox(
            "Language",
            ["English", "Hinglish"],
            help="Choose between standard academic English or conversational Hinglish.",
            key="sa_language_select",
        )

    marks = None
    num_questions = 5

    with col_opt3:
        if mode == "Exam Answer (Marks-based)":
            marks = st.selectbox("Exam Marks Weight", [2, 5, 10], index=1)
        elif mode == "Test":
            num_questions = st.selectbox("Question Count", [5, 8, 10], index=0)
        else:
            st.info(f"Target: {difficulty} depth")

    # Sync state
    st.session_state["current_topic"] = topic
    st.session_state["current_difficulty"] = difficulty
    st.session_state["current_mode"] = mode

    lang_instruction = LANG_NOTE.get(language, "")
    diff_instruction = DIFFICULTY_GUIDELINES.get(difficulty, "")

    # Generate Button
    generate_col, _ = st.columns([2, 5])
    with generate_col:
        trigger_generate = st.button(
            "⚡ Generate Study Material",
            type="primary",
            use_container_width=True,
            key="sa_generate_btn",
        )

    # ---------------- GENERATION LOGIC ----------------
    if trigger_generate:
        if not topic.strip():
            st.warning("⚠️ Please provide a study topic before generating.")
            return

        # Clear previous mode outputs when regenerating
        cache_key = f"content_{mode}"
        st.session_state.pop(cache_key, None)

        with st.spinner(f"✨ PromptWise is crafting your {difficulty}-level {mode} material with Gemini..."):
            try:
                if mode == "Explain":
                    prompt = ENHANCED_EXPLAIN_PROMPT.format(
                        topic=topic,
                        difficulty_guideline=diff_instruction,
                        language_note=lang_instruction,
                    )
                    content = call_gemini(prompt)
                    st.session_state["content_Explain"] = content
                    db_service.add_history(
                        topic=topic,
                        study_mode="Explain",
                        difficulty=difficulty,
                        original_prompt=f"Explain {topic} ({difficulty})",
                        optimized_prompt=prompt,
                        generated_response=content,
                    )

                elif mode == "Summarize":
                    prompt = ENHANCED_SUMMARIZE_PROMPT.format(
                        topic=topic,
                        difficulty_guideline=diff_instruction,
                        language_note=lang_instruction,
                    )
                    content = call_gemini(prompt)
                    st.session_state["content_Summarize"] = content
                    db_service.add_history(
                        topic=topic,
                        study_mode="Summarize",
                        difficulty=difficulty,
                        original_prompt=f"Summarize {topic} ({difficulty})",
                        optimized_prompt=prompt,
                        generated_response=content,
                    )

                elif mode == "Quiz":
                    prompt = STRUCTURED_QUIZ_PROMPT.format(
                        topic=topic,
                        difficulty=difficulty,
                        difficulty_guideline=diff_instruction,
                        language_note=lang_instruction,
                    )
                    raw_content = call_gemini(prompt, response_mime_type="application/json")
                    parsed_quiz = parse_json_response(raw_content)
                    st.session_state["content_Quiz"] = parsed_quiz
                    st.session_state["quiz_user_answers"] = {}
                    st.session_state["quiz_submitted"] = False
                    db_service.add_history(
                        topic=topic,
                        study_mode="Quiz",
                        difficulty=difficulty,
                        original_prompt=f"Quiz on {topic} ({difficulty})",
                        optimized_prompt=prompt,
                        generated_response=json.dumps(parsed_quiz, ensure_ascii=False),
                    )

                elif mode == "Flashcards":
                    prompt = STRUCTURED_FLASHCARDS_PROMPT.format(
                        topic=topic,
                        difficulty=difficulty,
                        difficulty_guideline=diff_instruction,
                        language_note=lang_instruction,
                    )
                    raw_content = call_gemini(prompt, response_mime_type="application/json")
                    parsed_cards = parse_json_response(raw_content)
                    cards = parsed_cards.get("flashcards", [])
                    st.session_state["content_Flashcards"] = cards
                    st.session_state["flashcard_index"] = 0
                    st.session_state["flashcard_flipped"] = False
                    st.session_state["flashcard_status"] = {}  # id -> "known" | "needs_revision"
                    db_service.add_history(
                        topic=topic,
                        study_mode="Flashcards",
                        difficulty=difficulty,
                        original_prompt=f"Flashcards on {topic} ({difficulty})",
                        optimized_prompt=prompt,
                        generated_response=json.dumps(parsed_cards, ensure_ascii=False),
                    )

                elif mode == "Test":
                    suggested_time = num_questions * 2  # 2 mins per question
                    prompt = STRUCTURED_TEST_PROMPT.format(
                        topic=topic,
                        num_questions=num_questions,
                        suggested_time=suggested_time,
                        difficulty=difficulty,
                        difficulty_guideline=diff_instruction,
                        language_note=lang_instruction,
                    )
                    raw_content = call_gemini(prompt, response_mime_type="application/json")
                    parsed_test = parse_json_response(raw_content)
                    st.session_state["content_Test"] = parsed_test
                    st.session_state["test_user_answers"] = {}
                    st.session_state["test_start_time"] = time.time()
                    st.session_state["test_submitted"] = False
                    st.session_state["test_evaluation"] = None
                    db_service.add_history(
                        topic=topic,
                        study_mode="Test",
                        difficulty=difficulty,
                        original_prompt=f"Test on {topic} ({difficulty}, {num_questions} questions)",
                        optimized_prompt=prompt,
                        generated_response=json.dumps(parsed_test, ensure_ascii=False),
                    )

                elif mode == "Exam Answer (Marks-based)":
                    prompt = MARKS_PROMPT.format(
                        topic=topic,
                        level=difficulty,
                        marks=marks,
                        language_note=lang_instruction,
                    )
                    content = call_gemini(prompt)
                    st.session_state["content_Exam"] = content
                    db_service.add_history(
                        topic=topic,
                        study_mode="Exam Answer",
                        difficulty=difficulty,
                        original_prompt=f"{marks}-mark exam answer for {topic}",
                        optimized_prompt=prompt,
                        generated_response=content,
                    )

                active_model = st.session_state.get("last_active_model", "gemini-3.5-flash-lite")
                used_fb = st.session_state.get("used_fallback", False)
                fb_suffix = " (Fallback Model)" if used_fb else " (Primary Model)"
                st.success(f"✅ Generated via `{active_model}`{fb_suffix} and saved to your history successfully!")

            except Exception as e:
                st.error(f"❌ Generation failed: {str(e)}")

    st.markdown("<hr style='border-color: rgba(139, 92, 246, 0.2); margin: 24px 0;'>", unsafe_allow_html=True)

    # ---------------- DISPLAY CONTENT BY MODE ----------------
    if mode == "Explain" and "content_Explain" in st.session_state:
        st.markdown(st.session_state["content_Explain"])

    elif mode == "Summarize" and "content_Summarize" in st.session_state:
        st.markdown(st.session_state["content_Summarize"])

    elif mode == "Exam Answer (Marks-based)" and "content_Exam" in st.session_state:
        st.subheader(f"📝 {marks}-Mark Model Exam Answer")
        st.markdown(st.session_state["content_Exam"])

    elif mode == "Quiz" and "content_Quiz" in st.session_state:
        render_interactive_quiz(st.session_state["content_Quiz"])

    elif mode == "Flashcards" and "content_Flashcards" in st.session_state:
        render_interactive_flashcards(st.session_state["content_Flashcards"])

    elif mode == "Test" and "content_Test" in st.session_state:
        render_practice_test(st.session_state["content_Test"], topic, difficulty)


# ---------------- SUB-COMPONENTS FOR INTERACTIVE MODES ----------------

def render_interactive_quiz(quiz_data: Dict[str, Any]):
    """Render interactive quiz questions with immediate grading and scoring."""
    st.subheader(f"❓ Interactive Quiz: {quiz_data.get('topic', 'Study Quiz')}")
    questions = quiz_data.get("questions", [])

    if not questions:
        st.warning("No questions found in this quiz.")
        return

    submitted = st.session_state.get("quiz_submitted", False)
    user_answers = st.session_state.setdefault("quiz_user_answers", {})

    for idx, q in enumerate(questions):
        qid = q.get("id", idx + 1)
        q_text = q.get("question", "")
        options = q.get("options", {})
        correct = (q.get("correct_answer") or q.get("answer") or q.get("correct_option") or q.get("correct") or "").strip().upper()
        explanation = q.get("explanation", "")

        st.markdown(f"**Question {idx + 1}:** {q_text}")

        # Build options list
        opt_keys = ["A", "B", "C", "D"]
        opt_labels = [f"{k}. {options.get(k, '')}" for k in opt_keys if k in options]

        if not submitted:
            current_choice = user_answers.get(qid, None)
            choice_idx = None
            if current_choice:
                for o_idx, k in enumerate(opt_keys):
                    if k == current_choice:
                        choice_idx = o_idx
                        break

            selected = st.radio(
                f"Choose an option for Question {idx + 1}:",
                options=opt_labels,
                index=choice_idx,
                key=f"quiz_radio_{qid}",
                label_visibility="collapsed",
            )
            if selected:
                letter = selected.split(".")[0].strip()
                user_answers[qid] = letter
        else:
            # Result view
            user_choice = user_answers.get(qid, "None")
            is_correct = (user_choice == correct)

            if is_correct:
                st.success(f"✅ **Your Answer:** {user_choice} (Correct!)")
            else:
                st.error(f"❌ **Your Answer:** {user_choice} | **Correct Answer:** {correct}")

            st.info(f"💡 **Explanation:** {explanation}")

        st.markdown("<br>", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([2, 5])
    with col_btn1:
        if not submitted:
            if st.button("📝 Submit Quiz Answers", type="primary", use_container_width=True):
                st.session_state["quiz_submitted"] = True
                st.rerun()
        else:
            if st.button("🔄 Retake Quiz", use_container_width=True):
                st.session_state["quiz_submitted"] = False
                st.session_state["quiz_user_answers"] = {}
                st.rerun()

    if submitted:
        # Calculate final score
        correct_count = sum(
            1 for q in questions
            if user_answers.get(q.get("id", 0)) == (q.get("correct_answer") or q.get("answer") or q.get("correct_option") or q.get("correct") or "").strip().upper()
        )
        total = len(questions)
        pct = (correct_count / total) * 100

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="pw-card" style="text-align: center; padding: 24px;">
                <div style="font-size: 1.1rem; color: #a5b4fc; font-weight: 600;">FINAL QUIZ SCORE</div>
                <div style="font-size: 3rem; font-weight: 800; color: #ffffff; margin: 8px 0;">
                    {correct_count} / {total}
                </div>
                <div style="font-size: 1.2rem; font-weight: 700; color: {'#10b981' if pct >= 70 else '#f59e0b'};">
                    {pct:.0f}% Mastery
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_interactive_flashcards(cards: List[Dict[str, Any]]):
    """Render interactive question/answer flashcards with 3D-like flip, navigation, and mastery status."""
    st.subheader("🗂️ Interactive Study Flashcards")

    if not cards:
        st.warning("No flashcards found.")
        return

    total = len(cards)
    current_idx = st.session_state.get("flashcard_index", 0)
    if current_idx >= total:
        current_idx = 0
        st.session_state["flashcard_index"] = 0

    card = cards[current_idx]
    card_id = card.get("id", current_idx + 1)
    is_flipped = st.session_state.get("flashcard_flipped", False)
    status_map = st.session_state.setdefault("flashcard_status", {})

    # Progress bar and status indicator
    st.progress((current_idx + 1) / total)
    p_col1, p_col2 = st.columns([3, 1])
    with p_col1:
        st.caption(f"Card {current_idx + 1} of {total} • Category: {card.get('category', 'Concept')}")
    with p_col2:
        known_count = sum(1 for v in status_map.values() if v == "known")
        st.caption(f"⭐ Mastered: {known_count}/{total}")

    # Display Card
    card_face_text = card.get("back" if is_flipped else "front", "")
    card_label = "REVEALED ANSWER / EXPLANATION" if is_flipped else "QUESTION / CONCEPT"
    tag_bg = "rgba(16, 185, 129, 0.2)" if is_flipped else "rgba(139, 92, 246, 0.2)"
    tag_color = "#34d399" if is_flipped else "#c4b5fd"

    st.markdown(
        f"""
        <div class="pw-flashcard">
            <span class="pw-flashcard-tag" style="background: {tag_bg}; color: {tag_color};">
                {card_label}
            </span>
            <div class="pw-flashcard-text">
                {card_face_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Flip Button
    f_col1, f_col2, f_col3 = st.columns([1, 2, 1])
    with f_col2:
        flip_btn_text = "🔄 Flip to Question" if is_flipped else "🔍 Flip to Reveal Answer"
        if st.button(flip_btn_text, use_container_width=True, key="flip_btn"):
            st.session_state["flashcard_flipped"] = not is_flipped
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation & Mastery Controls
    c_prev, c_mark_rev, c_mark_know, c_next, c_shuffle = st.columns(5)

    with c_prev:
        if st.button("⬅️ Previous", disabled=(current_idx == 0), use_container_width=True):
            st.session_state["flashcard_index"] = max(0, current_idx - 1)
            st.session_state["flashcard_flipped"] = False
            st.rerun()

    with c_mark_rev:
        if st.button("⚠️ Need Revision", use_container_width=True):
            status_map[card_id] = "needs_revision"
            if current_idx < total - 1:
                st.session_state["flashcard_index"] += 1
                st.session_state["flashcard_flipped"] = False
            st.rerun()

    with c_mark_know:
        if st.button("✅ Mastered", type="primary", use_container_width=True):
            status_map[card_id] = "known"
            if current_idx < total - 1:
                st.session_state["flashcard_index"] += 1
                st.session_state["flashcard_flipped"] = False
            st.rerun()

    with c_next:
        if st.button("Next ➡️", disabled=(current_idx == total - 1), use_container_width=True):
            st.session_state["flashcard_index"] = min(total - 1, current_idx + 1)
            st.session_state["flashcard_flipped"] = False
            st.rerun()

    with c_shuffle:
        if st.button("🔀 Shuffle", use_container_width=True):
            random.shuffle(cards)
            st.session_state["content_Flashcards"] = cards
            st.session_state["flashcard_index"] = 0
            st.session_state["flashcard_flipped"] = False
            st.rerun()


def render_practice_test(test_data: Dict[str, Any], topic: str, difficulty: str):
    """Render full practice test with timer, mixed questions, and automatic Gemini evaluation."""
    st.subheader(f"⏱️ Practice Test: {test_data.get('topic', topic)}")

    questions = test_data.get("questions", [])
    total_q = len(questions)
    suggested_time = test_data.get("suggested_time_minutes", total_q * 2)

    # Elapsed time calculation
    start_time = st.session_state.get("test_start_time", time.time())
    elapsed_seconds = int(time.time() - start_time)
    elapsed_min = elapsed_seconds // 60
    elapsed_sec = elapsed_seconds % 60

    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.6); padding: 10px 18px; border-radius: 10px; margin-bottom: 20px;">
            <div><strong>Questions:</strong> {total_q} Mixed | <strong>Difficulty:</strong> {difficulty}</div>
            <div style="font-weight: 700; color: #a855f7;">⏳ Elapsed Time: {elapsed_min:02d}:{elapsed_sec:02d} (Target: ~{suggested_time} mins)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    submitted = st.session_state.get("test_submitted", False)
    user_answers = st.session_state.setdefault("test_user_answers", {})

    if not submitted:
        # Render question forms
        with st.form("practice_test_form"):
            for idx, q in enumerate(questions):
                qid = q.get("id", idx + 1)
                q_type = q.get("type", "mcq")
                q_text = q.get("question", "")

                st.markdown(f"### Q{idx + 1} ({'Multiple Choice' if q_type == 'mcq' else 'Conceptual Answer'}):")
                st.markdown(q_text)

                if q_type == "mcq":
                    options = q.get("options", {})
                    opt_keys = ["A", "B", "C", "D"]
                    opt_labels = [f"{k}. {options.get(k, '')}" for k in opt_keys if k in options]
                    selected = st.radio(
                        f"Select answer for Q{idx + 1}:",
                        options=opt_labels,
                        index=None,
                        key=f"test_mcq_{qid}",
                    )
                    if selected:
                        user_answers[qid] = selected.split(".")[0].strip()
                else:
                    ans_text = st.text_area(
                        f"Write your response for Q{idx + 1}:",
                        placeholder="Explain your reasoning clearly...",
                        key=f"test_short_{qid}",
                        height=100,
                    )
                    user_answers[qid] = ans_text

                st.markdown("<hr style='border-color: rgba(139, 92, 246, 0.1);'>", unsafe_allow_html=True)

            submit_test = st.form_submit_button("🏁 Submit Practice Test for Evaluation", type="primary")

        if submit_test:
            st.session_state["test_submitted"] = True
            with st.spinner("🤖 PromptWise is evaluating your answers and generating your performance summary..."):
                try:
                    # Construct evaluation payload
                    answers_summary = "\n".join(
                        f"Question {k}: Student Answer: {v}" for k, v in user_answers.items()
                    )
                    eval_prompt = TEST_EVALUATION_PROMPT.format(
                        topic=topic,
                        test_content=json.dumps(test_data, ensure_ascii=False, indent=2),
                        student_answers=answers_summary,
                        total_questions=total_q,
                    )
                    eval_result = call_gemini(eval_prompt)
                    st.session_state["test_evaluation"] = eval_result
                    st.rerun()
                except Exception as e:
                    st.error(f"Evaluation error: {e}")
    else:
        # Results View
        st.success("🎉 Practice Test Submitted & Evaluated!")
        evaluation = st.session_state.get("test_evaluation", "Evaluation in progress...")
        st.markdown(evaluation)

        if st.button("🔄 Retake Practice Test", key="retake_test_btn"):
            st.session_state["test_submitted"] = False
            st.session_state["test_user_answers"] = {}
            st.session_state["test_start_time"] = time.time()
            st.session_state["test_evaluation"] = None
            st.rerun()
