# Changelog (since Milestone 1)

- 2026-11-19: Major Production Upgrade:
  - Redesigned UI/UX into a modern AI SaaS interface with custom dark navy and purple design system.
  - Implemented 6-page sidebar navigation (Dashboard, Study Assistant, Prompt Optimizer, Compare Responses, Prompt History, About Project).
  - Added dedicated Prompt Optimizer integrating all 7 prompt engineering pillars with dynamic Gemini generation.
  - Upgraded Study Assistant to 5 specialized interactive modes: Explain, Summarize, Interactive Quiz with scoring, Flashcards with 3D flip & mastery tracking, and Timed Practice Test with auto-evaluation.
  - Maintained full backwards compatibility with marks-based exam answers and bilingual English/Hinglish options.
  - Built "Compare Responses" feature evaluating basic vs optimized prompts across 5 objective criteria with Gemini.
  - Implemented persistent SQLite database for Prompt History with search, filter, preview, deletion, and metrics.
  - Modularized codebase into `services/`, `views/`, `ui/`, `prompts/`, and `data/`.
  - Added automated end-to-end test suite (`code/test_promptwise_suite.py`) and verified all features with `gemini-3.5-flash-lite`.
- 2026-11-17: Created the repository structure; wrote final prompts P1 to P6 and older versions v1 to v4; wrote the Streamlit app (code/app.py); drew the four diagrams; added the Milestone 2 PDF builder.
- [FILL: date]: Ran the app locally with the Gemini API key and fixed errors.
- [FILL: date]: Ran the 12 tests and saved outputs and screenshots in test-data/.
- [FILL: date]: Deployed the app on Streamlit Community Cloud.
- [FILL: date]: Recorded the reel and submitted Milestone 2.
