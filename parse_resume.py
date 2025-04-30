import pdfplumber
import docx
import pandas as pd
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('punkt')

# Load keywords from Excel
def load_keywords(filepath):
    df = pd.read_excel(filepath, engine='openpyxl')
    keywords = df['Skills'].dropna().str.lower().tolist()
    # Remove duplicates
    keywords = list(set(keywords))
    return keywords

def extract_text(filepath):
    if filepath.endswith('.pdf'):
        with pdfplumber.open(filepath) as pdf:
            text = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif filepath.endswith('.docx'):
        doc = docx.Document(filepath)
        text = '\n'.join([para.text for para in doc.paragraphs])
    else:
        text = ''
    return text

def calculate_score(text, keywords, keyword_weights=None):
    # Initialize word count array to store the count of each keyword in the text
    word_count = []

    # Iterate over keywords to count their occurrences in the text
    for keyword in keywords:
        count = text.lower().count(keyword.lower())  # Case-insensitive count
        # If weights are provided, multiply by the keyword's weight
        if keyword_weights and keyword in keyword_weights:
            count *= keyword_weights[keyword]
        word_count.append(count)

    # Calculate the total score by summing up the counts of each keyword
    total_score = sum(word_count)

    # Normalize the score by dividing by the number of keywords and multiplying by 100
    normalized_score = (total_score / len(keywords)) * 100 if len(keywords) > 0 else 0

    # Provide feedback for each keyword (whether it was found or not)
    feedback = [f"'{keywords[i]}': {'Found' if word_count[i] > 0 else 'Not Found'}" for i in range(len(keywords))]

    # Return the normalized score and feedback
    return round(normalized_score, 2), feedback


def parse_and_score(filepath):
    # Load keywords from your Excel file
    keywords = load_keywords('skills_dataset.xlsx')

    # Extract text from resume
    text = extract_text(filepath)
    if not text:
        return 0, ["No text found in resume."]
    
    # Calculate score based on the resume content
    score, feedback = calculate_score(text, keywords)
    return score, feedback
