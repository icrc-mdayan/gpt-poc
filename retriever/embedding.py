import os
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import voyageai
import numpy as np
import cohere
import hnswlib
import sys

class Vectorstore:
    def __init__(self, document_embeddings = None, data = None, shape=1024, voyageai_api_key = None, cohere_api_key = None):
        self.documents_embeddings = document_embeddings
        self.data = data
        voyageai.api_key = voyageai_api_key
        self.vo = voyageai.Client()
        self.co = cohere.Client(cohere_api_key)
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
        retrieved_doc = []
        total_length = 0
        for index in top_k_related_indices:
            retrieved_doc.append(self.data[index])
            total_length += len(self.data[index])
        

        return retrieved_doc #top_k_related_embeddings, top_k_related_indices

    def retrieve_documents(self, query, k=10):            
        query_embedding = self.vo.embed(query, model="voyage-large-2-instruct", input_type="query").embeddings
        
        max_length=1500
        retrieved_embed, distance = self.idx.knn_query(query_embedding, k=k)

        top_docs = [self.data[index] for index, distance in zip(retrieved_embed[0], distance[0]) if distance < 0.25]
        if len(top_docs) == 0:
            return [], query_embedding
        else:
            results = self.co.rerank(model= "rerank-english-v3.0", query=query, documents=[doc["text"] for doc in top_docs], top_n = 5).results
            total_length = 0
            retrieved_doc = []  
            for res in results:
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
    with open('API_token.json', 'r') as json_file:
        api_keys = json.load(json_file)
    voyageai.api_key = api_keys["voyageai"]

        
    vo = voyageai.Client()
    data = []
    with open(sys.argv[1], 'r') as json_file:
        for line in json_file:
            data.append(json.loads(line)["text"])
    new_data = []
    #new data is data,but with a maximum of 8000 characaters per document
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
    with open(sys.argv[2], 'w') as json_file:
        json.dump(documents_embeddings, json_file)
            