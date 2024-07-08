import os
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import voyageai
import numpy as np

def k_nearest_neighbors(query_embedding, documents_embeddings, k=5):
  query_embedding = np.array(query_embedding) # convert to numpy array
  documents_embeddings = np.array(documents_embeddings) # convert to numpy array

  # Reshape the query vector embedding to a matrix of shape (1, n) to make it compatible with cosine_similarity
  query_embedding = query_embedding.reshape(1, -1)

  # Calculate the similarity for each item in data
  cosine_sim = cosine_similarity(query_embedding, documents_embeddings)

  # Sort the data by similarity in descending order and take the top k items
  sorted_indices = np.argsort(cosine_sim[0])[::-1]

  # Take the top k related embeddings
  top_k_related_indices = sorted_indices[:k]
  top_k_related_embeddings = documents_embeddings[sorted_indices[:k]]
  top_k_related_embeddings = [list(row[:]) for row in top_k_related_embeddings] # convert to list

  return top_k_related_embeddings, top_k_related_indices


voyageai.api_key = "pa-dQ28MnYTDY5xF72HnbBVB5-w9FCs7E6yzzZBbAn0YPk"
    
vo = voyageai.Client()

with open('icrc_embeddings.jsonl', 'r') as json_file:
    documents_embeddings = json.load(json_file)
print(len(documents_embeddings))
query_embedding = vo.embed('A patient with a high fever talks to a medical assistant in Kenya', model="voyage-large-2-instruct", input_type="query").embeddings

#reads all the documents in icrc_split.jsonl and stores them in data
data = []
for root, dirs, files in os.walk('icrc_split.jsonl'):
    for filename in files:
        if filename.endswith('.json'):
            file_path = os.path.join(root, filename)
            with open(file_path, 'r') as json_file:
                data.append(json.load(json_file))

retrieved_embd, retrieved_embd_index = k_nearest_neighbors(query_embedding, documents_embeddings, k=3)
retrieved_doc = [data[index] for index in retrieved_embd_index]

print(retrieved_doc)


