from sklearn import svm
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from collections import Counter

# Define the Bloom's Taxonomy categories
class BloomCategory:
    REMEMBERING = "REMEMBERING"
    UNDERSTANDING = "UNDERSTANDING"
    APPLYING = "APPLYING"
    ANALYZING = "ANALYZING"
    EVALUATING = "EVALUATING"
    CREATING = "CREATING"

# Define category values
category_values = {
    BloomCategory.REMEMBERING: 1,
    BloomCategory.UNDERSTANDING: 2,
    BloomCategory.APPLYING: 3,
    BloomCategory.ANALYZING: 4,
    BloomCategory.EVALUATING: 5,
    BloomCategory.CREATING: 6
}

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

# Convert training texts to BERT embeddings
train_x_vectors = get_bert_embeddings(train_x)

# Initialize and train SVM classifier
clf_svm = svm.SVC(kernel='linear')
clf_svm.fit(train_x_vectors, train_y)

# Classify questions
def classify_questions(questions):
    question_vectors = get_bert_embeddings(questions)
    predictions = clf_svm.predict(question_vectors)
    return predictions

# Calculate quality of paper
def calculate_quality_of_paper(predictions):
    total_questions = len(predictions)
    if total_questions == 0:
        return 0

    sum_values = sum(category_values[pred] for pred in predictions)
    quality_of_paper = (sum_values / (total_questions * max(category_values.values()))) * 100
    return round(quality_of_paper, 2)

# Count occurrences of each Bloom's level
def count_bloom_levels(predictions):
    return dict(Counter(predictions))
