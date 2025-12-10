from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def analyze(prompt: str):
    tokens = len(prompt.split())
    text = prompt.lower()

    strong_words = re.findall(r"\b(must|always|never|strict|exactly|only)\b", text)

    uncertainty_words = re.findall(r"\b(might|maybe|could|possibly|generally)\b", text)

    role_specified = bool(re.search(r"\b(you are|act as)\b", text))

    risk = 0
    reasons = []

    # 1️⃣ Role clarity (highest impact)
    if not role_specified:
        risk += 3
        reasons.append("No role specified")

    # 2️⃣ Prompt length extremes
    if tokens < 10:
        risk += 2
        reasons.append("Prompt very short → under-specified")
    elif tokens > 250:
        risk += 1
        reasons.append("Very long prompt → higher drift risk")

    # 3️⃣ Constraint balance
    if len(strong_words) == 0:
        risk += 2
        reasons.append("No hard constraints")
    elif len(strong_words) >= 4:
        risk += 1
        reasons.append("Over-constrained prompt")

    # 4️⃣ Confidence signaling
    if len(uncertainty_words) == 0:
        risk += 1
        reasons.append("No uncertainty language")
    elif len(uncertainty_words) >= 3:
        risk += 1
        reasons.append("Excessive uncertainty")

    risk = min(risk, 10)

    return {
        "tokens": tokens,
        "strong": len(strong_words),
        "uncertainty": len(uncertainty_words),
        "role": role_specified,
        "risk": risk,
        "risk_reasons": reasons,
    }


def diff(a, b):
    insights = []

    if b["tokens"] > a["tokens"]:
        insights.append("More tokens → higher cost, more context")
    elif b["tokens"] < a["tokens"]:
        insights.append("Fewer tokens → faster, less constrained")

    if b["strong"] > a["strong"]:
        insights.append("Stronger constraints → lower creativity")

    if b["role"] and not a["role"]:
        insights.append("Role clarity added → reduced hallucination risk")

    if b["uncertainty"] > a["uncertainty"]:
        insights.append("More uncertainty language → safer but less confident output")

    return insights


def risk_band(score: int):
    if score <= 3:
        return "Low"
    elif score <= 6:
        return "Moderate"
    return "High"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "insights": None,
            "delta": None,
            "risk": None,
            "risk_band": None,
            "risk_reasons": None,
        },
    )


@app.post("/", response_class=HTMLResponse)
def compare(request: Request, prompt_a: str = Form(...), prompt_b: str = Form(...)):
    analysis_a = analyze(prompt_a)
    analysis_b = analyze(prompt_b)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "insights": diff(analysis_a, analysis_b),
            "delta": analysis_b["tokens"] - analysis_a["tokens"],
            "risk": analysis_b["risk"],
            "risk_band": risk_band(analysis_b["risk"]),
            "risk_reasons": analysis_b["risk_reasons"],
        },
    )
