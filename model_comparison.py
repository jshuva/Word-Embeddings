import json
from scipy.spatial.distance import cosine
from scipy.stats import spearmanr

# Set YOUR name here as it appears in the CSV
MY_NAME = "Jayanta Sarker Shuva" 

def get_rankings(embeddings_dict, target_name):
    distances = []
    target_vec = embeddings_dict[target_name]
    for name, vec in embeddings_dict.items():
        if name != target_name:
            distances.append((name, cosine(target_vec, vec))) # Cosine distance
    # Sort closest to farthest
    distances.sort(key=lambda x: x[1])
    return [name for name, dist in distances]

# Load both embeddings
with open("embeddings_minilm.json", "r") as f:
    emb_model1 = json.load(f)
with open("embeddings_paraphrase.json", "r") as f:
    emb_model2 = json.load(f)

rankings1 = get_rankings(emb_model1, MY_NAME)
rankings2 = get_rankings(emb_model2, MY_NAME)

print(f"Model 1 closest: {rankings1[:3]}")
print(f"Model 2 closest: {rankings2[:3]}")

# Convert names to numerical ranks for correlation
rank_dict1 = {name: i for i, name in enumerate(rankings1)}
ranks1_num = [rank_dict1[name] for name in rankings1]
ranks2_num = [rank_dict1[name] for name in rankings2] # Rank relative to Model 1's order

correlation, _ = spearmanr(ranks1_num, ranks2_num)
print(f"Spearman Rank Correlation: {correlation:.4f}")