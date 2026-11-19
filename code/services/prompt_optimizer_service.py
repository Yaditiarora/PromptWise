"""
Prompt Optimizer service for PromptWise.
Transforms basic study prompts into production-grade prompts using Gemini.
"""

from typing import Any, Dict

from prompts.templates import (
    DIFFICULTY_GUIDELINES,
    LANG_NOTE,
    OPTIMIZER_PROMPT,
    OPTIMIZER_SYSTEM_PROMPT,
)
from services.gemini_service import call_gemini, parse_json_response


def optimize_prompt(
    raw_prompt: str,
    topic: str = "",
    difficulty: str = "Intermediate",
    goal: str = "Comprehensive conceptual understanding",
    audience: str = "College student",
    output_format: str = "Structured sections with definition, steps, example, and takeaways",
    constraints: str = "Accurate facts, no hallucinations, concise academic depth",
    language: str = "English",
) -> Dict[str, Any]:
    """Optimize a user's basic study prompt into an engineered prompt using Gemini.

    Args:
        raw_prompt: The initial prompt supplied by user.
        topic: Specific subject matter context.
        difficulty: Beginner, Intermediate, or Advanced.
        goal: Study objective.
        audience: Intended learner persona.
        output_format: Desired formatting requirements.
        constraints: Guardrails and limits.
        language: English or Hinglish.

    Returns:
        Dict with keys:
          - optimized_prompt
          - role_assigned
          - task_clarified
          - constraints_added
          - explanation_of_improvements
    """
    if not topic.strip():
        topic = raw_prompt[:50]

    lang_note = LANG_NOTE.get(language, "")

    formatted_prompt = OPTIMIZER_PROMPT.format(
        raw_prompt=raw_prompt,
        topic=topic,
        difficulty=difficulty,
        goal=goal,
        audience=audience,
        output_format=output_format,
        constraints=constraints,
        language_note=lang_note,
    )

    raw_response = call_gemini(
        prompt=formatted_prompt,
        system_instruction=OPTIMIZER_SYSTEM_PROMPT,
        temperature=0.5,
        response_mime_type="application/json",
    )

    try:
        data = parse_json_response(raw_response)
        return {
            "optimized_prompt": data.get("optimized_prompt", raw_response),
            "role_assigned": data.get("role_assigned", "Academic Mentor & Domain Specialist"),
            "task_clarified": data.get("task_clarified", "Clarified objectives and step-by-step instructions"),
            "constraints_added": data.get("constraints_added", "Enforced length limits, tone control, and accuracy requirements"),
            "explanation_of_improvements": data.get(
                "explanation_of_improvements",
                "The optimized prompt provides clear structural guardrails, assigns an expert role, defines target audience depth, and enforces verifiable takeaways."
            ),
        }
    except Exception:
        # Fallback if model returned plain text instead of JSON
        return {
            "optimized_prompt": raw_response,
            "role_assigned": "Academic Domain Expert",
            "task_clarified": "Enhanced with structured learning requirements",
            "constraints_added": "Standard academic guardrails applied",
            "explanation_of_improvements": (
                "Transformed the raw prompt with explicit role framing, target depth constraints, "
                "and structured learning milestones for optimal model reasoning."
            ),
        }
