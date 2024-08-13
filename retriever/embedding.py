import os
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import voyageai
import numpy as np
import cohere
import hnswlib

class Vectorstore:
    def __init__(self, document_embeddings = None, data = None, shape=1024):
        self.documents_embeddings = document_embeddings
        self.data = data
        voyageai.api_key = "pa-dQ28MnYTDY5xF72HnbBVB5-w9FCs7E6yzzZBbAn0YPk"
        self.vo = voyageai.Client()
        self.co = cohere.Client("5h8nFK1B6NLl9qVyqgwjBqA6wt3iOIfGfUaud4TG")
        self.idx = hnswlib.Index(space='cosine', dim=shape)
        self.idx.init_index(max_elements=len(self.documents_embeddings), ef_construction=200, M=16)
        self.idx.add_items(self.documents_embeddings)

    def k_nearest_neighbors(self, query_embedding, k=5, max_length = 5000):
        query_embedding = np.array(query_embedding) # convert to numpy array
        self.documents_embeddings = np.array(self.documents_embeddings) # convert to numpy array

        # Reshape the query vector embedding to a matrix of shape (1, n) to make it compatible with cosine_similarity
        query_embedding = query_embedding.reshape(1, -1)

        # Calculate the similarity for each item in data
        cosine_sim = cosine_similarity(query_embedding, self.documents_embeddings)
        
        # Sort the data by similarity in descending order and take the top k items
        sorted_indices = np.argsort(cosine_sim[0])[::-1]
        sorted_args = np.sort(cosine_sim[0])[::-1]
        #if args are smaller than 0.7 we return an empty list
        if sorted_args[0] < 0.7:
            return []
        # Take the top k related embeddings
        top_k_related_indices = sorted_indices[:k]
        #   top_k_related_embeddings = documents_embeddings[sorted_indices[:k]]
        #   top_k_related_embeddings = [list(row[:]) for row in top_k_related_embeddings] # convert to list
        retrieved_doc = []
        total_length = 0
        for index in top_k_related_indices:
            retrieved_doc.append(self.data[index])
            total_length += len(self.data[index])
            # if total_length > max_length:
            #     break
        

        return retrieved_doc #top_k_related_embeddings, top_k_related_indices

    def retrieve_documents(self, query, k=10):
        #with open('retriever/icrc_embeddings.jsonl', 'r') as json_file:
        
        # documents_embeddings_array = np.array(documents_embeddings)
        # reshaped_documents_embeddings = documents_embeddings_array.reshape(len(documents_embeddings), len(documents_embeddings[0][0]))
        # with open('retriever/icrc_embeddings_reshaped.jsonl', 'w') as json_file:
        #     json.dump(reshaped_documents_embeddings, json_file)
            
        query_embedding = self.vo.embed(query, model="voyage-large-2-instruct", input_type="query").embeddings

        #reads all the documents in icrc_split.jsonl and stores them in data
        #with open('retriever/icrc_split.jsonl', 'r') as json_file:
        #    data = json.load(json_file)
        
        # data = []
        # for root, dirs, files in os.walk('retriever/icrc_split_2.jsonl'):
        #     for filename in files:
        #         if filename.endswith('.json'):
        #             file_path = os.path.join(root, filename)
        #             with open(file_path, 'r') as json_file:
        #                 data.append(json.load(json_file))
        
        max_length=2000
        #top_docs = self.k_nearest_neighbors(query_embedding, k=k, max_length=max_length)
        retrieved_embed, distance = self.idx.knn_query(query_embedding, k=k)
        top_docs = [self.data[index] for index in retrieved_embed[0]]
        results = self.co.rerank(model= "rerank-english-v3.0", query=query, documents=[doc["text"] for doc in top_docs], top_n = 5).results
        total_length = 0
        retrieved_doc = []  
        for res in results:
            # if res.relevance_score < 0.7:
            #     break
            #quick and dirty fix
            if top_docs[res.index]["source_document"] == "**Tropical diseases ethiology, pathologies and treatment":
                continue
            retrieved_doc.append(top_docs[res.index])
            total_length += len(top_docs[res.index]["text"])
            if total_length > max_length:
                break
        return retrieved_doc, query_embedding


if __name__ == "__main__":
    documents_embeddings = []
    voyageai.api_key = "pa-dQ28MnYTDY5xF72HnbBVB5-w9FCs7E6yzzZBbAn0YPk"
        
    vo = voyageai.Client()
    data = []
    with open('retriever/books_split_final.jsonl', 'r') as json_file:
        for line in json_file:
            data.append(json.loads(line)["text"])
    new_data = []
    #new data is data,but with a maximum of 20000 characaters per document
    for document in data:
        if len(document) > 8000:
            new_data.append(document[:8000])
        else:
            new_data.append(document)

    print(len(new_data))
    for i in range(5632, len(new_data), 128):
        print(i)
        embed = vo.embed(new_data[i:i+128], model="voyage-large-2-instruct", input_type="document").embeddings
        for emb in embed:
            documents_embeddings.append(emb) 
            with open('retriever/tmp.jsonl', 'a') as json_file:
                json.dump(emb, json_file)
                json_file.write('\n')
    with open('retriever/books_embeddings_2.jsonl', 'w') as json_file:
        json.dump(documents_embeddings, json_file)
            