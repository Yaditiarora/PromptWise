"""
About Project view for PromptWise.
Provides architectural documentation, prompt engineering principles, team credits, and technology stack.
"""

import streamlit as st
from ui.components import render_hero


def render_about():
    """Render the About Project page."""
    render_hero(
        title="ℹ️ About PromptWise",
        subtitle="Prompt Engineering Mini Project • SCSE4041 Milestone 2 • Team Cognivance",
        badge_text="Academic Research & Architecture",
    )

    st.markdown(
        """
        ### 🎯 Project Mission
        **PromptWise** is an advanced AI study assistant built to demonstrate the practical power of **prompt engineering**
        in educational technology. By transforming basic, ambiguous questions into structured, role-grounded prompts,
        PromptWise maximizes conceptual comprehension, eliminates AI hallucinations, and provides targeted revision.
        """
    )

    # Architectural Overview
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🏛️ System Architecture")

    col_arch1, col_arch2 = st.columns(2)
    with col_arch1:
        st.markdown(
            """
            <div class="pw-card">
                <div style="font-weight: 700; color: #a5b4fc; font-size: 1.1rem; margin-bottom: 8px;">Frontend & Orchestration</div>
                <ul style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; padding-left: 20px;">
                    <li><strong>Framework:</strong> Streamlit 1.67+ with responsive wide layout</li>
                    <li><strong>Styling:</strong> Custom dark navy & purple CSS design system</li>
                    <li><strong>Session Management:</strong> Streamlit Session State prevents redundant API re-invocations</li>
                    <li><strong>Modular Views:</strong> Dashboard, Study Assistant, Optimizer, Comparison, History</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_arch2:
        st.markdown(
            """
            <div class="pw-card">
                <div style="font-weight: 700; color: #c084fc; font-size: 1.1rem; margin-bottom: 8px;">AI & Data Tier</div>
                <ul style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; padding-left: 20px;">
                    <li><strong>LLM:</strong> Google Gemini 3.5 Flash Lite via Google GenAI SDK</li>
                    <li><strong>Resilience:</strong> Automated model fallback, HTTP timeout management & 429/503 retry</li>
                    <li><strong>Persistence:</strong> Local SQLite database with thread-safe connection pooling</li>
                    <li><strong>Security:</strong> API credentials stored strictly in Streamlit secrets</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Prompt Engineering Methodology
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔬 The 7 Pillars of Prompt Optimization")
    st.markdown(
        """
        Every prompt processed by PromptWise's **Prompt Optimizer** is engineered using seven core architectural components:
        """
    )

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown(
            """
            <div class="pw-card" style="min-height: 140px;">
                <div style="color: #6366f1; font-weight: 700;">1. Role Assignment</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Establishes expert persona, pedagogical stance, and tone.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            """
            <div class="pw-card" style="min-height: 140px;">
                <div style="color: #8b5cf6; font-weight: 700;">2. Task Specifics</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Decomposes the objective into explicit, sequential instructions.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p3:
        st.markdown(
            """
            <div class="pw-card" style="min-height: 140px;">
                <div style="color: #a855f7; font-weight: 700;">3. Context Grounding</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Anchors the discussion to academic domain frameworks.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p4:
        st.markdown(
            """
            <div class="pw-card" style="min-height: 140px;">
                <div style="color: #ec4899; font-weight: 700;">4. Audience Depth</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Calibrates cognitive load for Beginner, Intermediate, or Advanced.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    p5, p6, p7, _ = st.columns(4)
    with p5:
        st.markdown(
            """
            <div class="pw-card" style="min-height: 140px;">
                <div style="color: #3b82f6; font-weight: 700;">5. Difficulty Calibration</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Matches depth from foundational intuition to mathematical rigor.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p6:
        st.markdown(
            """
            <div class="pw-card" style="min-height: 140px;">
                <div style="color: #10b981; font-weight: 700;">6. Output Formatting</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Specifies exact Markdown sections, bullets, definitions & takeaways.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p7:
        st.markdown(
            """
            <div class="pw-card" style="min-height: 140px;">
                <div style="color: #f59e0b; font-weight: 700;">7. Negative Constraints</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Strict guardrails preventing hallucinations and verbose fluff.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Team Credits
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("👥 Project Team — Cognivance")

    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown(
            """
            <div class="pw-card" style="text-align: center;">
                <div style="font-size: 2rem;">👑</div>
                <div style="font-weight: 700; color: #ffffff; margin-top: 4px;">Vanshika Beniwal</div>
                <div style="font-size: 0.8rem; color: #a5b4fc;">Team Leader • S24CSEU0166</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 6px;">Prompt Design & Engineering Architecture</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with t2:
        st.markdown(
            """
            <div class="pw-card" style="text-align: center;">
                <div style="font-size: 2rem;">💻</div>
                <div style="font-weight: 700; color: #ffffff; margin-top: 4px;">Yaditi Arora</div>
                <div style="font-size: 0.8rem; color: #c084fc;">Developer • S24CSEU0241</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 6px;">Application Engineering, UI/UX & Deployment</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with t3:
        st.markdown(
            """
            <div class="pw-card" style="text-align: center;">
                <div style="font-size: 2rem;">📊</div>
                <div style="font-weight: 700; color: #ffffff; margin-top: 4px;">Mohita Purohit</div>
                <div style="font-size: 0.8rem; color: #f472b6;">Analyst • S24CSEU0340</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 6px;">Testing, Benchmarking & Documentation</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
