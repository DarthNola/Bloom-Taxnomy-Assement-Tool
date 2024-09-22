from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from classifier import classify_questions, calculate_quality_of_paper, count_bloom_levels
from pdf_processor import convert_pdf_to_images,extract_text_with_pytesseract, extract_questions_from_text

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the PDF
        images_list = convert_pdf_to_images(file_path)
        text_from_images = extract_text_with_pytesseract(images_list)
        questions = extract_questions_from_text(text_from_images)

        # Classify extracted questions
        if questions:
            predictions = classify_questions(questions)
            quality_of_paper = calculate_quality_of_paper(predictions)
            level_counts = count_bloom_levels(predictions)

            response = {
                "classified_questions": [
                    {"question": question, "predicted_level": prediction} 
                    for question, prediction in zip(questions, predictions)
                ],
                "quality_of_paper": quality_of_paper,
                "level_counts": level_counts
            }
            return jsonify(response), 200
        else:
            return jsonify({"message": "No questions found in the PDF."}), 200
    
    return jsonify({"error": "File type not allowed."}), 400

def allowed_file(filename):
    allowed_extensions = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

if __name__ == '__main__':
    app.run(debug=True)
