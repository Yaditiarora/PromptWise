"""
Dashboard view for PromptWise.
Provides user overview, study statistics, quick launch for study modes, and recent activity.
"""

import streamlit as st
from services import db_service
from ui.components import render_hero, render_metric_card


def render_dashboard(set_page_fn):
    """Render the main dashboard page."""
    render_hero(
        title="📚 PromptWise",
        subtitle="Learn Smarter. Prompt Better. — AI-Powered Adaptive Study Platform",
        badge_text="Version 2.0 • Powered by Gemini",
    )

    # Fetch real SQLite metrics
    stats = db_service.get_history_stats()
    total_sessions = stats["total_sessions"]
    mode_counts = stats["mode_counts"]
    recent_sessions = stats["recent_sessions"]

    # Quick metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card(str(total_sessions), "Saved Study Sessions", "📚")
    with col2:
        modes_used = len(mode_counts)
        render_metric_card(f"{modes_used}/5", "Modes Explored", "🎯")
    with col3:
        quiz_count = mode_counts.get("Quiz", 0) + mode_counts.get("Test", 0)
        render_metric_card(str(quiz_count), "Quizzes & Tests Taken", "🏆")
    with col4:
        opt_count = mode_counts.get("Prompt Optimizer", 0) + mode_counts.get("Comparison", 0)
        render_metric_card(str(opt_count), "Prompts Engineered", "✨")

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Access to All Five Study Modes
    st.subheader("⚡ Quick Start Study Modes")
    st.caption("Select any study mode to jump directly into interactive learning.")

    def launch_mode_callback(mode_name: str):
        st.session_state["pending_nav"] = "Study Assistant"
        st.session_state["nav_selection_radio"] = "Study Assistant"
        st.session_state["sa_mode_select"] = mode_name
        st.session_state["active_study_mode"] = mode_name

    def view_history_callback():
        st.session_state["pending_nav"] = "Prompt History"
        st.session_state["nav_selection_radio"] = "Prompt History"

    # Row 1: 3 Cards (Explain, Summarize, Quiz)
    r1_c1, r1_c2, r1_c3 = st.columns(3)

    with r1_c1:
        st.markdown(
            """
            <div class="pw-mode-card">
                <div style="font-size: 2.2rem;">📖</div>
                <div class="pw-mode-title">Explain</div>
                <div class="pw-mode-desc">Intuitive conceptual explanations with real-world examples.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Start Explain",
            key="dash_btn_explain",
            use_container_width=True,
            type="primary",
            on_click=launch_mode_callback,
            args=("Explain",),
        )

    with r1_c2:
        st.markdown(
            """
            <div class="pw-mode-card">
                <div style="font-size: 2.2rem;">📝</div>
                <div class="pw-mode-title">Summarize</div>
                <div class="pw-mode-desc">High-impact revision notes, bullet points & memory tips.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Start Summarize",
            key="dash_btn_notes",
            use_container_width=True,
            type="primary",
            on_click=launch_mode_callback,
            args=("Summarize",),
        )

    with r1_c3:
        st.markdown(
            """
            <div class="pw-mode-card">
                <div style="font-size: 2.2rem;">❓</div>
                <div class="pw-mode-title">Quiz</div>
                <div class="pw-mode-desc">Interactive multiple-choice quizzes with instant scoring.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Start Quiz",
            key="dash_btn_quiz",
            use_container_width=True,
            type="primary",
            on_click=launch_mode_callback,
            args=("Quiz",),
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Row 2: 2 Cards (Flashcards, Practice Test)
    r2_c1, r2_c2 = st.columns(2)

    with r2_c1:
        st.markdown(
            """
            <div class="pw-mode-card">
                <div style="font-size: 2.2rem;">🗂️</div>
                <div class="pw-mode-title">Flashcards</div>
                <div class="pw-mode-desc">Interactive card flip with spaced repetition mastery tracking.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Start Flashcards",
            key="dash_btn_cards",
            use_container_width=True,
            type="primary",
            on_click=launch_mode_callback,
            args=("Flashcards",),
        )

    with r2_c2:
        st.markdown(
            """
            <div class="pw-mode-card">
                <div style="font-size: 2.2rem;">⏱️</div>
                <div class="pw-mode-title">Practice Test</div>
                <div class="pw-mode-desc">Timed exam simulation with mixed questions & AI evaluation.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Start Practice Test",
            key="dash_btn_test",
            use_container_width=True,
            type="primary",
            on_click=launch_mode_callback,
            args=("Test",),
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Activity Summary & Recent Sessions
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("🕒 Recently Used Topics & Prompts")
        if not recent_sessions:
            st.info("No study sessions recorded yet. Launch any mode above to begin learning!")
        else:
            for s in recent_sessions:
                with st.container():
                    st.markdown(
                        f"""
                        <div class="pw-card" style="padding: 14px 18px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <span style="font-weight: 700; font-size: 1rem; color: #f8fafc;">{s['topic']}</span>
                                    <span style="margin-left: 10px; font-size: 0.75rem; color: #c084fc; background: rgba(168,85,247,0.15); padding: 2px 8px; border-radius: 6px;">{s['study_mode']}</span>
                                </div>
                                <span style="font-size: 0.8rem; color: #64748b;">{s['timestamp']}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            st.button("View Full History →", key="view_hist_btn", on_click=view_history_callback)

    with col_right:
        st.subheader("📊 Study Activity Breakdown")
        if not mode_counts:
            st.info("Activity breakdown will appear as you generate content.")
        else:
            for m, cnt in mode_counts.items():
                pct = int((cnt / max(total_sessions, 1)) * 100)
                st.markdown(f"**{m}**: {cnt} sessions ({pct}%)")
                st.progress(min(pct / 100, 1.0))
