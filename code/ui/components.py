"""
Reusable UI components for PromptWise.
Provides standardized headers, metric cards, badges, and layout helpers.
"""

from typing import Optional
import streamlit as st


def render_hero(title: str, subtitle: str, badge_text: Optional[str] = None):
    """Render the standard PromptWise hero header banner."""
    badge_html = (
        f'<div style="display:inline-block; margin-bottom: 8px;" class="pw-badge pw-badge-intermediate">{badge_text}</div>'
        if badge_text
        else ""
    )
    st.markdown(
        f"""
        <div class="pw-hero-banner">
            {badge_html}
            <h1 class="pw-hero-title">{title}</h1>
            <p class="pw-hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(number: str, label: str, icon: str = "⚡"):
    """Render an individual glowing metric card."""
    st.markdown(
        f"""
        <div class="pw-card">
            <div style="font-size: 1.4rem; margin-bottom: 6px;">{icon}</div>
            <div class="pw-metric-number">{number}</div>
            <div class="pw-metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_difficulty_badge(difficulty: str) -> str:
    """Return HTML for a styled difficulty badge."""
    css_class = {
        "Beginner": "pw-badge-beginner",
        "Intermediate": "pw-badge-intermediate",
        "Advanced": "pw-badge-advanced",
    }.get(difficulty, "pw-badge-intermediate")

    icon = {
        "Beginner": "🌱",
        "Intermediate": "🚀",
        "Advanced": "⚡",
    }.get(difficulty, "📚")

    return f'<span class="pw-badge {css_class}">{icon} {difficulty}</span>'
