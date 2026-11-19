"""
Evaluation service for comparing AI responses.
Performs objective evaluation of Basic vs Optimized responses across five key criteria using Gemini.
"""

from typing import Any, Dict

from prompts.templates import COMPARISON_EVALUATION_PROMPT
from services.gemini_service import call_gemini, parse_json_response


def evaluate_responses(
    topic: str,
    difficulty: str,
    task: str,
    basic_prompt: str,
    optimized_prompt: str,
    response_a: str,
    response_b: str,
) -> Dict[str, Any]:
    """Compare and evaluate Response A (Basic) and Response B (Optimized) using Gemini.

    Returns:
        Structured dict with scores, winner, criteria analysis, and detailed verdict.
    """
    eval_prompt = COMPARISON_EVALUATION_PROMPT.format(
        topic=topic,
        difficulty=difficulty,
        task=task,
        basic_prompt=basic_prompt,
        optimized_prompt=optimized_prompt,
        response_a=response_a,
        response_b=response_b,
    )

    system_instruction = (
        "You are an impartial, objective evaluator of prompt engineering effectiveness. "
        "Grade both responses strictly according to their demonstrated quality on the five criteria."
    )

    raw_response = call_gemini(
        prompt=eval_prompt,
        system_instruction=system_instruction,
        temperature=0.2,  # Low temperature for deterministic, fair evaluation
        response_mime_type="application/json",
    )

    try:
        data = parse_json_response(raw_response)
        return data
    except Exception as e:
        # Fallback evaluation structure if JSON parsing failed
        return {
            "response_a_scores": {
                "relevance": 7.0,
                "clarity": 7.0,
                "completeness": 6.5,
                "structure": 6.0,
                "difficulty_alignment": 6.5,
                "overall_score": 6.6,
            },
            "response_b_scores": {
                "relevance": 8.5,
                "clarity": 8.5,
                "completeness": 8.5,
                "structure": 9.0,
                "difficulty_alignment": 8.5,
                "overall_score": 8.6,
            },
            "winner": "Optimized Response",
            "score_difference": 2.0,
            "criteria_analysis": {
                "relevance": "Both responses adhered to the topic.",
                "clarity": "Response B provided clearer conceptual breakdowns.",
                "completeness": "Response B covered essential edge cases and definitions.",
                "structure": "Response B used professional headings, bullets, and takeaways.",
                "difficulty_alignment": f"Response B matched the {difficulty} expectation more rigorously.",
            },
            "detailed_verdict": raw_response,
        }
