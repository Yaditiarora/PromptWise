"""
Custom CSS and theme styling for PromptWise.
Provides a modern AI SaaS look with dark navy and purple/violet accents.
"""

THEME_CSS = """
<style>
/* ---------------- Root Palette & Fonts ---------------- */
:root {
    --bg-dark: #0b0f19;
    --card-bg: rgba(22, 27, 46, 0.75);
    --card-border: rgba(139, 92, 246, 0.25);
    --card-hover-border: rgba(168, 85, 247, 0.6);
    --primary-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    --accent-glow: 0 0 25px rgba(139, 92, 246, 0.25);
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
}

/* ---------------- Global App Layout ---------------- */
.stApp {
    background: radial-gradient(circle at 15% 15%, #13172e 0%, #0b0f19 80%);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* ---------------- Top Hero Banner ---------------- */
.pw-hero-banner {
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), var(--accent-glow);
    position: relative;
    overflow: hidden;
}

.pw-hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 280px;
    height: 280px;
    background: radial-gradient(circle, rgba(168, 85, 247, 0.2) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.pw-hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}

.pw-hero-subtitle {
    font-size: 1.05rem;
    color: #a5b4fc;
    margin-top: 6px;
    margin-bottom: 0;
    font-weight: 500;
}

/* ---------------- Modern Metric & Feature Cards ---------------- */
.pw-card {
    background: rgba(22, 27, 46, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.25s ease-in-out;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
}

.pw-card:hover {
    border-color: var(--card-hover-border);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.2);
}

.pw-metric-number {
    font-size: 2.2rem;
    font-weight: 700;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}

.pw-metric-label {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    margin-top: 4px;
}

/* ---------------- Quick Start Mode Cards ---------------- */
.pw-mode-card {
    background: rgba(22, 27, 46, 0.75);
    backdrop-filter: blur(12px);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    min-height: 175px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
    transition: all 0.25s ease-in-out;
}

.pw-mode-card:hover {
    border-color: var(--card-hover-border);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.25);
}

.pw-mode-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 8px 0 4px 0;
    white-space: nowrap !important;
    word-break: keep-all !important;
    overflow-wrap: normal !important;
    hyphens: none !important;
}

.pw-mode-desc {
    font-size: 0.85rem;
    color: #94a3b8;
    line-height: 1.4;
    margin-bottom: 6px;
    word-break: normal;
    overflow-wrap: break-word;
}

/* ---------------- Interactive Flashcard Component ---------------- */
.pw-flashcard {
    background: linear-gradient(145deg, rgba(30, 37, 66, 0.9) 0%, rgba(19, 23, 43, 0.95) 100%);
    border: 1px solid rgba(168, 85, 247, 0.4);
    border-radius: 18px;
    padding: 36px 28px;
    text-align: center;
    min-height: 240px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35), var(--accent-glow);
    margin: 15px 0;
}

.pw-flashcard-tag {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    background: rgba(139, 92, 246, 0.2);
    border: 1px solid rgba(139, 92, 246, 0.4);
    color: #c4b5fd;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 12px;
}

.pw-flashcard-text {
    font-size: 1.35rem;
    font-weight: 600;
    color: #ffffff;
    line-height: 1.5;
}

/* ---------------- Badges and Chips ---------------- */
.pw-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 600;
}

.pw-badge-beginner {
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.pw-badge-intermediate {
    background: rgba(59, 130, 246, 0.15);
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.3);
}

.pw-badge-advanced {
    background: rgba(168, 85, 247, 0.15);
    color: #c084fc;
    border: 1px solid rgba(168, 85, 247, 0.3);
}

/* ---------------- Comparison Visualizer ---------------- */
.pw-score-box {
    text-align: center;
    padding: 16px;
    border-radius: 12px;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.2);
}

.pw-score-val {
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 4px;
}

/* ---------------- Streamlit Element Overrides ---------------- */
/* Buttons */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease !important;
}

.stButton > button[kind="primary"] {
    background: var(--primary-gradient) !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.35) !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(168, 85, 247, 0.5) !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0d121f !important;
    border-right: 1px solid rgba(139, 92, 246, 0.15) !important;
}

[data-testid="stSidebar"] .stRadio > div {
    gap: 8px;
}

/* Input Fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: rgba(17, 24, 39, 0.8) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #a855f7 !important;
    box-shadow: 0 0 10px rgba(168, 85, 247, 0.3) !important;
}

/* Code boxes */
pre {
    border-radius: 10px !important;
    border: 1px solid rgba(139, 92, 246, 0.25) !important;
}
</style>
"""


def apply_theme():
    """Inject the custom CSS theme into the current Streamlit app."""
    import streamlit as st
    st.markdown(THEME_CSS, unsafe_allow_html=True)
