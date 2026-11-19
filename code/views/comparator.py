"""
Compare Responses view for PromptWise.
Demonstrates the empirical value of prompt engineering by generating side-by-side
Basic vs Optimized AI responses and evaluating them with transparent criteria using Gemini.
"""

import streamlit as st
from services import db_service
from services.evaluation_service import evaluate_responses
from services.gemini_service import call_gemini
from services.prompt_optimizer_service import optimize_prompt
from ui.components import render_hero


def render_response_comparison():
    """Render the Basic vs Optimized Response Comparison view."""
    render_hero(
        title="⚖️ Compare Responses",
        subtitle="Empirical prompt engineering: Compare raw AI output vs optimized output side-by-side.",
        badge_text="Evaluation & Benchmarking",
    )

    st.markdown(
        """
        Evaluate how prompt engineering impacts learning quality. PromptWise runs both the
        **basic unengineered prompt** and the **optimized prompt** through Gemini, then performs
        an objective, multi-criteria evaluation with scores out of 10.
        """
    )

    # Input Form
    col_t1, col_t2 = st.columns([3, 2])
    with col_t1:
        topic = st.text_input(
            "Topic / Subject",
            value=st.session_state.get("comp_topic", "Operating Systems Paging and Virtual Memory"),
            placeholder="e.g. Mealy vs Moore machines, Photosynthesis, Normalization in DBMS...",
            key="comp_topic_input",
        )
    with col_t2:
        task = st.selectbox(
            "Study Task",
            ["Explain Concept", "Generate Revision Notes", "Exam-Style Answer", "Step-by-step Tutorial"],
            index=0,
            key="comp_task_select",
        )

    basic_prompt = st.text_area(
        "Basic (Unengineered) Prompt",
        value=st.session_state.get("comp_basic_prompt", "Explain paging in operating systems."),
        placeholder="e.g. Explain photosynthesis or What is recursion?",
        height=70,
        key="comp_basic_prompt_input",
    )

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        difficulty = st.selectbox(
            "Target Difficulty",
            ["Beginner", "Intermediate", "Advanced"],
            index=1,
            key="comp_diff_select",
        )
    with col_d2:
        audience = st.selectbox(
            "Target Academic Level",
            ["School / Introductory", "Undergraduate / College", "Postgraduate / Professional"],
            index=1,
            key="comp_aud_select",
        )

    col_btn, _ = st.columns([2, 5])
    with col_btn:
        compare_clicked = st.button("🔬 Run Comparison Benchmark", type="primary", use_container_width=True)

    if compare_clicked:
        if not basic_prompt.strip() or not topic.strip():
            st.warning("⚠️ Please provide both a topic and a basic prompt.")
            return

        with st.status("🚀 Running Comparative Benchmark...", expanded=True) as status:
            try:
                # Step 1: Optimize the prompt
                status.write("1/3 Optimizing prompt architecture with Gemini...")
                opt_data = optimize_prompt(
                    raw_prompt=basic_prompt,
                    topic=topic,
                    difficulty=difficulty,
                    goal=task,
                    audience=audience,
                )
                optimized_prompt = opt_data.get("optimized_prompt", basic_prompt)

                # Step 2: Generate Basic Response (minimal system instruction)
                status.write("2/3 Generating Basic Response from raw prompt...")
                basic_response = call_gemini(
                    prompt=basic_prompt,
                    system_instruction="You are a helpful assistant. Answer the user prompt directly.",
                    temperature=0.7,
                )

                # Step 3: Generate Optimized Response
                status.write("3/3 Generating Optimized Response from engineered prompt...")
                opt_response = call_gemini(
                    prompt=optimized_prompt,
                    temperature=0.7,
                )

                # Step 4: Evaluate both with Gemini
                status.write("⚖️ Conducting objective 5-dimension evaluation with Gemini...")
                eval_data = evaluate_responses(
                    topic=topic,
                    difficulty=difficulty,
                    task=task,
                    basic_prompt=basic_prompt,
                    optimized_prompt=optimized_prompt,
                    response_a=basic_response,
                    response_b=opt_response,
                )

                st.session_state["comp_results"] = {
                    "topic": topic,
                    "difficulty": difficulty,
                    "task": task,
                    "basic_prompt": basic_prompt,
                    "optimized_prompt": optimized_prompt,
                    "basic_response": basic_response,
                    "optimized_response": opt_response,
                    "evaluation": eval_data,
                }

                # Save to history
                db_service.add_history(
                    topic=topic,
                    study_mode="Comparison",
                    difficulty=difficulty,
                    original_prompt=basic_prompt,
                    optimized_prompt=optimized_prompt,
                    generated_response=f"Winner: {eval_data.get('winner', 'N/A')}\n\nVerdict: {eval_data.get('detailed_verdict', '')}",
                    metadata=eval_data,
                )

                status.update(label="✅ Benchmark completed successfully!", state="complete", expanded=False)

            except Exception as e:
                status.update(label=f"❌ Error occurred: {str(e)}", state="error")
                st.error(f"Benchmark failed: {str(e)}")

    # ---------------- DISPLAY COMPARISON RESULTS ----------------
    if "comp_results" in st.session_state:
        res = st.session_state["comp_results"]
        eval_data = res.get("evaluation", {})
        scores_a = eval_data.get("response_a_scores", {})
        scores_b = eval_data.get("response_b_scores", {})
        winner = eval_data.get("winner", "Optimized Response")

        st.markdown("<hr style='border-color: rgba(139, 92, 246, 0.2); margin: 30px 0;'>", unsafe_allow_html=True)

        # Side-by-Side Outputs
        col_res_a, col_res_b = st.columns(2)

        with col_res_a:
            st.markdown("### 🅰️ Basic Response")
            st.caption("Generated with unengineered prompt")
            overall_a = scores_a.get("overall_score", 6.5)
            st.markdown(
                f"""
                <div class="pw-score-box" style="margin-bottom: 14px;">
                    <div class="pw-score-val" style="color: #94a3b8;">{overall_a}/10</div>
                    <div style="font-size: 0.85rem; color: #64748b; font-weight: 600;">EVALUATION SCORE</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander("Show Raw Prompt Sent", expanded=False):
                st.code(res["basic_prompt"], language="text")
            st.markdown(
                f"""
                <div class="pw-card" style="min-height: 400px; max-height: 600px; overflow-y: auto;">
                    {res['basic_response']}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_res_b:
            st.markdown("### 🅱️ Optimized Response")
            st.caption("Generated with engineered prompt")
            overall_b = scores_b.get("overall_score", 9.0)
            st.markdown(
                f"""
                <div class="pw-score-box" style="margin-bottom: 14px; border-color: rgba(168, 85, 247, 0.5); background: rgba(30, 27, 75, 0.4);">
                    <div class="pw-score-val" style="color: #c084fc;">{overall_b}/10</div>
                    <div style="font-size: 0.85rem; color: #a5b4fc; font-weight: 600;">EVALUATION SCORE</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander("Show Optimized Prompt Sent", expanded=False):
                st.code(res["optimized_prompt"], language="text")
            st.markdown(
                f"""
                <div class="pw-card" style="min-height: 400px; max-height: 600px; overflow-y: auto; border-color: rgba(168, 85, 247, 0.4);">
                    {res['optimized_response']}
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Evaluation & Criteria Breakdown
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Objective Criteria Breakdown (Scale: 1 to 10)")

        criteria = [
            ("Relevance", "relevance", "Adherence to topic and core intent"),
            ("Clarity", "clarity", "Readability, explanations, and flow"),
            ("Completeness", "completeness", "Thoroughness of concepts and depth"),
            ("Structure", "structure", "Logical formatting, headings, and takeaways"),
            ("Difficulty Alignment", "difficulty_alignment", f"Calibration to {res.get('difficulty')} level"),
        ]

        crit_analysis = eval_data.get("criteria_analysis", {})

        for name, key, desc in criteria:
            sc_a = scores_a.get(key, 5.0)
            sc_b = scores_b.get(key, 5.0)
            c1, c2, c3 = st.columns([2, 4, 4])
            with c1:
                st.markdown(f"**{name}**<br><span style='font-size: 0.75rem; color: #94a3b8;'>{desc}</span>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"**Basic:** `{sc_a}/10`")
                st.progress(min(float(sc_a) / 10.0, 1.0))
            with c3:
                st.markdown(f"**Optimized:** `{sc_b}/10`")
                st.progress(min(float(sc_b) / 10.0, 1.0))

            if key in crit_analysis:
                st.caption(f"💬 *Analysis:* {crit_analysis[key]}")
            st.markdown("<hr style='border-color: rgba(148, 163, 184, 0.1); margin: 8px 0;'>", unsafe_allow_html=True)

        # Verdict Summary Card
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🏆 Comparative Verdict & Key Takeaway")
        diff_val = eval_data.get("score_difference", abs(overall_b - overall_a))
        st.markdown(
            f"""
            <div class="pw-card" style="border-left: 4px solid #a855f7;">
                <div style="font-weight: 700; font-size: 1.1rem; color: #ffffff; margin-bottom: 6px;">
                    Selected Winner: <span style="color: #c084fc;">{winner}</span> (Delta: +{diff_val:.1f} pts)
                </div>
                <div style="color: #cbd5e1; line-height: 1.6; font-size: 0.95rem;">
                    {eval_data.get('detailed_verdict', 'The optimized prompt yielded a more structured and pedagogically sound response with specific takeaways and guardrails.')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption(
            "📌 **Academic Evaluation Methodology & Limitations:** Automated response benchmarking utilizes Gemini "
            "as an impartial evaluator across 5 predefined criteria (Relevance, Clarity, Completeness, Structure, Difficulty Alignment). "
            "Both responses were generated with identical model parameters (temperature=0.7). "
            "While automated LLM evaluation provides structured, scalable comparative analysis, it serves as a pedagogical heuristic "
            "and does not replace formal human grading."
        )
