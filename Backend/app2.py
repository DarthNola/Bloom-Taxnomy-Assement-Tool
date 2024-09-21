import re
import pypdfium2 as pdfium
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from pytesseract import image_to_string, pytesseract
from transformers import BertTokenizer, BertModel
from sklearn import svm
import torch
import numpy as np
import os

# Load environment variables using dotenv (if used)
from dotenv import load_dotenv

load_dotenv()  # Make sure .env is loaded

# Check the TESSERACT_PATH value
tesseract_path = os.getenv('TESSERACT_PATH')
print(f"Tesseract Path from .env: {tesseract_path}")

if tesseract_path:
    pytesseract.tesseract_cmd = tesseract_path
else:
    raise FileNotFoundError("Tesseract path is not set in environment variables or not found.")


def convert_pdf_to_images(file_path, scale=300/72):
    try:
        pdf_file = pdfium.PdfDocument(file_path)
        page_indices = range(len(pdf_file))

        renderer = pdf_file.render(
            pdfium.PdfBitmap.to_pil,
            page_indices=page_indices,
            scale=scale,
        )

        list_final_images = []

        for i, image in zip(page_indices, renderer):
            with BytesIO() as image_byte_array:
                image.save(image_byte_array, format='jpeg', optimize=True)
                list_final_images.append({i: image_byte_array.getvalue()})

        return list_final_images

    except Exception as e:
        print(f"An error occurred while converting PDF to images: {e}")
        return []

def extract_text_with_pytesseract(list_dict_final_images):
    if not list_dict_final_images:
        print("No images to extract text from.")
        return ""

    text_list = []
    for image_bytes in (list(data.values())[0] for data in list_dict_final_images):
        image = Image.open(BytesIO(image_bytes))
        text_list.append(image_to_string(image))

    return "\n".join(text_list)

def extract_questions_from_text(text):
    keywords = ['how', 'explain', 'describe', 'define', 'name', 
                'which', 'who', 'where', 'when', 'state', 'determine', 
                'illustrate']

    pattern = r'\b(?:' + '|'.join(keywords) + r')\b.*?[?.]'
    questions = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
    
    return questions

# Define categories with corresponding values
class BloomCategory:
    REMEMBERING = "REMEMBERING"
    UNDERSTANDING = "UNDERSTANDING"
    APPLYING = "APPLYING"
    ANALYZING = "ANALYZING"
    EVALUATING = "EVALUATING"
    CREATING = "CREATING"

category_values = {
    BloomCategory.REMEMBERING: 1,
    BloomCategory.UNDERSTANDING: 2,
    BloomCategory.APPLYING: 3,
    BloomCategory.ANALYZING: 4,
    BloomCategory.EVALUATING: 5,
    BloomCategory.CREATING: 6
}

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to get BERT embeddings
def get_bert_embeddings(texts):
    embeddings = []
    for text in texts:
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        # Use the mean of the last hidden layer's token embeddings
        embedding = outputs.last_hidden_state.mean(dim=1).numpy().flatten()
        embeddings.append(embedding)
    return np.array(embeddings)

# Training data (should be replaced with real data)

train_x = [
    # REMEMBERING (Keywords: list, define, recall, state, identify)
    "Define the term 'photosynthesis'", 
    "List the stages of mitosis",
    "Identify the capital city of Japan",
    "Recall the name of the 16th U.S. President",
    "State the three laws of motion",
    "What is the boiling point of water?",
    

    # UNDERSTANDING (Keywords: summarize, explain, interpret, classify, describe)
    "Summarize the main events of World War II", 
    "Explain the process of cellular respiration", 
    "Describe the character development in the novel", 
    "Interpret the meaning of the poem", 
    "Classify the different types of rocks", 
    "Explain how photosynthesis works in plants",

    # APPLYING (Keywords: solve, use, demonstrate, apply, implement)
    "Solve this quadratic equation", 
    "Use the law of supply and demand to explain market prices", 
    "Apply Ohm's law to calculate the resistance in this circuit", 
    "Demonstrate how to tie a knot", 
    "Implement the formula to calculate compound interest", 
    "Solve a real-world problem using algebraic expressions",

    # ANALYZING (Keywords: compare, contrast, examine, differentiate, analyze)
    "Compare the leadership styles of two presidents", 
    "Analyze the impact of climate change on polar bears", 
    "Examine the plot structure of the novel", 
    "Differentiate between renewable and non-renewable energy sources", 
    "Analyze the similarities and differences between socialism and capitalism", 
    "Examine the author's use of symbolism in the text",

    # EVALUATING (Keywords: assess, critique, judge, argue, justify)
    "Assess the effectiveness of the new policy", 
    "Critique the author's argument on climate change", 
    "Judge the fairness of the new tax law", 
    "Argue whether electric cars are more sustainable", 
    "Justify the need for stricter environmental regulations", 
    "Evaluate the success of the company’s marketing campaign",

    # CREATING (Keywords: design, create, compose, develop, construct)
    "Design a new logo for the company", 
    "Create a short film based on the prompt", 
    "Compose a piece of music inspired by nature", 
    "Develop a mobile app to track fitness goals", 
    "Construct a model of a sustainable city", 
    "Write a story about a hero overcoming adversity"
]

train_y = [
    # REMEMBERING
    BloomCategory.REMEMBERING, BloomCategory.REMEMBERING, BloomCategory.REMEMBERING,
    BloomCategory.REMEMBERING, BloomCategory.REMEMBERING, BloomCategory.REMEMBERING,

    # UNDERSTANDING
    BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING,
    BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING,

    # APPLYING
    BloomCategory.APPLYING, BloomCategory.APPLYING, BloomCategory.APPLYING,
    BloomCategory.APPLYING, BloomCategory.APPLYING, BloomCategory.APPLYING,

    # ANALYZING
    BloomCategory.ANALYZING, BloomCategory.ANALYZING, BloomCategory.ANALYZING,
    BloomCategory.ANALYZING, BloomCategory.ANALYZING, BloomCategory.ANALYZING,

    # EVALUATING
    BloomCategory.EVALUATING, BloomCategory.EVALUATING, BloomCategory.EVALUATING,
    BloomCategory.EVALUATING, BloomCategory.EVALUATING, BloomCategory.EVALUATING,

    # CREATING
    BloomCategory.CREATING, BloomCategory.CREATING, BloomCategory.CREATING,
    BloomCategory.CREATING, BloomCategory.CREATING, BloomCategory.CREATING
]

# Convert training texts to BERT embeddings
train_x_vectors = get_bert_embeddings(train_x)

# Initialize and train SVM classifier
clf_svm = svm.SVC(kernel='linear')
clf_svm.fit(train_x_vectors, train_y)

# Path to PDF
path_to_pdf = r'Bloom-Taxnomy-Assement-Tool\Backend\digitalexam.pdf'
images_list = convert_pdf_to_images(path_to_pdf)
text_from_images = extract_text_with_pytesseract(images_list)

questions = extract_questions_from_text(text_from_images)

# Classify extracted questions
def classify_questions(questions):
    question_vectors = get_bert_embeddings(questions)
    predictions = clf_svm.predict(question_vectors)
    return predictions

if questions:
    predictions = classify_questions(questions)
    predictions_list = predictions.tolist()  # Convert NumPy array to list
    classified_questions = [{'question': question, 'prediction': prediction} for question, prediction in zip(questions, predictions_list)]
    
    # Calculate quality of paper
    total_questions = len(questions)
    if total_questions > 0:
        sum_values = sum(category_values[pred] for pred in predictions_list)
        quality_of_paper = (sum_values / (total_questions * 6)) * 100
    else:
        quality_of_paper = 0
    
    # Count each Bloom's level
    level_counts = {level: predictions_list.count(level) for level in category_values.keys()}
    
    # Print classified questions
    print("Classified Questions:")
    for item in classified_questions:
        print(f"Question: {item['question'].strip()} | Predicted Bloom's Level: {item['prediction']}")
    
    # Print quality of paper
    print(f"Quality of Paper: {quality_of_paper:.2f}%")
    
    # Print count of each Bloom's level
    print("Counts of Each Bloom's Level:")
    for level, count in level_counts.items():
        print(f"{level}: {count}")
else:
    print("No questions to classify.")
