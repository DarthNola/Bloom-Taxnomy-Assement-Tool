import os
from flask import request, jsonify
from pdf_processor import upload_pdf_and_extract_questions
from classifier import classify_questions, calculate_quality_of_paper, count_bloom_levels

def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the file temporarily
    pdf_path = f"uploads/{file.filename}"
    file.save(pdf_path)
    
    # Extract questions from the PDF
    questions = upload_pdf_and_extract_questions(pdf_path)

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
        return jsonify({'error': 'No questions to classify.'}), 400
