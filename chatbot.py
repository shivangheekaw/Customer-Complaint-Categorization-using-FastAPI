import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_knowledge_base(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(text):
    return text.strip().lower()


def exact_match_category(complaint_text, knowledge_base):
    complaint_text = normalize_text(complaint_text)

    for entry in knowledge_base["KnowledgeBase"]:
        category = entry["Category"]
        all_complaints = [entry["Complaint"]] + entry["Complaint Variants"]

        for text in all_complaints:
            if complaint_text == normalize_text(text):
                return category

    return None


def build_similarity_corpus(knowledge_base):
    texts = []
    categories = []

    for entry in knowledge_base["KnowledgeBase"]:
        category = entry["Category"]
        all_complaints = [entry["Complaint"]] + entry["Complaint Variants"]

        for text in all_complaints:
            texts.append(normalize_text(text))
            categories.append(category)

    return texts, categories


def cosine_similarity_category(
    complaint_text,
    corpus_texts,
    corpus_categories,
    threshold=0.25
):
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(corpus_texts)
    complaint_vector = vectorizer.transform([normalize_text(complaint_text)])

    similarities = cosine_similarity(complaint_vector, tfidf_matrix)[0]

    best_index = np.argmax(similarities)
    best_score = similarities[best_index]

    if best_score >= threshold:
        return corpus_categories[best_index]

    return None


def predict_category(
    complaint_text,
    knowledge_base,
    threshold=0.25
):
    category = exact_match_category(complaint_text, knowledge_base)
    if category is not None:
        return category

    corpus_texts, corpus_categories = build_similarity_corpus(knowledge_base)

    return cosine_similarity_category(
        complaint_text,
        corpus_texts,
        corpus_categories,
        threshold
    )


# if __name__ == "__main__":
#     KNOWLEDGE_BASE_PATH = r"C:\Users\Admin\Desktop\Day_Zero\Complaints.json"

#     knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_PATH)

#     test_complaint = "Incorrect or missing information on my credit report, including payment history, balances, late payments, or account status, and credit bureaus failing to properly investigate or correct reported errors."
#     predicted_category = predict_category(
#         complaint_text=test_complaint,
#         knowledge_base=knowledge_base,
#         threshold=0.23
#     )

#     print("Predicted Category:", predicted_category)


def chatbot_logic(test_complaint):
    KNOWLEDGE_BASE_PATH = r"C:\Users\Admin\Desktop\Day_Zero\Complaints.json"

    knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_PATH)

    # test_complaint = "Incorrect or missing information on my credit report, including payment history, balances, late payments, or account status, and credit bureaus failing to properly investigate or correct reported errors."
    predicted_category = predict_category(
        complaint_text=test_complaint,
        knowledge_base=knowledge_base,
        threshold=0.23
    )

    return str("Predicted Category:"+ predicted_category)

# chatbot_logic()
