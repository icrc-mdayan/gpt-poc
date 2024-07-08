import os
import json

# from torch import Tensor
# from transformers import AutoTokenizer, AutoModel

# def get_detailed_instruct(task_description: str, query: str) -> str:
#     return f'Instruct: {task_description}\nQuery: {query}'

# def last_token_pool(last_hidden_states: Tensor,
#                  attention_mask: Tensor) -> Tensor:
#     left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
#     if left_padding:
#         return last_hidden_states[:, -1]
#     else:
#         sequence_lengths = attention_mask.sum(dim=1) - 1
#         batch_size = last_hidden_states.shape[0]
#         return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]

# model = SentenceTransformer("Alibaba-NLP/gte-Qwen2-1.5B-instruct", trust_remote_code=True)
# # In case you want to reduce the maximum length:
# model.max_seq_length = 8192
# #read all the documents in icrc_split.jsonl
# for root, dirs, files in os.walk('icrc_split.jsonl'):
#     for filename in files:
#         if filename.endswith('.json'):
#             file_path = os.path.join(root, filename)
#             with open(file_path, 'r') as json_file:
#                 data = json.load(json_file)
#             #get the embeddings for each sequence
#             embeddings = model.encode(data)
#             #save the embeddings to a new file
#             name = filename.split('.')[0] + f'_embeddings.json'
#             new_file_path = os.path.join('icrc_embeddings.jsonl', name)
#             with open(new_file_path, 'w') as new_json_file:
#                 json.dump(embeddings, new_json_file)
from sklearn.metrics.pairwise import cosine_similarity
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

import voyageai
voyageai.api_key = "pa-dQ28MnYTDY5xF72HnbBVB5-w9FCs7E6yzzZBbAn0YPk"
    
vo = voyageai.Client()
import numpy as np
# data = []
# for root, dirs, files in os.walk('icrc_split.jsonl'):
#     for filename in files:
#         if filename.endswith('.json'):
#             file_path = os.path.join(root, filename)
#             with open(file_path, 'r') as json_file:
#                 data.append(json.load(json_file))
# print(len(data))
# batch_size = 128
# embeddings = []
# for i in range(0, len(data), batch_size):
#     embedding = vo.embed(
#         data[i:i + batch_size], model="voyage-large-2-instruct", input_type="document"
#     ).embeddings
#     embeddings.append(embedding)

# with open('icrc_embeddings.jsonl', 'w') as json_file:
#     json.dump(embeddings, json_file)
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


