from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai
import os

# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

app = Flask(__name__)
CORS(app)

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

# Create Gemini client
client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return jsonify({
        "message": "StudyMate backend is running! 🎓"
    })


@app.route("/summarize", methods=["POST"])
def summarize():

    # Check if PDF was uploaded
    if "file" not in request.files:
        return jsonify({
            "error": "Please upload a PDF file."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected."
        }), 400

    try:
        # Read PDF
        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        # Check if text was extracted
        if not text.strip():
            return jsonify({
                "error": "Could not extract text from this PDF."
            }), 400

        # Limit extremely large PDFs for our first version
        text = text[:50000]

        # Prompt Gemini
        prompt = f"""
You are StudyMate, an AI study assistant.

Summarize the following study material for a college student.

Give the answer in this format:

1. 📌 Short Overview
2. 🧠 Key Concepts
3. 📝 Important Points
4. 🎯 Exam/Revision Focus
5. 💡 Simple Explanation

Keep the explanation clear, organized and easy to revise.

Study Material:
{text}
"""

        # Send request to Gemini
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        summary = interaction.output_text

        return jsonify({
            "success": True,
            "summary": summary
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)

