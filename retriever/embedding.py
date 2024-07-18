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
  sorted_args = np.sort(cosine_sim[0])[::-1]
  #if args are smaller than 0.7 we return an empty list
  if sorted_args[0] < 0.7:
    return None, None
  # Take the top k related embeddings
  top_k_related_indices = sorted_indices[:k]
  top_k_related_embeddings = documents_embeddings[sorted_indices[:k]]
  top_k_related_embeddings = [list(row[:]) for row in top_k_related_embeddings] # convert to list

  return top_k_related_embeddings, top_k_related_indices

def retrieve_documents(query, k=5):
    voyageai.api_key = "pa-dQ28MnYTDY5xF72HnbBVB5-w9FCs7E6yzzZBbAn0YPk"
        
    vo = voyageai.Client()

    #with open('retriever/icrc_embeddings.jsonl', 'r') as json_file:
    with open('retriever/books_embeddings.jsonl', 'r') as json_file:
        documents_embeddings = json.load(json_file)
    # documents_embeddings_array = np.array(documents_embeddings)
    # reshaped_documents_embeddings = documents_embeddings_array.reshape(len(documents_embeddings), len(documents_embeddings[0][0]))
    # with open('retriever/icrc_embeddings_reshaped.jsonl', 'w') as json_file:
    #     json.dump(reshaped_documents_embeddings, json_file)
        
    query_embedding = vo.embed(query, model="voyage-large-2-instruct", input_type="query").embeddings

    #reads all the documents in icrc_split.jsonl and stores them in data
    #with open('retriever/icrc_split.jsonl', 'r') as json_file:
    #    data = json.load(json_file)
    data = []
    with open('retriever/books.json', 'r') as json_file:
        for line in json_file:
            data.append(json.loads(line)["text"])
    # data = []
    # for root, dirs, files in os.walk('retriever/icrc_split_2.jsonl'):
    #     for filename in files:
    #         if filename.endswith('.json'):
    #             file_path = os.path.join(root, filename)
    #             with open(file_path, 'r') as json_file:
    #                 data.append(json.load(json_file))
    
    
    retrieved_embd, retrieved_embd_index = k_nearest_neighbors(query_embedding, documents_embeddings, k=2)
    if retrieved_embd_index is None:
        return []
    retrieved_doc = [data[index] for index in retrieved_embd_index]

    return retrieved_doc


if __name__ == "__main__":
    documents_embeddings = []
    voyageai.api_key = "pa-dQ28MnYTDY5xF72HnbBVB5-w9FCs7E6yzzZBbAn0YPk"
        
    vo = voyageai.Client()
    data = []
    with open('retriever/books.json', 'r') as json_file:
        for line in json_file:
            data.append(json.loads(line)["text"])
    #Je devrais pas faire doc par doc, mais faire par batch et après ajouter chaque embedded document dans documents_embeddings
    print(len(data))
    for i in range(0, len(data), 100):
        print(i)
        embed = vo.embed(data[i:i+100], model="voyage-large-2-instruct", input_type="document").embeddings
        for emb in embed:
            documents_embeddings.append(emb) 
    with open('retriever/books_embeddings.jsonl', 'w') as json_file:
        json.dump(documents_embeddings, json_file)
