from typing import Any, Dict

from fastapi import FastAPI

app = FastAPI(title="BiasScope Sample Model API", version="1.0.0")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(payload: Dict[str, Any]):
    """
    Very simple deterministic-ish scoring function so BiasScope has something to analyze.
    This is NOT a real model.
    """
    age = float(payload.get("age", 0) or 0)
    income = float(payload.get("income", 0) or 0)
    credit_score = float(payload.get("credit_score", 0) or 0)
    experience_years = float(payload.get("experience_years", 0) or 0)

    # Deliberately simplistic "score"
    score = (
        0.15 * min(age / 80.0, 1.0)
        + 0.45 * min(income / 100000.0, 1.0)
        + 0.35 * min(credit_score / 850.0, 1.0)
        + 0.05 * min(experience_years / 40.0, 1.0)
    )

    score = max(0.0, min(1.0, score))
    label = "approved" if score >= 0.55 else "rejected"

    return {"prediction": score, "label": label}

