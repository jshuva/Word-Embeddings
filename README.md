## Classmate Interests Visualization

### What Are Embeddings?

Imagine trying to explain to a computer how similar two people's hobbies are. Computers don't understand English words; they only understand numbers. To solve this, we use a concept called **embeddings**.

Think of an embedding as giving a sentence a highly specific "GPS coordinate" on a giant map of meaning.

If two places are close together in the real world, their GPS coordinates are very similar. Embeddings do the exact same thing for ideas. When a computer reads our class dataset, it assigns a coordinate point to each person's description based on the underlying concepts, not just the exact letters or words.

Let’s look at my entry in the dataset: *"I enjoy reading books, hiking, and watching documentaries"*.

Now, let's look at a few of our classmates:

**Mohamed Drira** wrote: *"I’m passionate about hiking, reading, meditation, movies, and embracing new challenges"*.


**Bhavik Kantilal Bhagat** wrote: *"Chess, Maths and Music."*.

Even though Mohamed and I didn't use the exact same phrasing, the embedding model understands that "watching documentaries" and "movies" are related concepts, and it sees that we both explicitly love "hiking" and "reading". Because the *meanings* of our sentences are similar, the computer assigns our sentences "GPS coordinates" that are right next to each other on the map.

On the other hand, Bhavik's interests (math, chess, music) share very little thematic overlap with mine. As a result, the computer gives Bhavik's sentence a completely different set of coordinates, plotting him much further away from me in the visual space.

By translating text into these coordinate points, embeddings allow us to take unstructured, messy human language and mathematically measure exactly how closely related two ideas are. The visualization above is simply a 2D map of all those coordinates, automatically pulling classmates with shared interests closer together!


![Sample output of script](https://github.com/jshuva/Word-Embeddings/blob/main/visualization.png?raw=true)


### Data Analysis

To understand how sensitive our embedding model is to dataset idiosyncrasies, I modified three sentences in `classmates.csv`.

First, I made a major conceptual change to Somto Muotoe's entry, completely altering the core meaning of the sentence from the original hobbies from `I enjoy reading, cycling, playing chess, and story-based video games` to `I absolutely love devouring books, driving.`. For the other two entries—my own (Jayanta Sarker Shuva) and Krushi Mistry's—I made minor modifications by swapping single words with close synonyms (for example, changing "hiking" to "walking" or "cricket" to "football").

I then generated new embeddings and compared them to the originals using cosine similarity. The results clearly highlight how the model interprets text:

* **Somto Muotoe (Major Change):** 0.4756 similarity
* **Jayanta Sarker Shuva (Minor Change):** 0.9564 similarity
* **Krushi Mistry (Minor Change):** 0.9552 similarity

The minor changes had a very small impact on the embeddings, keeping the similarity scores above 0.95. This occurs because the model successfully recognizes synonyms and contextual relationships; tweaking a single word barely shifts the overall meaning (or "GPS coordinate") of the sentence.

In contrast, the major change to Somto's entry caused the similarity score to drop significantly to 0.4756. Because the semantic meaning was drastically altered, the model moved the entry to a completely different location in the high-dimensional space. This demonstrates that the model correctly prioritizes the underlying meaning of a sentence rather than just looking at superficial word counts.


### Embedding Sensitivity Tests

To evaluate how sensitive our matchmaking pipeline is to the choice of the underlying embedding model, I replaced the default `all-MiniLM-L6-v2` model with `paraphrase-MiniLM-L6-v2`. I then calculated the cosine similarity between my profile and the rest of the class for both models, ranked the results, and compared them.

**Quantitative Impact:** The Spearman Rank Correlation between the two models' rankings is **0.8246**. This high positive correlation indicates that the overall, broad ordering of classmates—from most similar to least similar—remains largely consistent regardless of which model is used. Both models generally agree on the big picture.

**Qualitative Impact:** However, despite the strong overall correlation, the models are highly sensitive at the micro-level, significantly changing who my immediate "closest friends" are.

* Under the original model, my top three matches were: **Binziya Siddik, Mohammad Pakdoust, and Miguel Palafox**.
* Under the paraphrase model, my top three shifted to: **Mohammad Pakdoust, Mohamed Drira, and Md Musfiqur Rahman**.

While Mohammad Pakdoust remained a top match across both models, the rest of my top matches changed completely. This reveals that while different embedding models agree on general similarities, the fine-grained rankings at the very top are highly sensitive to the specific model's architecture and training data. The choice of model undeniably alters the final matchmaking results.


### Dimension Reduction Analysis

When running the default UMAP algorithm with different random seeds, the resulting output changes noticeably every time. This visual instability occurs because UMAP is a stochastic algorithm designed to map complex, non-linear high-dimensional spaces (like our 384-dimensional sentence embeddings) down to just two dimensions. To achieve this, it relies on random initialization and local optimization. Because there is no single "perfect" way to flatten 384 dimensions without distortion, the algorithm often settles into different valid 2D layouts depending on the starting seed. This instability indicates that a single, untuned visualization might not be entirely reliable on its own.

To ensure the 2D map faithfully reflects the true similarities between classmates, I used an Optuna optimization routine to tune the algorithm's hyperparameters. The objective was to maximize the average Spearman rank correlation between the actual high-dimensional cosine similarity and the flattened 2D Euclidean distance.

The hyperparameter search yielded the following optimal configuration:

* **`n_neighbors`:** 7
* **`min_dist`:** 0.6859
* **Best Average Rank Correlation:** 0.6057

An average rank correlation of approximately 0.61 indicates a moderately strong positive relationship. This means the tuned UMAP implementation is highly adequate for our matchmaking purposes. While compressing 384 dimensions into a 2D plot inevitably results in some structural information loss (which is why the correlation isn't perfectly 1.0), a score of 0.6057 confirms that the tuned visualization reliably preserves the original high-dimensional rankings. Classmates plotted near each other on the tuned map genuinely share similar underlying interests.


![Sample output of script](https://github.com/jshuva/Word-Embeddings/blob/dimension-reduction-analysis/visualization.png?raw=true)
