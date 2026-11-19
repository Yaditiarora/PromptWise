"""
Prompt History view for PromptWise.
Provides SQLite-backed persistence, real-time search, multi-factor filtering,
detailed inspection, prompt copying, and deletion management.
"""

import streamlit as st
from services import db_service
from ui.components import render_difficulty_badge, render_hero


def render_prompt_history():
    """Render the SQLite-backed Prompt History page."""
    render_hero(
        title="📜 Prompt History",
        subtitle="Review, search, filter, and reuse your past study sessions and engineered prompts.",
        badge_text="Persistent SQLite Storage",
    )

    # ---------------- SEARCH & FILTERS ----------------
    col_search, col_f_mode, col_f_diff = st.columns([3, 2, 2])

    with col_search:
        search_query = st.text_input(
            "Search History",
            placeholder="Search by topic, keyword, or prompt...",
            key="hist_search_input",
        )

    with col_f_mode:
        mode_filter = st.selectbox(
            "Filter by Mode",
            ["All", "Explain", "Summarize", "Quiz", "Flashcards", "Test", "Exam Answer", "Prompt Optimizer", "Comparison"],
            key="hist_mode_filter",
        )

    with col_f_diff:
        diff_filter = st.selectbox(
            "Filter by Difficulty",
            ["All", "Beginner", "Intermediate", "Advanced"],
            key="hist_diff_filter",
        )

    # Query DB
    records = db_service.get_history(
        search_query=search_query,
        mode_filter=mode_filter,
        difficulty_filter=diff_filter,
    )

    # Top summary & bulk actions row
    col_cnt, col_clear = st.columns([4, 1])
    with col_cnt:
        st.caption(f"Showing **{len(records)}** recorded study sessions")

    with col_clear:
        if len(records) > 0:
            if "confirm_clear" not in st.session_state:
                st.session_state["confirm_clear"] = False

            if not st.session_state["confirm_clear"]:
                if st.button("🗑️ Clear All", key="hist_clear_btn", use_container_width=True):
                    st.session_state["confirm_clear"] = True
                    st.rerun()
            else:
                st.warning("Are you sure? This will delete all history.")
                c_yes, c_no = st.columns(2)
                with c_yes:
                    if st.button("Yes, Clear", type="primary", key="confirm_clear_yes"):
                        db_service.clear_all_history()
                        st.session_state["confirm_clear"] = False
                        st.success("All history cleared.")
                        st.rerun()
                with c_no:
                    if st.button("Cancel", key="confirm_clear_no"):
                        st.session_state["confirm_clear"] = False
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if not records:
        st.info("No study history records match your search criteria. Generate content in Study Assistant to see items here.")
        return

    # Render history cards
    for item in records:
        item_id = item["id"]
        topic = item["topic"]
        mode = item["study_mode"]
        diff = item["difficulty"]
        timestamp = item["timestamp"]
        orig_p = item["original_prompt"]
        opt_p = item.get("optimized_prompt", "")
        response_text = item["generated_response"]

        with st.container():
            st.markdown(
                f"""
                <div class="pw-card" style="margin-bottom: 12px; padding: 18px 22px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <span style="font-size: 1.15rem; font-weight: 700; color: #ffffff;">{topic}</span>
                            <span style="margin-left: 10px; font-size: 0.8rem; background: rgba(99, 102, 241, 0.2); color: #a5b4fc; padding: 3px 8px; border-radius: 6px; font-weight: 600;">{mode}</span>
                            <span style="margin-left: 6px;">{render_difficulty_badge(diff)}</span>
                        </div>
                        <span style="font-size: 0.8rem; color: #64748b;">📅 {timestamp}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Details expander
            with st.expander(f"🔍 Inspect Session Details (ID #{item_id})", expanded=False):
                d_col1, d_col2 = st.columns(2)
                with d_col1:
                    st.markdown("**Original Prompt:**")
                    st.code(orig_p, language="text")

                with d_col2:
                    if opt_p and opt_p != orig_p:
                        st.markdown("**Optimized Prompt:**")
                        st.code(opt_p, language="text")
                    else:
                        st.markdown("**Mode Type:**")
                        st.info(f"{mode} • {diff}")

                st.markdown("**Generated Output Preview:**")
                st.markdown(response_text)

                # Delete single item button
                del_col, _ = st.columns([2, 5])
                with del_col:
                    if st.button(f"🗑️ Delete Session #{item_id}", key=f"del_item_{item_id}"):
                        db_service.delete_history(item_id)
                        st.success(f"Deleted session #{item_id}")
                        st.rerun()

            st.markdown("<hr style='border-color: rgba(139, 92, 246, 0.1); margin: 6px 0;'>", unsafe_allow_html=True)
