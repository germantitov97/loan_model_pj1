"""model_service.py - loads the trained model and its saved info, and exposes
them through plain Python functions (no web code here)."""

import json
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "loan_svc_model.pkl"
INFO_PATH = BASE_DIR / "model_info.json"

# Load once at import time so every call reuses them.
_model = joblib.load(MODEL_PATH)
with open(INFO_PATH, encoding="utf-8") as f:
    _info = json.load(f)

NUMERIC = _info["features"]["numeric"]
CATEGORICAL = _info["features"]["categorical"]
ALL_FEATURES = NUMERIC + CATEGORICAL


def get_model_info():
    return _info


def get_file_info():
    return _info["file"]


def get_features():
    return _info["features"]


def get_samples():
    return _info["samples"]


def get_function():
    return _info["function"]


def get_margin():
    return _info["margin"]


def get_accuracy():
    return _info["accuracy"]


def predict(applicant):
    """Predict loan approval for one applicant (a dict of feature -> value).

    Missing features are allowed; the pipeline's imputers fill them in.
    Returns the decision, the class label, and the SVM decision score.
    """
    if not isinstance(applicant, dict):
        raise ValueError("applicant must be a JSON object")

    unknown = set(applicant) - set(ALL_FEATURES)
    if unknown:
        raise ValueError(f"unknown features: {sorted(unknown)}")

    row = {}
    for name in NUMERIC:
        value = applicant.get(name)
        try:
            row[name] = float(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            raise ValueError(f"{name} must be a number")
    for name in CATEGORICAL:
        value = applicant.get(name)
        if name == "Credit_History" and value not in (None, ""):
            value = float(value)  # trained as 0.0 / 1.0
        row[name] = value if value != "" else None

    X = pd.DataFrame([row], columns=ALL_FEATURES)
    label = int(_model.predict(X)[0])
    score = float(_model.decision_function(X)[0])

    return {
        "prediction": label,
        "decision": "Approved" if label == 1 else "Rejected",
        "decision_score": round(score, 4),
        "inside_margin": abs(score) < 1,
    }
