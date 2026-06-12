import random

QUESTION_BANK = {
    "machine learning": [
        "Explain overfitting and underfitting. How would you reduce overfitting?",
        "What is the bias-variance tradeoff?",
        "How would you evaluate an imbalanced classification model?",
        "Explain cross-validation and why it is useful."
    ],
    "deep learning": [
        "What is dropout and how does it help in neural networks?",
        "Explain CNN vs RNN vs LSTM.",
        "What is vanishing gradient problem?",
        "How does batch normalization help training?"
    ],
    "nlp": [
        "Explain TF-IDF and its limitations.",
        "What is the difference between stemming and lemmatization?",
        "How do transformers improve over RNNs?",
        "How would you build a fake news detection model?"
    ],
    "fastapi": [
        "How would you deploy an ML model using FastAPI?",
        "How do you handle file uploads in FastAPI?",
        "How would you design an API for model inference?",
        "How would you secure an ML API?"
    ],
    "python": [
        "How do you handle missing values in Python using pandas?",
        "Explain list, tuple, set, and dictionary.",
        "How would you optimize slow Python code?",
        "What is the difference between shallow copy and deep copy?"
    ],
    "sql": [
        "Explain joins in SQL with examples.",
        "How would you optimize a slow SQL query?",
        "What is indexing in SQL?",
        "Difference between WHERE and HAVING?"
    ]
}

DEFAULT_QUESTIONS = [
    "Explain the complete machine learning project lifecycle.",
    "How would you select the best ML model for a real-world problem?",
    "How do you prevent data leakage in ML projects?",
    "Explain precision, recall, F1-score, and accuracy."
]


def generate_question(role, skills, context="", asked_questions=None, question_number=1):
    asked_questions = asked_questions or []
    asked_lower = [q.lower().strip() for q in asked_questions]

    possible_questions = []

    for skill in skills:
        skill_lower = skill.lower()
        for key, questions in QUESTION_BANK.items():
            if key in skill_lower:
                possible_questions.extend(questions)

    if not possible_questions:
        possible_questions = DEFAULT_QUESTIONS

    unused_questions = [
        q for q in possible_questions
        if q.lower().strip() not in asked_lower
    ]

    if not unused_questions:
        unused_questions = [
            q for q in DEFAULT_QUESTIONS
            if q.lower().strip() not in asked_lower
        ]

    if not unused_questions:
        return f"For the role of {role}, explain one advanced AI/ML concept from your resume with a real project example."

    return unused_questions[(question_number - 1) % len(unused_questions)]


def evaluate_answer(question, answer):
    answer_length = len(answer.split())

    keywords = [
        "model", "data", "training", "validation", "test",
        "accuracy", "precision", "recall", "f1", "example",
        "overfitting", "regularization", "cross-validation"
    ]

    score = 5

    if answer_length > 40:
        score += 2

    if answer_length > 80:
        score += 1

    matched = sum(1 for k in keywords if k.lower() in answer.lower())

    if matched >= 3:
        score += 2

    score = min(score, 10)

    if score >= 8:
        feedback = "Strong answer. It explains the concept and includes practical reasoning."
    elif score >= 6:
        feedback = "Good answer, but it can be improved with examples and more technical detail."
    else:
        feedback = "Needs improvement. Add explanation, metrics, examples, and project-based reasoning."

    return score, feedback