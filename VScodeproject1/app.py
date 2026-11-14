"""app.py - Flask REST API. Each endpoint calls the matching function
in model_service.py and returns JSON. "/" serves the dashboard page."""

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

import model_service as ms

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/predict")
def predict_page():
    return send_from_directory(BASE_DIR, "predict.html")


@app.get("/assets/<path:filename>")
def assets(filename):
    return send_from_directory(BASE_DIR / "assets", filename)


@app.get("/api/info")
def info():
    return jsonify(ms.get_model_info())


@app.get("/api/file")
def file_info():
    return jsonify(ms.get_file_info())


@app.get("/api/features")
def features():
    return jsonify(ms.get_features())


@app.get("/api/samples")
def samples():
    return jsonify(ms.get_samples())


@app.get("/api/function")
def function():
    return jsonify(ms.get_function())


@app.get("/api/margin")
def margin():
    return jsonify(ms.get_margin())


@app.get("/api/accuracy")
def accuracy():
    return jsonify(ms.get_accuracy())


@app.post("/api/predict")
def predict():
    applicant = request.get_json(silent=True)
    if applicant is None:
        return jsonify({"error": "send a JSON body with the applicant's features"}), 400
    try:
        return jsonify(ms.predict(applicant))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
