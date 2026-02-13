import json
from scipy.spatial.distance import cosine

# Load old and new embeddings
with open("embeddings_old.json", "r") as f:
    old_emb = json.load(f)
with open("embeddings.json", "r") as f:
    new_emb = json.load(f)

# The names of the 3 students you modified
modified_students = ["Somto Muotoe", "Jayanta Sarker Shuva", "Krushi Mistry"]

for student in modified_students:
    if student in old_emb and student in new_emb:
        # Calculate cosine similarity (1 - cosine distance)
        similarity = 1 - cosine(old_emb[student], new_emb[student])
        print(f"Similarity for {student} before and after modification: {similarity:.4f}")