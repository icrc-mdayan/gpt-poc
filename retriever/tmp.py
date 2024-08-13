#reads books_2.jsonl and discards elements that have only one sentence in text
import json
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

data = []
with open('retriever/books_split.jsonl', 'r') as json_file:
    for line in json_file:
        text = json.loads(line)["text"]
        if text is not None:
            sentences = sent_tokenize(text)
            if len(sentences) > 2:
                data.append(json.loads(line))

with open('retriever/books_split_2.jsonl', 'w') as json_file:
    for text in data:
        json.dump(text, json_file)
        json_file.write('\n')
# import json
# embeddings = []
# with open('retriever/tmp.jsonl', 'r') as file:
#     for line in file:
#             # Parse the JSON data from the line
#             emb = json.loads(line)
            
#             # Append the embedding to the list
#             embeddings.append(emb)
# #save the embeddings in a json file
# with open('retriever/books_embeddings_2.jsonl', 'w') as json_file:
#       json.dump(embeddings, json_file)