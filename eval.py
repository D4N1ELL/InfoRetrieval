test_queries = [
    {"query": "Toyota Sedan", "relevant_docs": [0, 2, 5]},
    {"query": "Electric Car", "relevant_docs": [8, 12, 15]},
    {"query": "SUV Family", "relevant_docs": [3, 7, 9]},
]

def precision_recall_f1(retrieved, relevant):
    # Convert to sets for easier calculations
    retrieved_set = set(retrieved)
    relevant_set = set(relevant)

    # Calculate Precision and Recall
    true_positives = len(retrieved_set & relevant_set)
    precision = true_positives / len(retrieved_set) if retrieved_set else 0
    recall = true_positives / len(relevant_set) if relevant_set else 0

    # Calculate F1-score
    f1_score = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

    return precision, recall, f1_score

def average_precision(retrieved, relevant):
    relevant_set = set(relevant)
    precision_sum = 0
    relevant_count = 0

    for i, doc in enumerate(retrieved):
        if doc in relevant_set:
            relevant_count += 1
            precision_sum += relevant_count / (i + 1)

    return precision_sum / len(relevant_set) if relevant_set else 0

def mean_average_precision(test_queries, search_function):
    ap_sum = 0
    for test_query in test_queries:
        query = test_query["query"]
        relevant_docs = test_query["relevant_docs"]
        retrieved_docs = search_function(query)
        ap_sum += average_precision(retrieved_docs, relevant_docs)

    return ap_sum / len(test_queries) if test_queries else 0

# Example Search Function (replace this with your ranked_search or boolean_search)
def mock_search(query):
    # Example function that simulates search results
    # Replace this with your actual ranked_search or boolean_search function
    if query == "Toyota Sedan":
        return [0, 2, 10, 12]
    elif query == "Electric Car":
        return [8, 13, 15]
    elif query == "SUV Family":
        return [3, 7, 11, 14]
    return []

# Evaluate Metrics
for test_query in test_queries:
    query = test_query["query"]
    relevant_docs = test_query["relevant_docs"]
    retrieved_docs = mock_search(query)  # Replace mock_search with your search function
    precision, recall, f1_score = precision_recall_f1(retrieved_docs, relevant_docs)
    print(f"Query: {query}")
    print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1-Score: {f1_score:.2f}\n")

# Calculate MAP
map_score = mean_average_precision(test_queries, mock_search)  # Replace mock_search with your search function
print(f"Mean Average Precision (MAP): {map_score:.2f}")
