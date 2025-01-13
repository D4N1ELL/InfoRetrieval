import json
from collections import defaultdict

# Load the dataset
with open("cars.json", "r") as file:
    data = json.load(file)

# Initialize inverted index
inverted_index = defaultdict(list)

# Build the inverted index
for doc_id, car in enumerate(data):
    # Combine relevant fields for indexing
    text = f"{car['Make']} {car['Model']} {car['Type']} {car['Fuel']}"
    
    # Tokenize and normalize
    tokens = text.lower().split()
    
    # Add tokens to the index
    for token in tokens:
        if doc_id not in inverted_index[token]:
            inverted_index[token].append(doc_id)

# Store the inverted index for later use
with open("inverted_index.json", "w") as outfile:
    json.dump(inverted_index, outfile, indent=4)

print("Inverted index created successfully!")

def query_index(term, index):
    return index.get(term.lower(), [])

# Example usage
with open("inverted_index.json", "r") as file:
    index = json.load(file)

results = query_index("Toyota", index)
print("Documents containing 'Toyota':", results)
