"""
PromptWise: AI-Powered Study Assistant
Main application entry point.

Team Cognivance | SCSE4041 Prompt Engineering Mini Project
"""

import sys
from pathlib import Path

# Ensure 'code' folder is on sys.path for direct imports
CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import streamlit as st
from services import db_service
from services.gemini_service import get_api_status, is_client_ready
from ui.styles import apply_theme
from views.about import render_about
from views.comparator import render_response_comparison
from views.dashboard import render_dashboard
from views.history import render_prompt_history
from views.optimizer import render_prompt_optimizer
from views.study_assistant import render_study_assistant

# ----------------- STREAMLIT CONFIGURATION -----------------
st.set_page_config(
    page_title="PromptWise • AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply global dark navy & purple theme
apply_theme()

# Initialize SQLite database
db_service.init_db()


# Handle pending navigation before sidebar radio is instantiated
if "pending_nav" in st.session_state:
    st.session_state["nav_selection_radio"] = st.session_state.pop("pending_nav")


# ----------------- SIDEBAR NAVIGATION -----------------
def set_active_page(page_name: str):
    """Callback to switch pages programmatically."""
    st.session_state["pending_nav"] = page_name
    st.session_state["nav_selection"] = page_name


# Sidebar brand header
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: left; padding: 10px 0 16px 0;">
            <div style="font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                📚 PromptWise
            </div>
            <div style="font-size: 0.85rem; color: #a5b4fc; font-weight: 600; margin-top: 2px;">
                Learn Smarter. Prompt Better.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pages = [
        "Dashboard",
        "Study Assistant",
        "Prompt Optimizer",
        "Compare Responses",
        "Prompt History",
        "About Project",
    ]

    if "nav_selection_radio" not in st.session_state:
        st.session_state["nav_selection_radio"] = "Dashboard"

    selected_page = st.radio(
        "Navigation",
        pages,
        key="nav_selection_radio",
        label_visibility="collapsed",
    )
    st.session_state["nav_selection"] = selected_page

    st.markdown("<hr style='border-color: rgba(139, 92, 246, 0.15); margin: 24px 0 16px 0;'>", unsafe_allow_html=True)

    # System Status & Quick Stats
    api_info = get_api_status()
    st.markdown(
        f"""
        <div style="background: rgba(22, 27, 46, 0.6); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 10px; padding: 12px; margin-bottom: 16px;">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #64748b; font-weight: 700; letter-spacing: 0.05em;">SYSTEM STATUS</div>
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px; font-size: 0.85rem; font-weight: 600; color: {api_info['color']};">
                <span>{api_info['icon']}</span>
                <span>{api_info['label']}</span>
            </div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">
                {api_info['details']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Stats widget in sidebar
    stats = db_service.get_history_stats()
    st.markdown(
        f"""
        <div style="background: rgba(22, 27, 46, 0.6); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 10px; padding: 12px; margin-bottom: 20px;">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #64748b; font-weight: 700; letter-spacing: 0.05em;">SAVED SESSIONS</div>
            <div style="font-size: 1.4rem; font-weight: 800; color: #c4b5fd; margin-top: 2px;">
                {stats['total_sessions']}
            </div>
            <div style="font-size: 0.75rem; color: #94a3b8;">
                Available in persistent history
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------- VIEW ROUTING -----------------
active_page = st.session_state.get("nav_selection_radio", "Dashboard")

if active_page == "Dashboard":
    render_dashboard(set_active_page)

elif active_page == "Study Assistant":
    render_study_assistant()

elif active_page == "Prompt Optimizer":
    render_prompt_optimizer()

elif active_page == "Compare Responses":
    render_response_comparison()

elif active_page == "Prompt History":
    render_prompt_history()

elif active_page == "About Project":
    render_about()
