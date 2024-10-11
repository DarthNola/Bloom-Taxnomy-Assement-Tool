import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn import svm
import torch

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Define Bloom's Taxonomy categories
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

# Training data (replace with real data)


train_x = [
    # REMEMBERING (Keywords: list, define, recall, state, identify)
    "Define the term 'photosynthesis'", 
    "List the stages of mitosis", 
    "Identify the capital city of Japan", 
    "Recall the name of the 16th U.S. President", 
    "State the three laws of motion", 
    "What is the boiling point of water?",
    "Identify the chemical formula for water", 
    "Define the theory of relativity",
    "State the first law of thermodynamics", 
    "Recall the main characters in 'To Kill a Mockingbird'", 
    "List the names of all planets in the solar system", 
    "Identify the tallest mountain in the world",

    # UNDERSTANDING (Keywords: summarize, explain, interpret, classify, describe)
    "Summarize the main events of World War II", 
    "Explain the process of cellular respiration", 
    "Describe the character development in the novel", 
    "Interpret the meaning of the poem", 
    "Classify the different types of rocks", 
    "Explain how photosynthesis works in plants",
    "Summarize the causes of the Great Depression", 
    "Explain the significance of the Magna Carta", 
    "Describe how seasons change on Earth", 
    "Classify the different types of government systems", 
    "Interpret the message of Martin Luther King Jr.'s speech", 
    "Explain how vaccines work in the human body",

    # APPLYING (Keywords: solve, use, demonstrate, apply, implement)
    "Solve this quadratic equation", 
    "Use the law of supply and demand to explain market prices", 
    "Apply Ohm's law to calculate the resistance in this circuit", 
    "Demonstrate how to tie a knot", 
    "Implement the formula to calculate compound interest", 
    "Solve a real-world problem using algebraic expressions",
    "Apply the Pythagorean theorem to find the length of the hypotenuse", 
    "Demonstrate the steps for creating a simple website", 
    "Use the periodic table to predict the reactivity of an element", 
    "Apply the principles of aerodynamics to explain how planes fly", 
    "Solve for x in the equation: 2x + 3 = 7", 
    "Use a map to determine the shortest driving route between two cities",

    # ANALYZING (Keywords: compare, contrast, examine, differentiate, analyze)
    "Compare the leadership styles of two presidents", 
    "Analyze the impact of climate change on polar bears", 
    "Examine the plot structure of the novel", 
    "Differentiate between renewable and non-renewable energy sources", 
    "Analyze the similarities and differences between socialism and capitalism", 
    "Examine the author's use of symbolism in the text",
    "Compare and contrast the properties of metals and non-metals", 
    "Analyze the reasons behind the stock market crash of 1929", 
    "Differentiate between similes and metaphors in the poem", 
    "Examine the causes and effects of the American Civil War", 
    "Analyze the impact of deforestation on biodiversity", 
    "Compare the benefits and drawbacks of solar and wind energy",

    # EVALUATING (Keywords: assess, critique, judge, argue, justify)
    "Assess the effectiveness of the new policy", 
    "Critique the author's argument on climate change", 
    "Judge the fairness of the new tax law", 
    "Argue whether electric cars are more sustainable", 
    "Justify the need for stricter environmental regulations", 
    "Evaluate the success of the company’s marketing campaign",
    "Assess the effectiveness of renewable energy sources compared to fossil fuels", 
    "Critique the use of technology in modern education", 
    "Judge the ethical implications of genetic modification", 
    "Argue for or against the use of nuclear energy", 
    "Justify the use of military intervention in international conflicts", 
    "Evaluate the impact of social media on youth culture",

    # CREATING (Keywords: design, create, compose, develop, construct)
    "Design a new logo for the company", 
    "Create a short film based on the prompt", 
    "Compose a piece of music inspired by nature", 
    "Develop a mobile app to track fitness goals", 
    "Construct a model of a sustainable city", 
    "Write a story about a hero overcoming adversity",
    "Design an experiment to test the effects of different fertilizers on plant growth", 
    "Create a storyboard for a short film about climate change", 
    "Invent a new product that could solve everyday household problems", 
    "Compose a poem about the beauty of nature", 
    "Develop a business plan for a startup company", 
    "Write a song expressing gratitude"
]

train_y = [
    # REMEMBERING
    BloomCategory.REMEMBERING, BloomCategory.REMEMBERING, BloomCategory.REMEMBERING,
    BloomCategory.REMEMBERING, BloomCategory.REMEMBERING, BloomCategory.REMEMBERING,
    BloomCategory.REMEMBERING, BloomCategory.REMEMBERING, BloomCategory.REMEMBERING,
    BloomCategory.REMEMBERING, BloomCategory.REMEMBERING, BloomCategory.REMEMBERING,

    # UNDERSTANDING
    BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING,
    BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING,
    BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING,
    BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING, BloomCategory.UNDERSTANDING,

    # APPLYING
    BloomCategory.APPLYING, BloomCategory.APPLYING, BloomCategory.APPLYING,
    BloomCategory.APPLYING, BloomCategory.APPLYING, BloomCategory.APPLYING,
    BloomCategory.APPLYING, BloomCategory.APPLYING, BloomCategory.APPLYING,
    BloomCategory.APPLYING, BloomCategory.APPLYING, BloomCategory.APPLYING,

    # ANALYZING
    BloomCategory.ANALYZING, BloomCategory.ANALYZING, BloomCategory.ANALYZING,
    BloomCategory.ANALYZING, BloomCategory.ANALYZING, BloomCategory.ANALYZING,
    BloomCategory.ANALYZING, BloomCategory.ANALYZING, BloomCategory.ANALYZING,
    BloomCategory.ANALYZING, BloomCategory.ANALYZING, BloomCategory.ANALYZING,

    # EVALUATING
    BloomCategory.EVALUATING, BloomCategory.EVALUATING, BloomCategory.EVALUATING,
    BloomCategory.EVALUATING, BloomCategory.EVALUATING, BloomCategory.EVALUATING,
    BloomCategory.EVALUATING, BloomCategory.EVALUATING, BloomCategory.EVALUATING,
    BloomCategory.EVALUATING, BloomCategory.EVALUATING, BloomCategory.EVALUATING,

    # CREATING
    BloomCategory.CREATING, BloomCategory.CREATING, BloomCategory.CREATING,
    BloomCategory.CREATING, BloomCategory.CREATING, BloomCategory.CREATING,
    BloomCategory.CREATING, BloomCategory.CREATING, BloomCategory.CREATING,
    BloomCategory.CREATING, BloomCategory.CREATING, BloomCategory.CREATING
]


# Convert training texts to BERT embeddings
def get_bert_embeddings(texts):
    embeddings = []
    for text in texts:
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).numpy().flatten()
        embeddings.append(embedding)
    return np.array(embeddings)

# Convert training texts to BERT embeddings for SVM training
train_x_vectors = get_bert_embeddings(train_x)

# Initialize and train SVM classifier
clf_svm = svm.SVC(kernel='linear')
clf_svm.fit(train_x_vectors, train_y)

# Classify questions using the trained SVM model
def classify_questions(questions):
    question_vectors = get_bert_embeddings(questions)
    predictions = clf_svm.predict(question_vectors)
    return predictions

# Calculate quality of paper
def calculate_quality_of_paper(predictions):
    total_questions = len(predictions)
    sum_values = sum(category_values[pred] for pred in predictions)
    return (sum_values / (total_questions * 6)) * 100 if total_questions > 0 else 0

# Count each Bloom's level
def count_bloom_levels(predictions):
    return {level: predictions.tolist().count(level) for level in category_values.keys()}
