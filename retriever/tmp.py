#For every file in icrc_split_2.jsonl, we will save the data to a new file
import os
import json
data = []
for root, dirs, files in os.walk('icrc_split_2.jsonl'):
    for filename in files:
        if filename.endswith('.json'):
            file_path = os.path.join(root, filename)
            with open(file_path, 'r') as json_file:
                data.append(json.load(json_file))
with open('icrc_split.jsonl', 'w') as json_file:
    json.dump(data, json_file)