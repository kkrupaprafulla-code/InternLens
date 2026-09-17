from flask import Flask, request, jsonify
from flask_cors import CORS

from ai_analyzer import analyze_with_ai

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "InternLens AI backend is running!",
        "version": "2.0"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": "2.0"})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request."}), 400

    internship = data.get("internship", "")

    if not isinstance(internship, str) or not internship.strip():
        return jsonify({
            "error": "Please enter an internship listing."
        }), 400

    try:
        result = analyze_with_ai(internship)
        return jsonify(result), 200

    except Exception as exc:
        print("Analysis error:", repr(exc))
        return jsonify({
            "error": "InternLens could not complete the analysis.",
            "details": str(exc)
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
