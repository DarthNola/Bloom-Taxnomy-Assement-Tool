import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables using dotenv
load_dotenv()

# Configure Gemini with the API key
genai.configure(api_key=os.getenv("API_KEY"))

def upload_pdf_and_extract_questions(pdf_path):
    try:
        uploaded_file = genai.upload_file(pdf_path)
        prompt = "Extract questions from this uploaded PDF."
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([prompt, uploaded_file])
        questions = response.text.strip().split('\n')
        return questions
    except Exception as e:
        print(f"An error occurred while extracting questions: {e}")
        return []
