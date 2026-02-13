import json
import numpy as np
import umap
import optuna
from scipy.spatial.distance import cosine, euclidean
from scipy.stats import spearmanr

# Load the original all-MiniLM-L6-v2 embeddings
with open("embeddings.json", "r") as f:
    person_embeddings = json.load(f)
    
names = list(person_embeddings.keys())
embeddings_hd = np.array(list(person_embeddings.values()))
n_students = len(names)

def objective(trial):
    n_neighbors = trial.suggest_int('n_neighbors', 2, min(15, n_students - 1))
    min_dist = trial.suggest_float('min_dist', 0.0, 0.99)
    
    # Generate 2D projection
    reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, random_state=42)
    embeddings_2d = reducer.fit_transform(embeddings_hd)
    
    avg_corr = 0
    
    for i in range(n_students):
        hd_distances = []
        d2_distances = []
        for j in range(n_students):
            if i != j:
                hd_distances.append(cosine(embeddings_hd[i], embeddings_hd[j]))
                d2_distances.append(euclidean(embeddings_2d[i], embeddings_2d[j]))
                
        # Calculate Spearman correlation for this specific student's rankings
        corr, _ = spearmanr(hd_distances, d2_distances)
        avg_corr += corr
        
    return avg_corr / n_students

# We want to MAXIMIZE the correlation
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)

print("\nBest UMAP hyperparameters:", study.best_params)
print("Best Average Rank Correlation:", study.best_value)