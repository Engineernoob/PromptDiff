# Prompt Diff — Behavioral Prompt Analyzer

Prompt Diff is a lightweight web tool that analyzes how changes between two prompts
impact an LLM’s behavior. Instead of focusing on surface-level text differences,
it highlights _meaningful behavioral shifts_ that affect cost, reliability, and
model safety.

👉 **Live Demo:** https://your-render-url-here  
👉 Built with **FastAPI**, **Jinja2**, and a clean minimal UI.

---

## ✨ Features

- 🔍 **Behavioral Impact Analysis**  
  Detects how prompt edits change model constraints, certainty, and tone.

- 💬 **Risk Score (0–10)**  
  A heuristic scoring system that captures common LLM failure modes such as  
  under-specification, overconfidence, missing roles, or weak constraints.

- 🧠 **Risk Banding**  
  Labels prompts as **Low**, **Moderate**, or **High** risk depending on their
  likelihood of causing drift or hallucination.

- 📉 **Token Delta Reporting**  
  Shows how edits affect cost + latency.

- 🎨 **Clean Web UI**  
  A sleek, distraction-free interface for fast comparisons.

---

## 🖼️ UI Preview

_(Add a screenshot here after deployment)_

---

## 🚀 Running Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Start the server
   uvicorn app:app --reload

3. Visit the app
   http://127.0.0.1:8000

🗂️ Project Structure
prompt-diff/
├── app.py
├── requirements.txt
├── templates/
│ └── index.html
└── static/
└── style.css

💡 Why I Built This

Prompt engineering tools often treat prompts as plain text.
Prompt Diff treats prompts like code — where small changes matter.

This tool helps you:

Design safer prompts

Reduce hallucination risk

Understand how constraints guide AI behavior

Iterate prompts with intention

📄 License

MIT
