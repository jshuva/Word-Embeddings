## Classmate Interests Visualization

### What Are Embeddings?

Imagine trying to explain to a computer how similar two people's hobbies are. Computers don't understand English words; they only understand numbers. To solve this, we use a concept called **embeddings**.

Think of an embedding as giving a sentence a highly specific "GPS coordinate" on a giant map of meaning.

If two places are close together in the real world, their GPS coordinates are very similar. Embeddings do the exact same thing for ideas. When a computer reads our class dataset, it assigns a coordinate point to each person's description based on the underlying concepts, not just the exact letters or words.

Let’s look at my entry in the dataset: *"I enjoy reading books, hiking, and watching documentaries"*.

Now, let's look at a few of our classmates:

* 
**Mohamed Drira** wrote: *"I’m passionate about hiking, reading, meditation, movies, and embracing new challenges"*.


* 
**Bhavik Kantilal Bhagat** wrote: *"Chess, Maths and Music."*.



Even though Mohamed and I didn't use the exact same phrasing, the embedding model understands that "watching documentaries" and "movies" are related concepts, and it sees that we both explicitly love "hiking" and "reading". Because the *meanings* of our sentences are similar, the computer assigns our sentences "GPS coordinates" that are right next to each other on the map.

On the other hand, Bhavik's interests (math, chess, music) share very little thematic overlap with mine. As a result, the computer gives Bhavik's sentence a completely different set of coordinates, plotting him much further away from me in the visual space.

By translating text into these coordinate points, embeddings allow us to take unstructured, messy human language and mathematically measure exactly how closely related two ideas are. The visualization above is simply a 2D map of all those coordinates, automatically pulling classmates with shared interests closer together!


![Sample output of script](https://github.com/jshuva/Word-Embeddings/blob/main/visualization.png?raw=true)
