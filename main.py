import pandas as pd
from sentence_transformers import SentenceTransformer
import umap
import matplotlib.pyplot as plt
import json

def main():
    # Load Data (Assuming tab-separated or comma-separated; adjust sep if needed)
    df = pd.read_csv("classmates.csv", sep="\t", header=None, names=["Name", "Description"])
    
    # Generate Embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['Description'].tolist())
    
    # Save embeddings to JSON
    person_embeddings = {name: emb.tolist() for name, emb in zip(df['Name'], embeddings)}
    with open("embeddings.json", "w") as f:
        json.dump(person_embeddings, f)
        
    # Dimension Reduction with UMAP (Set seed for reproducibility)
    # reducer = umap.UMAP(random_state=42)
    reducer = umap.UMAP(n_neighbors=7, min_dist=0.6858581038306797, random_state=42)
    embedding_2d = reducer.fit_transform(embeddings)
    
    # Visualization
    plt.figure(figsize=(12, 10))
    plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1])
    
    for i, name in enumerate(df['Name']):
        plt.annotate(name, (embedding_2d[i, 0], embedding_2d[i, 1]), fontsize=9)
        
    plt.title("Classmate Interests Embedding Space")
    plt.savefig("visualization.png")
    plt.close()
    print("Generated visualization.png and embeddings.json")

if __name__ == "__main__":
    main()