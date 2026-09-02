from flask import Flask, request, jsonify
from google import genai
from PIL import Image
import io
import os

app = Flask(__name__)

# API key GitHub code में मत लिखना।
# इसे hosting service में GEMINI_API_KEY नाम से Secret/Environment Variable में डालना है।
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return "AppHum Photo Math Backend is running!"


@app.route("/solve", methods=["POST"])
def solve():
    try:
        if "image" not in request.files:
            return jsonify({"error": "Photo upload नहीं हुई"}), 400

        file = request.files["image"]

        if file.filename == "":
            return jsonify({"error": "कोई photo select नहीं की गई"}), 400

        image = Image.open(io.BytesIO(file.read()))

        prompt = """
You are a helpful math tutor.

Look carefully at the uploaded image and read the math question.

Solve the question correctly.

Give the response in Hindi.

Use this format:

Question:
[question you read]

Solution:
[step-by-step solution]

Final Answer:
[final answer]

If the image is not a math question, say:
"यह math question की photo नहीं है।"
"""

        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=[prompt, image]
        )

        return jsonify({
            "answer": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
