# 📚 PromptWise: AI-Powered Study Assistant

> **"Learn Smarter. Prompt Better."**  
> SCSE4041 Prompt Engineering Mini Project • Team Cognivance • Milestone 2 Upgrade

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://promptwise-a7i9rzr9og3ef8hqi26nub.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Gemini API](https://img.shields.io/badge/Model-Gemini%203.5%20Flash%20Lite-8E75C4?logo=google&logoColor=white)](https://aistudio.google.com)

**🌐 Live Application:** [https://promptwise-a7i9rzr9og3ef8hqi26nub.streamlit.app/](https://promptwise-a7i9rzr9og3ef8hqi26nub.streamlit.app/)

PromptWise is a production-grade, AI-powered study platform built with **Python**, **Streamlit**, and **Google's Gemini API**. It demonstrates the empirical superiority of structured prompt engineering by converting vague, ambiguous user prompts into high-yield, academically sound study materials with interactive learning, adaptive difficulty levels, empirical response benchmarking, and persistent history.

---

## 👥 Team Cognivance

| Enrollment No. | Student Name | Role | Responsibilities |
|---|---|---|---|
| **S24CSEU0166** | **Vanshika Beniwal** (Team Leader) | Prompt Architect | Prompt engineering design, 7-component template architecture, academic rubric calibration |
| **S24CSEU0241** | **Yaditi Arora** | Full-Stack & AI Engineer | App architecture, Streamlit UI/UX redesign, Gemini API integration, SQLite service |
| **S24CSEU0340** | **Mohita Purohit** | QA & Product Analyst | Testing suite, response benchmarking analysis, documentation, and video reel |

---

## 🌟 Key Features

### 1. Modern SaaS UI/UX Redesign
- **Design System:** Dark navy and purple/indigo palette (`#0B0F19`, `#1E1B4B`, `#8B5CF6`) with glowing card borders and responsive typography.
- **Sidebar Navigation:** 6 dedicated pages (Dashboard, Study Assistant, Prompt Optimizer, Compare Responses, Prompt History, About Project).
- **Responsive Layout:** Dynamic multi-column layout with loading status spinners, score indicators, and clean alerts.

### 2. Prompt Optimizer (Dynamic AI Engineering)
- Transforms basic prompts (e.g., *"Explain photosynthesis"*) into production-grade prompts.
- Integrates all **7 Prompt Engineering Pillars**:
  1. Clear Role Assignment (world-class academic educator)
  2. Specific Task Instructions (structured steps)
  3. Topic Context & Background
  4. Target Audience Calibrated Depth
  5. Difficulty Level Specification
  6. Output Formatting (definitions, bullets, takeaways)
  7. Strict Guardrails & Negative Constraints (no hallucinations)
- Displays **Original Prompt** and **Optimized Prompt** side-by-side with one-click code copy and explanation of improvements.

### 3. Multiple Adaptive Study Modes
All 5 modes operate dynamically using the configured Gemini model (`gemini-3.5-flash-lite`):
- **📖 Explain:** Concept definitions, progressive step-by-step breakdowns, real-world analogies, and core takeaways.
- **📝 Summarize (Revision Notes):** High-yield bullet points, critical terminology in bold, operational formulas, and memorable mnemonic tips.
- **❓ Interactive Quiz:** 5 multiple-choice questions with 4 options (A-D), interactive radio selection, instant automatic evaluation, color-coded answer badges, and scoring.
- **🗂️ Interactive Flashcards:** 3D flip card toggle (reveal answer), Previous/Next navigation, progress bar, shuffle functionality, and mastery tracking (*Mastered* vs *Needs Revision*).
- **⏱️ Practice Test:** Timed practice exam with configurable question count (5, 8, 10), mixed question formats (MCQs + short conceptual answers), elapsed timer, submit button, and automated Gemini evaluation.
- **📝 Exam Answer (Marks-based):** Preserved existing capability for 2-mark, 5-mark, and 10-mark structured exam answers.
- **🌐 Bilingual Options:** English and conversational Roman-script Hinglish with English technical terms preserved.

### 4. Difficulty Adaptation
- **Beginner:** Accessible vocabulary, intuitive metaphors, step-by-step foundation without jargon.
- **Intermediate:** Academically precise language, deeper mechanisms, practical use cases.
- **Advanced:** Rigorous domain terminology, theoretical subtleties, architectural reasoning, and edge cases.

### 5. Compare Responses (A/B Empirical Evaluation)
- Benchmarks **Basic Unengineered Response** vs. **Optimized Prompt Response** side-by-side.
- Evaluates both responses objectively across 5 core dimensions (scored 1 to 10):
  1. *Relevance*
  2. *Clarity*
  3. *Completeness*
  4. *Structure*
  5. *Difficulty Alignment*
- Transparent overall score out of 10 and in-depth comparative rationale showing why prompt engineering elevated the output.

### 6. Persistent SQLite Prompt History
- Persistent local SQLite storage in `code/data/history.db`.
- Saves topic, study mode, difficulty level, original prompt, optimized prompt, generated response, and timestamp.
- **Features:** Real-time search, multi-factor filtering by mode and difficulty, full inspection modal/expander, prompt copy, single entry deletion, and bulk clear with confirmation.
- Survives browser refreshes and server restarts without exposing API keys.

---

## 🏛️ System Architecture

```
PromptWise/
├── .streamlit/
│   ├── secrets.toml            # Secure API keys (gitignored)
│   └── secrets.toml.example    # Configuration template
├── code/
│   ├── app.py                  # Main Streamlit application entry point
│   ├── services/
│   │   ├── gemini_service.py   # Google GenAI client, retry, model fallback, JSON parsing
│   │   ├── db_service.py       # SQLite database persistence & queries
│   │   ├── prompt_optimizer_service.py # Dynamic prompt engineering service
│   │   └── evaluation_service.py # Multi-criteria response evaluation
│   ├── prompts/
│   │   └── templates.py        # Centralized prompt engineering templates
│   ├── views/
│   │   ├── dashboard.py        # Overview dashboard with metrics & quick launch
│   │   ├── study_assistant.py  # 5 interactive study modes + exam marks
│   │   ├── optimizer.py        # Prompt Optimizer view
│   │   ├── comparator.py       # Basic vs Optimized Response Comparison
│   │   ├── history.py          # SQLite-backed search & filter history
│   │   └── about.py            # Architectural & team documentation
│   ├── ui/
│   │   ├── styles.py           # SaaS dark navy & purple CSS design system
│   │   └── components.py       # Reusable badges, cards, hero headers
│   ├── data/
│   │   └── history.db          # SQLite persistent database (gitignored)
│   └── test_promptwise_suite.py # Automated end-to-end verification suite
├── prompts/final/              # Baseline prompt files (P1 to P6)
├── test-data/                  # Test inputs and outputs
├── requirements.txt            # Python dependencies (Streamlit & google-genai)
├── CHANGELOG.md                # Milestone changelog
└── README.md                   # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ (tested through 3.14)
- Google Gemini API Key (free from [Google AI Studio](https://aistudio.google.com/))

### Local Installation
1. **Clone or navigate to the repository:**
   ```bash
   cd PromptWise
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your Gemini API key:**
   Create `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your-actual-gemini-api-key-here"
   ```

5. **Run the application:**
   ```bash
   streamlit run code/app.py
   ```
   Open your browser to `http://localhost:8501`.

---

## 🧪 Testing and Verification

Run the automated test suite covering all modules, database operations, JSON resilience, prompt templates, and live Gemini API generation:

```bash
python code/test_promptwise_suite.py
```

### Verified Test Results:
- `[TEST 1] Database Persistence & CRUD` ✅ Passed
- `[TEST 2] JSON Parser & Escape Sequence Resilience` ✅ Passed
- `[TEST 3] Prompt Templates & 3 Difficulty Levels` ✅ Passed
- `[TEST 4] Live Gemini API Integration (gemini-3.5-flash-lite)` ✅ Passed
- `[TEST 5] Live Prompt Optimizer with Gemini` ✅ Passed
- `[TEST 6] Live 5 Study Modes (Explain, Summarize, Quiz, Flashcards, Test)` ✅ Passed
- `[TEST 7] Live Basic vs Optimized Response Comparison & 5-Dimension Evaluation` ✅ Passed

---

## ☁️ Deployment on Streamlit Community Cloud

1. Push your repository to GitHub (ensure `.streamlit/secrets.toml` and `*.db` are in `.gitignore`).
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io).
3. Click **"New App"** and select your repository and branch.
4. Set the **Main file path** to `code/app.py`.
5. Under **Advanced Settings** -> **Secrets**, paste your key:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   ```
6. Click **Deploy!**

---

## 🔒 Security Notice
- API keys are **never** committed to version control or printed in code or frontend UI.
- All secrets are managed strictly through Streamlit Secrets (`st.secrets["GEMINI_API_KEY"]`).
- SQLite history stores educational text only and strictly excludes credentials or private data.
