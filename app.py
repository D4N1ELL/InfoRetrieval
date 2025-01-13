from flask import Flask, render_template, request, jsonify
import re
import math
import json

app = Flask(__name__)

# Load the dataset
with open("cars.json", "r") as file:
    data = json.load(file)

# Load the inverted index
with open("inverted_index.json", "r") as f:
    inverted_index = json.load(f)

num_docs = len(data)  # Total number of documents

# Parse Query
def parse_query(query):
    tokens = re.findall(r'\w+|AND|OR|NOT|\(|\)', query.upper())
    return tokens

# Evaluate Stack for Boolean Search
def boolean_search(tokens, index):
    def evaluate_stack(stack):
        if not stack:
            return set()
        result = stack.pop()
        if isinstance(result, set):
            return result
        if result == "AND":
            return evaluate_stack(stack) & evaluate_stack(stack)
        elif result == "OR":
            return evaluate_stack(stack) | evaluate_stack(stack)
        elif result == "NOT":
            return set(range(num_docs)) - evaluate_stack(stack)
        else:
            return set(index.get(result.lower(), []))

    # Convert tokens to Reverse Polish Notation (RPN) for easier evaluation
    output = []
    operators = []
    precedence = {"NOT": 3, "AND": 2, "OR": 1}
    for token in tokens:
        if token.isalnum():
            output.append(token)
        elif token in precedence:
            while (operators and operators[-1] != "(" and
                   precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            operators.pop()
    while operators:
        output.append(operators.pop())

    # Evaluate the RPN expression
    stack = []
    for token in output:
        if token.isalnum():
            stack.append(set(index.get(token.lower(), [])))
        elif token in {"AND", "OR", "NOT"}:
            if token == "NOT":
                stack.append(set(range(num_docs)) - stack.pop())
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(a & b if token == "AND" else a | b)
    return list(stack.pop())

# # Calculate TF-IDF
def calculate_tfidf(index, num_docs):
    tfidf_index = {}
    for term, doc_list in index.items():
        df = len(set(doc_list))  # Unique documents
        idf = math.log((num_docs + 1) / (df + 1)) + 1  # Smoothed IDF
        for doc_id in doc_list:
            tf = doc_list.count(doc_id)
            tfidf_index.setdefault(term, {})[doc_id] = tf * idf
    return tfidf_index

# # Ranked Search
# def ranked_search(query, tfidf_index):
#     query_terms = query.lower().split()
#     scores = {}
#     for term in query_terms:
#         if term in tfidf_index:
#             for doc_id, score in tfidf_index[term].items():
#                 scores[doc_id] = scores.get(doc_id, 0) + score
#     return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# BM25 Parameters
k1 = 1.5  # Controls term frequency saturation
b = 0.75  # Controls document length normalization
avg_doc_length = sum(len(doc.values()) for doc in data) / len(data)

def calculate_bm25(index, num_docs, avg_doc_length):
    bm25_index = {}
    for term, doc_list in index.items():
        df = len(set(doc_list))  # Document frequency
        idf = math.log((num_docs - df + 0.5) / (df + 0.5) + 1)  # IDF for BM25
        for doc_id in set(doc_list):
            tf = doc_list.count(doc_id)
            doc_length = len(data[doc_id].values())
            term_score = idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_length / avg_doc_length))))
            bm25_index.setdefault(term, {})[doc_id] = term_score
    return bm25_index

def ranked_search(query, tfidf_index, bm25_index):
    query_terms = query.lower().split()
    tfidf_scores = {}
    bm25_scores = {}

    for term in query_terms:
        if term in tfidf_index:
            for doc_id, score in tfidf_index[term].items():
                tfidf_scores[doc_id] = tfidf_scores.get(doc_id, 0) + score
        if term in bm25_index:
            for doc_id, score in bm25_index[term].items():
                bm25_scores[doc_id] = bm25_scores.get(doc_id, 0) + score

    # Sort results by scores
    tfidf_sorted = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
    bm25_sorted = sorted(bm25_scores.items(), key=lambda x: x[1], reverse=True)

    return tfidf_sorted, bm25_sorted

# Calculate indices for BM25 and TF-IDF
bm25_index = calculate_bm25(inverted_index, num_docs, avg_doc_length)
# tfidf_index = calculate_tfidf(inverted_index, num_docs)


# Calculate TF-IDF Index
tfidf_index = calculate_tfidf(inverted_index, num_docs)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    tokens = parse_query(query)

    # Perform Boolean Search
    boolean_results = boolean_search(tokens, inverted_index)

    # Perform Ranked Search (TF-IDF and BM25)
    tfidf_results, bm25_results = ranked_search(query, tfidf_index, bm25_index)

    # Map document IDs to actual data
    boolean_docs = [data[doc_id] for doc_id in boolean_results]
    tfidf_docs = [{"doc_id": doc_id, "score": score, "data": data[doc_id]} for doc_id, score in tfidf_results]
    bm25_docs = [{"doc_id": doc_id, "score": score, "data": data[doc_id]} for doc_id, score in bm25_results]

    return jsonify({
        "query": query,
        "boolean_results": boolean_docs,
        "tfidf_results": tfidf_docs,
        "bm25_results": bm25_docs
    })


if __name__ == '__main__':
    app.run(debug=True)
