"""
Comprehensive Test Suite for PromptWise.
Tests all five study modes, difficulty levels, prompt optimization,
response comparison, database persistence, edge cases, and Gemini API calls.
"""

import json
import os
import sys
import time
import tomllib
from pathlib import Path

# Add 'code' directory to path
CODE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CODE_DIR.parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

# Set working directory to project root so streamlit finds .streamlit/secrets.toml
os.chdir(PROJECT_ROOT)
import streamlit as st

from prompts.templates import (
    DIFFICULTY_GUIDELINES,
    ENHANCED_EXPLAIN_PROMPT,
    ENHANCED_SUMMARIZE_PROMPT,
    LANG_NOTE,
    MARKS_PROMPT,
    STRUCTURED_FLASHCARDS_PROMPT,
    STRUCTURED_QUIZ_PROMPT,
    STRUCTURED_TEST_PROMPT,
)
from services import db_service
from services.evaluation_service import evaluate_responses
from services.gemini_service import (
    call_gemini,
    clean_json_string,
    is_client_ready,
    parse_json_response,
)
from services.prompt_optimizer_service import optimize_prompt


def test_database_persistence():
    print("\n--- [TEST 1] Testing Database Persistence & CRUD ---")
    db_service.init_db()

    # 1. Add session
    row_id = db_service.add_history(
        topic="Mealy and Moore Machines",
        study_mode="Explain",
        difficulty="Intermediate",
        original_prompt="Explain Mealy and Moore machines",
        optimized_prompt="Role: Hardware Architect...",
        generated_response="Mealy machines depend on input and state...",
        metadata={"test": True},
    )
    assert row_id > 0, f"Failed to insert row, got {row_id}"
    print(f"✓ Inserted history row with ID: {row_id}")

    # 2. Retrieve session by ID
    item = db_service.get_history_by_id(row_id)
    assert item is not None, "Failed to retrieve by ID"
    assert item["topic"] == "Mealy and Moore Machines"
    assert item["difficulty"] == "Intermediate"
    assert item["metadata"]["test"] is True
    print("✓ Successfully retrieved and verified session by ID")

    # 3. Filter by mode and difficulty
    records = db_service.get_history(mode_filter="Explain", difficulty_filter="Intermediate")
    assert any(r["id"] == row_id for r in records), "Mode/difficulty filter failed"
    print("✓ Mode and difficulty filtering verified")

    # 4. Keyword search
    search_records = db_service.get_history(search_query="Moore")
    assert any(r["id"] == row_id for r in search_records), "Search query failed"
    print("✓ Full-text keyword search verified")

    # 5. Stats computation
    stats = db_service.get_history_stats()
    assert stats["total_sessions"] >= 1
    assert "Explain" in stats["mode_counts"]
    print(f"✓ Database stats verified: {stats['total_sessions']} total sessions")

    # 6. Delete test row
    deleted = db_service.delete_history(row_id)
    assert deleted is True, "Failed to delete test row"
    assert db_service.get_history_by_id(row_id) is None
    print("✓ Delete history entry verified")


def test_json_parsing_and_resilience():
    print("\n--- [TEST 2] Testing JSON Parser & Resilience ---")
    raw_markdown_json = """```json
    {
        "status": "success",
        "value": 42
    }
    ```"""
    parsed = parse_json_response(raw_markdown_json)
    assert parsed.get("status") == "success"
    assert parsed.get("value") == 42
    print("✓ Successfully parsed markdown fenced JSON")

    embedded_json = "Here is your response:\n{\"quiz\": \"active\", \"score\": 10}\nHope this helps!"
    parsed2 = parse_json_response(embedded_json)
    assert parsed2.get("quiz") == "active"
    print("✓ Successfully extracted embedded JSON without code fences")


def test_prompt_formatting():
    print("\n--- [TEST 3] Testing Prompt Templates & Difficulty Formats ---")
    for diff in ["Beginner", "Intermediate", "Advanced"]:
        diff_guide = DIFFICULTY_GUIDELINES[diff]
        # Explain
        p_exp = ENHANCED_EXPLAIN_PROMPT.format(
            topic="Photosynthesis",
            difficulty_guideline=diff_guide,
            language_note=LANG_NOTE["English"],
        )
        assert "Photosynthesis" in p_exp
        assert diff in diff_guide

        # Summarize
        p_sum = ENHANCED_SUMMARIZE_PROMPT.format(
            topic="Binary Trees",
            difficulty_guideline=diff_guide,
            language_note=LANG_NOTE["Hinglish"],
        )
        assert "Binary Trees" in p_sum
        assert "Hinglish" in p_sum

        # Marks prompt
        for m in [2, 5, 10]:
            p_marks = MARKS_PROMPT.format(
                topic="Operating Systems",
                level=diff,
                marks=m,
                language_note="",
            )
            assert f"{m}-mark" in p_marks

    print("✓ All 3 difficulty levels, marks-based prompts, and bilingual instructions verified")


def test_live_gemini_api():
    print("\n--- [TEST 4] Testing Live Gemini API Integration ---")
    ready, msg = is_client_ready()
    print(f"Client readiness: {ready} ({msg})")
    assert ready is True, msg

    # Quick prompt
    resp = call_gemini("Say 'PROMPTWISE_READY' in one word.")
    assert "PROMPTWISE_READY" in resp or len(resp) > 0
    print(f"✓ Basic Gemini ping response: {resp.strip()}")


def test_live_prompt_optimizer():
    print("\n--- [TEST 5] Testing Live Prompt Optimizer with Gemini ---")
    time.sleep(3.0)
    raw_prompt = "Explain photosynthesis."
    result = optimize_prompt(
        raw_prompt=raw_prompt,
        topic="Photosynthesis",
        difficulty="Beginner",
        goal="School exam prep",
        audience="High School Student",
        output_format="Structured sections with definition, steps, example, and takeaways",
        constraints="Under 200 words, no hallucination",
        language="English",
    )
    assert "optimized_prompt" in result, "Missing optimized_prompt in result"
    assert len(result["optimized_prompt"]) > len(raw_prompt), "Optimized prompt was not expanded"
    assert "explanation_of_improvements" in result, "Missing explanation"
    print(f"✓ Live Prompt Optimizer succeeded!")
    print(f"  Role: {result.get('role_assigned')}")
    print(f"  Optimized Prompt Length: {len(result['optimized_prompt'])} chars")


def test_live_study_modes():
    print("\n--- [TEST 6] Testing Live Study Modes with Gemini ---")
    topic = "Mealy and Moore machines"

    # 1. Mode A: Explain
    print("Testing Mode A: Explain...")
    time.sleep(3.0)
    prompt_exp = ENHANCED_EXPLAIN_PROMPT.format(
        topic=topic,
        difficulty_guideline=DIFFICULTY_GUIDELINES["Intermediate"],
        language_note="",
    )
    res_exp = call_gemini(prompt_exp)
    assert "Mealy" in res_exp or "Moore" in res_exp
    print(f"✓ Explain generated ({len(res_exp)} chars)")

    # 2. Mode B: Summarize
    print("Testing Mode B: Summarize...")
    time.sleep(3.0)
    prompt_sum = ENHANCED_SUMMARIZE_PROMPT.format(
        topic=topic,
        difficulty_guideline=DIFFICULTY_GUIDELINES["Intermediate"],
        language_note="",
    )
    res_sum = call_gemini(prompt_sum)
    assert len(res_sum) > 50
    print(f"✓ Summarize generated ({len(res_sum)} chars)")

    # 3. Mode C: Quiz (Structured JSON)
    print("Testing Mode C: Interactive Quiz...")
    time.sleep(3.0)
    prompt_quiz = STRUCTURED_QUIZ_PROMPT.format(
        topic=topic,
        difficulty="Intermediate",
        difficulty_guideline=DIFFICULTY_GUIDELINES["Intermediate"],
        language_note="",
    )
    raw_quiz = call_gemini(prompt_quiz, response_mime_type="application/json")
    quiz_data = parse_json_response(raw_quiz)
    assert "questions" in quiz_data
    assert len(quiz_data["questions"]) >= 3
    q1 = quiz_data["questions"][0]
    assert "options" in q1
    assert "correct_answer" in q1
    print(f"✓ Quiz generated with {len(quiz_data['questions'])} questions and options: {list(q1['options'].keys())}")

    # 4. Mode D: Flashcards (Structured JSON)
    print("Testing Mode D: Flashcards...")
    time.sleep(3.0)
    prompt_fc = STRUCTURED_FLASHCARDS_PROMPT.format(
        topic=topic,
        difficulty="Intermediate",
        difficulty_guideline=DIFFICULTY_GUIDELINES["Intermediate"],
        language_note="",
    )
    raw_fc = call_gemini(prompt_fc, response_mime_type="application/json")
    fc_data = parse_json_response(raw_fc)
    assert "flashcards" in fc_data
    assert len(fc_data["flashcards"]) >= 3
    fc1 = fc_data["flashcards"][0]
    assert "front" in fc1 and "back" in fc1
    print(f"✓ Flashcards generated with {len(fc_data['flashcards'])} cards")

    # 5. Mode E: Practice Test (Structured JSON)
    print("Testing Mode E: Practice Test...")
    time.sleep(3.0)
    prompt_test = STRUCTURED_TEST_PROMPT.format(
        topic=topic,
        num_questions=3,
        suggested_time=6,
        difficulty="Intermediate",
        difficulty_guideline=DIFFICULTY_GUIDELINES["Intermediate"],
        language_note="",
    )
    raw_test = call_gemini(prompt_test, response_mime_type="application/json")
    test_data = parse_json_response(raw_test)
    assert "questions" in test_data
    assert len(test_data["questions"]) >= 2
    print(f"✓ Practice Test generated with {len(test_data['questions'])} mixed questions")


def test_live_response_comparison():
    print("\n--- [TEST 7] Testing Basic vs Optimized Response Comparison with Gemini ---")
    topic = "Recursion"
    basic_prompt = "Explain recursion."
    optimized_prompt = (
        "You are an expert Computer Science Professor. Explain recursion to an undergraduate student. "
        "Define base case and recursive step with a call stack diagram and factorial example. Max 150 words."
    )
    time.sleep(3.0)
    resp_a = call_gemini(basic_prompt, system_instruction="You are a helpful assistant.", temperature=0.7)
    time.sleep(3.0)
    resp_b = call_gemini(optimized_prompt, temperature=0.7)
    time.sleep(3.0)

    eval_data = evaluate_responses(
        topic=topic,
        difficulty="Intermediate",
        task="Explain Concept",
        basic_prompt=basic_prompt,
        optimized_prompt=optimized_prompt,
        response_a=resp_a,
        response_b=resp_b,
    )
    assert "response_a_scores" in eval_data
    assert "response_b_scores" in eval_data
    sc_a = eval_data["response_a_scores"].get("overall_score", 0)
    sc_b = eval_data["response_b_scores"].get("overall_score", 0)
    print(f"✓ Comparison evaluation completed! Basic Score: {sc_a}/10 | Optimized Score: {sc_b}/10")
    print(f"  Winner: {eval_data.get('winner')}")


def main():
    print("==================================================")
    print("Starting Comprehensive PromptWise Test Suite")
    print("==================================================")

    test_database_persistence()
    test_json_parsing_and_resilience()
    test_prompt_formatting()
    test_live_gemini_api()
    test_live_prompt_optimizer()
    test_live_study_modes()
    test_live_response_comparison()

    print("\n==================================================")
    print("🎉 ALL TESTS PASSED SUCCESSFULLY! FULL SYSTEM VERIFIED")
    print("==================================================")


if __name__ == "__main__":
    main()
