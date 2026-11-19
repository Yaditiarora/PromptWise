"""
Prompt templates for PromptWise.
Preserves existing prompt files from prompts/final while providing
enhanced templates for Prompt Optimizer, Study Modes, and Response Comparison.
"""

from pathlib import Path

PROMPT_FINAL_DIR = Path(__file__).resolve().parent.parent.parent / "prompts" / "final"


def load_file(name: str) -> str:
    """Load prompt file from prompts/final."""
    path = PROMPT_FINAL_DIR / name
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


# Existing baseline prompts
SYSTEM_PROMPT = load_file("P1_system.txt") or (
    "You are PromptWise, an AI study assistant for school and college students.\n"
    "Only help with academic study topics. If the request is not an academic topic "
    "(entertainment, personal advice, harmful requests), politely refuse and ask for a study topic.\n"
    "Be accurate. If you are unsure about a fact, say so instead of guessing.\n"
    "Never ask for names, contact details or personal data."
)

EXPLAIN_PROMPT = load_file("P2_explain.txt")
NOTES_PROMPT = load_file("P3_notes.txt")
QUIZ_PROMPT = load_file("P4_quiz.txt")
MARKS_PROMPT = load_file("P5_marks_answer.txt")
GRADE_PROMPT = load_file("P6_grading.txt")

# Language instructions
LANG_NOTE = {
    "English": "",
    "Hinglish": (
        "\n\nLanguage Instruction: Respond in natural, conversational Hinglish (Roman script). "
        "Keep technical terminology, formulas, and definitions in English for academic clarity."
    ),
}

# Difficulty instructions
DIFFICULTY_GUIDELINES = {
    "Beginner": (
        "Target Level: Beginner (School / Introductory).\n"
        "- Language: Clear, simple, accessible vocabulary without overwhelming jargon.\n"
        "- Conceptual Depth: Focus on fundamental concepts, intuitive analogies, and real-life connections.\n"
        "- Structure: Step-by-step progression from simple to concrete ideas."
    ),
    "Intermediate": (
        "Target Level: Intermediate (Undergraduate / College).\n"
        "- Language: Academically precise with appropriate domain terminology.\n"
        "- Conceptual Depth: Deeper mechanisms, practical applications, cause-and-effect relationships.\n"
        "- Structure: Thorough conceptual breakdown with relevant engineering/scientific examples."
    ),
    "Advanced": (
        "Target Level: Advanced (Postgraduate / Specialized).\n"
        "- Language: Rigorous technical terminology, high formal precision.\n"
        "- Conceptual Depth: Theoretical underpinnings, nuances, edge cases, advanced applications.\n"
        "- Structure: In-depth analytical critique, architectural reasoning, and mathematical/formal foundations."
    ),
}

# ----------------- PROMPT OPTIMIZER TEMPLATES -----------------

OPTIMIZER_SYSTEM_PROMPT = (
    "You are PromptWise's Senior Prompt Engineer and Educational Architect. "
    "Your objective is to transform raw, vague, or basic user study prompts into "
    "high-performance, professionally engineered prompts optimized for LLM reasoning and academic mastery."
)

OPTIMIZER_PROMPT = """You are an expert prompt engineer. Transform the following basic prompt into an optimal, production-grade prompt for an AI study assistant.

User's Original Prompt:
"{raw_prompt}"

Additional Context & Parameters:
- Topic: {topic}
- Target Difficulty: {difficulty}
- Study Goal: {goal}
- Target Audience: {audience}
- Desired Output Format: {output_format}
- Specific Constraints & Requirements: {constraints}
{language_note}

Instructions for Optimization:
Create an engineered prompt that contains ALL of the following 7 core components:
1. Clear Role Assignment (e.g., world-class academic tutor or domain specialist)
2. Specific Task Instructions (exact actionable steps)
3. Topic Context & Background
4. Target Audience & Educational Level
5. Difficulty Level Specification
6. Output Format & Structure (clear sections, markdown formatting, tables/bullets)
7. Constraints & Guardrails (accuracy, tone, length bounds, what to avoid)

Output your response in the following strict JSON format:
```json
{{
  "optimized_prompt": "<The full, ready-to-run optimized prompt text with all 7 components integrated cleanly>",
  "role_assigned": "<Brief summary of the role assigned>",
  "task_clarified": "<Brief summary of how the task was sharpened>",
  "constraints_added": "<List of constraints and guardrails introduced>",
  "explanation_of_improvements": "<A clear explanation of why this prompt outperforms the original basic prompt and what was improved>"
}}
```
Provide only valid JSON.
"""

# ----------------- STUDY MODES ENHANCED TEMPLATES -----------------

# Mode A: Explain
ENHANCED_EXPLAIN_PROMPT = """You are an expert academic educator. Provide a comprehensive yet crystal-clear explanation of the topic "{topic}".

{difficulty_guideline}
{language_note}

Please format your response strictly using these Markdown sections:
# 📖 {topic}

### 1. 🎯 Definition & Core Concept
Provide an exact, memorable definition and explain what this concept fundamentally is in 2-3 sentences.

### 2. 🔍 Step-by-Step Explanation
Break down how it works step-by-step:
- **Phase 1 / Step 1**: Clear breakdown
- **Phase 2 / Step 2**: Clear breakdown
- **Phase 3 / Step 3**: Clear breakdown

### 3. 💡 Real-World Examples & Analogies
Provide at least one vivid real-life example or intuitive analogy that makes this instantly relatable.

### 4. 🔑 Key Takeaways
- Bullet point 1: Crucial rule or takeaway
- Bullet point 2: Common misconception or insight
- Bullet point 3: Practical significance
"""

# Mode B: Summarize / Notes
ENHANCED_SUMMARIZE_PROMPT = """You are an expert academic study assistant. Generate concise, high-impact revision notes for the topic "{topic}".

{difficulty_guideline}
{language_note}

Please format your response strictly using these Markdown sections:
# 📝 Revision Notes: {topic}

### 1. 📌 Core Concepts & Key Definitions
Highlight the critical terms in **bold** with crisp 1-2 sentence definitions.

### 2. ⚡ Essential Principles & Bullet Points
- Key principle 1
- Key principle 2
- Key principle 3
- Important formulas, laws, or structural mechanisms (if applicable)

### 3. 📊 Important Facts & Relationships
Comparison points, advantages/disadvantages, or operational characteristics.

### 4. 🧠 Quick Revision Summary & Memory Tip
A concise 2-3 sentence wrap-up plus a clever mnemonic or mental model for instant exam recall.
"""

# Mode C: Interactive Quiz
STRUCTURED_QUIZ_PROMPT = """You are an expert exam creator. Generate an interactive 5-question multiple choice quiz on the topic "{topic}".

{difficulty_guideline}
{language_note}

Requirements:
- Exactly 5 multiple-choice questions.
- Each question must test understanding, not trivial trivia.
- Exactly 4 distinct options per question labelled "A", "B", "C", and "D".
- Specify the single correct option letter ("A", "B", "C", or "D").
- Provide a clear, educational explanation for why that answer is correct.

Output your response strictly as valid JSON matching this schema:
```json
{{
  "topic": "{topic}",
  "difficulty": "{difficulty}",
  "questions": [
    {{
      "id": 1,
      "question": "<Question text>",
      "options": {{
        "A": "<Option A text>",
        "B": "<Option B text>",
        "C": "<Option C text>",
        "D": "<Option D text>"
      }},
      "correct_answer": "A",
      "explanation": "<Educational explanation of the correct answer>"
    }}
  ]
}}
```
Return only valid JSON.
"""

# Mode D: Flashcards
STRUCTURED_FLASHCARDS_PROMPT = """You are an expert learning specialist using spaced repetition techniques.
Generate a deck of 6 interactive study flashcards on the topic "{topic}".

{difficulty_guideline}
{language_note}

Requirements:
- Exactly 6 flashcards.
- Each card has a "front" (a clear question, core term, or conceptual scenario to test) and a "back" (a clear, concise, high-yield explanation with the key answer and memory cue).
- Progress from foundational concepts to practical/applied concepts.

Output your response strictly as valid JSON matching this schema:
```json
{{
  "topic": "{topic}",
  "difficulty": "{difficulty}",
  "flashcards": [
    {{
      "id": 1,
      "front": "<Question or concept prompt on the front of the card>",
      "back": "<Clear, concise answer and explanation on the back of the card>",
      "category": "<e.g., Definition, Mechanism, Application, or Formula>"
    }}
  ]
}}
```
Return only valid JSON.
"""

# Mode E: Practice Test
STRUCTURED_TEST_PROMPT = """You are an academic examiner creating a rigorous practice test on the topic "{topic}".

Number of questions requested: {num_questions}
{difficulty_guideline}
{language_note}

Requirements:
- Generate {num_questions} questions mixing:
  1. Multiple Choice Questions (with 4 options A, B, C, D)
  2. Conceptual / Short Scenario Questions (marked type="short_answer")
- Each question must include an answer key, rubric criteria, and comprehensive explanation.

Output your response strictly as valid JSON matching this schema:
```json
{{
  "topic": "{topic}",
  "difficulty": "{difficulty}",
  "total_marks": {num_questions},
  "suggested_time_minutes": {suggested_time},
  "questions": [
    {{
      "id": 1,
      "type": "mcq",
      "question": "<Question prompt>",
      "options": {{
        "A": "<Option A>",
        "B": "<Option B>",
        "C": "<Option C>",
        "D": "<Option D>"
      }},
      "correct_answer": "A",
      "explanation": "<Why this is correct>"
    }},
    {{
      "id": 2,
      "type": "short_answer",
      "question": "<Scenario or conceptual question>",
      "sample_answer": "<Ideal model answer for evaluation>",
      "explanation": "<Key grading points and reasoning>"
    }}
  ]
}}
```
Return only valid JSON.
"""

# Test Evaluation Prompt
TEST_EVALUATION_PROMPT = """You are an objective academic evaluator grading a student's practice test on the topic "{topic}".

Test Content and Answer Key:
{test_content}

Student's Submitted Answers:
{student_answers}

Grade the test accurately and fairly:
- For MCQs, check against the exact correct answer.
- For Short Answer questions, evaluate conceptual accuracy, completeness, and understanding.
- Calculate the total score out of {total_questions}.
- Highlight strengths, specific misconceptions, and a 3-bullet personalized study prescription.

Output your response in Markdown with clear sections:
# 📊 Test Results: {topic}
### 🏆 Overall Score: [Score] / {total_questions} ([Percentage]%)
### 📝 Detailed Question Breakdown
(Per question: Question, Your Answer, Correct Answer, Result [✅ Correct / ❌ Incorrect], Explanation)
### 💡 Strengths & Weak Areas
### 🚀 Actionable Revision Plan
"""

# ----------------- RESPONSE COMPARISON TEMPLATES -----------------

COMPARISON_EVALUATION_PROMPT = """You are an impartial, expert AI evaluator and prompt engineering researcher.
You are tasked with conducting an objective, rigorous comparison between two AI-generated study responses:

TOPIC: "{topic}"
DIFFICULTY: "{difficulty}"
STUDY TASK: "{task}"

ORIGINAL USER PROMPT:
"{basic_prompt}"

OPTIMIZED PROMPT:
"{optimized_prompt}"

---
RESPONSE A (Generated from Basic Prompt):
{response_a}
---

---
RESPONSE B (Generated from Optimized Prompt):
{response_b}
---

Evaluate BOTH responses thoroughly across five dimensions on a scale of 1 to 10:
1. Relevance: Direct adherence to the topic and user intent.
2. Clarity: Readability, flow, accessibility of explanations.
3. Completeness: Depth, coverage of necessary concepts, lack of critical omissions.
4. Structure: Formatting, organization, logical headings, ease of scanning.
5. Difficulty Alignment: How accurately the depth matches the target difficulty level ({difficulty}).

Important:
- Evaluate objectively based on actual content quality.
- Do NOT automatically score Response B higher if Response A was genuinely better or equal.
- Calculate an overall score out of 10 for each response (weighted average of the criteria).
- Explain precisely why one response performed better with concrete evidence from the outputs.

Output your evaluation strictly as valid JSON matching this schema:
```json
{{
  "response_a_scores": {{
    "relevance": 8,
    "clarity": 7,
    "completeness": 6,
    "structure": 6,
    "difficulty_alignment": 7,
    "overall_score": 6.8
  }},
  "response_b_scores": {{
    "relevance": 9,
    "clarity": 9,
    "completeness": 9,
    "structure": 9,
    "difficulty_alignment": 9,
    "overall_score": 9.0
  }},
  "winner": "Optimized Response",
  "score_difference": 2.2,
  "criteria_analysis": {{
    "relevance": "<Comparison on relevance>",
    "clarity": "<Comparison on clarity>",
    "completeness": "<Comparison on completeness>",
    "structure": "<Comparison on structure>",
    "difficulty_alignment": "<Comparison on difficulty alignment>"
  }},
  "detailed_verdict": "<Comprehensive explanation of why the winner performed better and what specific prompt engineering techniques made the difference>"
}}
```
Provide only valid JSON.
"""
