import os
import base64

from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# API key environment variable से आएगी
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def home():
    return "AppHum AI Math Backend is running"

@app.route("/solve", methods=["POST"])
def solve():
    try:
        if "image" not in request.files:
            return jsonify({"error": "Photo नहीं मिली"}), 400

        image = request.files["image"]

        image_bytes = image.read()

        mime_type = image.mimetype or "image/jpeg"

        prompt = """
तुम AppHum के AI Math Solver हो।

इस फोटो में दिए गए गणित के सवाल को ध्यान से पढ़ो।

उत्तर इस format में दो:

Question:
सवाल को लिखो।

Solution:
सवाल को step-by-step हल करो।

Final Answer:
अंतिम उत्तर साफ-साफ बताओ।

अगर फोटो में गणित का सवाल साफ नहीं दिखाई देता,
तो बताओ कि फोटो दोबारा साफ तरीके से upload करें।

उत्तर हिंदी में दो।
"""

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )

        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=[image_part, prompt]
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
