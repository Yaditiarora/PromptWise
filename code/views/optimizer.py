"""
Prompt Optimizer view for PromptWise.
Transforms basic study prompts into production-grade, highly structured prompts using Gemini.
"""

import streamlit as st
from services import db_service
from services.prompt_optimizer_service import optimize_prompt
from ui.components import render_difficulty_badge, render_hero


def render_prompt_optimizer():
    """Render the dedicated Prompt Optimizer view."""
    render_hero(
        title="✨ Prompt Optimizer",
        subtitle="Upgrade vague study prompts into high-performance, structured academic prompts.",
        badge_text="Prompt Engineering Engine",
    )

    st.markdown(
        """
        An optimized prompt guides the AI with **clear roles, targeted context, structured output constraints,
        and difficulty calibration**, delivering substantially deeper, hallucination-free explanations.
        """
    )

    # Input Form
    with st.container():
        raw_prompt = st.text_area(
            "Enter your basic prompt",
            value=st.session_state.get("optimizer_raw_input", "Explain photosynthesis."),
            placeholder="e.g. Explain how quicksort works, or What is quantum entanglement?",
            help="Type your raw, unoptimized study prompt here.",
            height=100,
            key="opt_raw_text",
        )

        col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
        with col_cfg1:
            topic = st.text_input(
                "Subject / Topic",
                value=st.session_state.get("optimizer_topic", "Biology / Plant Physiology"),
                key="opt_topic_input",
            )
        with col_cfg2:
            difficulty = st.selectbox(
                "Target Difficulty",
                ["Beginner", "Intermediate", "Advanced"],
                index=1,
                key="opt_diff_select",
            )
        with col_cfg3:
            audience = st.selectbox(
                "Target Audience",
                ["High School Student", "Undergraduate Student", "Postgraduate Researcher", "Self-Learner"],
                index=1,
                key="opt_aud_select",
            )

        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            output_format = st.selectbox(
                "Desired Output Format",
                [
                    "Structured Sections (Definition, Steps, Example, Takeaways)",
                    "Concise Revision Bullet Points & Memory Tips",
                    "Step-by-Step Educational Tutorial with Code/Diagrams",
                    "Marks-based Exam Format with Headings & Points",
                ],
                key="opt_format_select",
            )
        with col_p2:
            constraints = st.text_input(
                "Specific Constraints / Limits",
                value="Under 250 words, include 1 real-world analogy, no hallucination",
                key="opt_constraints_input",
            )
        with col_p3:
            language = st.selectbox(
                "Language Mode",
                ["English", "Hinglish"],
                key="opt_lang_select",
            )

    btn_col1, btn_col2 = st.columns([2, 5])
    with btn_col1:
        optimize_clicked = st.button("🚀 Optimize Prompt with AI", type="primary", use_container_width=True)

    # Handle generation
    if optimize_clicked:
        if not raw_prompt.strip():
            st.warning("⚠️ Please provide a prompt to optimize.")
            return

        with st.spinner("🤖 PromptWise is analyzing and engineering your prompt with Gemini..."):
            try:
                result = optimize_prompt(
                    raw_prompt=raw_prompt,
                    topic=topic,
                    difficulty=difficulty,
                    goal="Comprehensive conceptual mastery",
                    audience=audience,
                    output_format=output_format,
                    constraints=constraints,
                    language=language,
                )
                st.session_state["opt_result"] = result
                st.session_state["opt_raw_used"] = raw_prompt
                st.session_state["opt_diff_used"] = difficulty
                st.session_state["opt_topic_used"] = topic

                # Save to history
                db_service.add_history(
                    topic=topic or "Prompt Optimization",
                    study_mode="Prompt Optimizer",
                    difficulty=difficulty,
                    original_prompt=raw_prompt,
                    optimized_prompt=result["optimized_prompt"],
                    generated_response=result["explanation_of_improvements"],
                    metadata=result,
                )
                active_model = st.session_state.get("last_active_model", "gemini-3.5-flash-lite")
                used_fb = st.session_state.get("used_fallback", False)
                fb_suffix = " (Fallback Model)" if used_fb else " (Primary Model)"
                st.success(f"✅ Prompt engineered via `{active_model}`{fb_suffix}!")
            except Exception as e:
                st.error(f"❌ Optimization failed: {str(e)}")

    # ---------------- DISPLAY RESULTS ----------------
    if "opt_result" in st.session_state:
        res = st.session_state["opt_result"]
        opt_text = res.get("optimized_prompt", "")
        explanation = res.get("explanation_of_improvements", "")
        raw_used = st.session_state.get("opt_raw_used", raw_prompt)

        st.markdown("<hr style='border-color: rgba(139, 92, 246, 0.2); margin: 30px 0;'>", unsafe_allow_html=True)

        col_orig, col_opt = st.columns(2)

        with col_orig:
            st.markdown("### 🅰️ Original Prompt")
            st.caption("Raw, unoptimized user input")
            st.markdown(
                f"""
                <div class="pw-card" style="min-height: 220px; font-style: italic; color: #cbd5e1;">
                    "{raw_used}"
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Copy original prompt code snippet
            st.code(raw_used, language="text")

        with col_opt:
            st.markdown("### 🅱️ Optimized Prompt")
            st.caption("Engineered with role, context, output format & constraints")
            st.markdown(
                f"""
                <div class="pw-card" style="min-height: 220px; border-color: rgba(168, 85, 247, 0.6); background: rgba(30, 27, 75, 0.4);">
                    <div style="margin-bottom: 8px;">{render_difficulty_badge(st.session_state.get('opt_diff_used', 'Intermediate'))}</div>
                    <pre style="white-space: pre-wrap; word-wrap: break-word; font-family: inherit; font-size: 0.95rem; color: #f8fafc; margin: 0;">{opt_text}</pre>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Copy optimized prompt snippet
            st.code(opt_text, language="text")

        # Regenerate & Action Buttons
        act1, act2 = st.columns([2, 5])
        with act1:
            if st.button("🔄 Regenerate Optimized Prompt", use_container_width=True):
                with st.spinner("Re-optimizing prompt..."):
                    try:
                        result = optimize_prompt(
                            raw_prompt=raw_used,
                            topic=st.session_state.get("opt_topic_used", topic),
                            difficulty=st.session_state.get("opt_diff_used", difficulty),
                            audience=audience,
                        )
                        st.session_state["opt_result"] = result
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

        # Improvement Analysis Section
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("💡 What Was Improved?")
        st.markdown(
            f"""
            <div class="pw-card">
                <div style="color: #c4b5fd; font-weight: 600; margin-bottom: 6px;">Prompt Architecture Breakdown:</div>
                <p style="color: #e2e8f0; line-height: 1.6;">{explanation}</p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-top: 14px;">
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 10px 14px; border-radius: 8px; border-left: 3px solid #6366f1;">
                        <span style="font-weight: 700; color: #a5b4fc;">Role Framing:</span><br>
                        <span style="font-size: 0.85rem; color: #94a3b8;">{res.get('role_assigned', 'Expert Educator')}</span>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 10px 14px; border-radius: 8px; border-left: 3px solid #a855f7;">
                        <span style="font-weight: 700; color: #c084fc;">Task Clarification:</span><br>
                        <span style="font-size: 0.85rem; color: #94a3b8;">{res.get('task_clarified', 'Structured instructions')}</span>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 10px 14px; border-radius: 8px; border-left: 3px solid #ec4899;">
                        <span style="font-weight: 700; color: #f472b6;">Guardrails:</span><br>
                        <span style="font-size: 0.85rem; color: #94a3b8;">{res.get('constraints_added', 'Accuracy & scope limits')}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
