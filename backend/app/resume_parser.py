import re
import fitz

SKILLS = [
    'Python','Machine Learning','Deep Learning','Data Science','NLP','Computer Vision','TensorFlow','PyTorch',
    'Scikit-learn','Pandas','NumPy','SQL','MongoDB','FastAPI','Flask','Django','React','Git','Docker',
    'Data Structures','Neural Networks','Classification','Regression','Clustering','Statistics','Power BI','Excel'
]


def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ''
    for page in doc:
        text += page.get_text() + '\n'
    return text.strip()


def extract_candidate_name(text):
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    bad_words = ['contact', 'email', 'phone', 'resume', 'curriculum', 'linkedin', 'github']
    for line in lines[:10]:
        clean = re.sub(r'[^A-Za-z ]', '', line).strip()
        if 2 <= len(clean.split()) <= 4 and not any(b in clean.lower() for b in bad_words):
            return clean.title()
    return 'Candidate'


def extract_skills(text):
    found = []
    low = text.lower()
    for skill in SKILLS:
        if skill.lower() in low:
            found.append(skill)
    return sorted(set(found))
