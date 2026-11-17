# PromptWise: AI Study Assistant Using Prompt Engineering
Team Cognivance | SCSE4041 Prompt Engineering Mini Project (Milestone 2)

PromptWise turns a topic, academic level, task and language into level-appropriate study material
(explanation, revision notes, quiz, marks-based exam answer) and grades quiz answers with targeted revision.

**Prototype link:** [FILL: deployed Streamlit app link]
**Reel link:** [FILL: reel link]

## Team
| Enrollment no. | Name | Role |
|---|---|---|
| S24CSEU0166 | Vanshika Beniwal (Team Leader) | Prompt design |
| S24CSEU0241 | Yaditi Arora | App building and deployment |
| S24CSEU0340 | Mohita Purohit | Testing, reel and documents |

## How to open or run
**Online:** open the prototype link above. No login is needed.

**Locally:**
1. `python3 -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add your own Gemini API key (free from https://aistudio.google.com). Never commit this file.
4. From the repository root run: `streamlit run code/app.py`

## Folder structure
- `prompts/v1` to `prompts/v4`: older prompt versions, `prompts/final`: the six final prompts (P1 to P6), one file each
- `code/app.py`: Streamlit app (reads the prompts from `prompts/final`)
- `test-data/`: test inputs, saved outputs, screenshots
- `docs/`: diagrams, `m2_data.py` and `build_m2_pdf.py` (build the Milestone 2 PDF), the Milestone 2 PDF
- `CHANGELOG.md`: dated changes since Milestone 1

Model: Gemini 4 Hydrogen via the Gemini API (Google AI Studio).
