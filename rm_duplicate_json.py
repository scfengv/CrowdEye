import os
import json

from tqdm import tqdm


def remove_duplicate_content(path):

    '''
    input the folder path that have the json data to be modified
    '''

    with open(fr"{path}", "r") as f:
        data = json.load(f)

    unique_content = set()
    filtered_data = []

    for item in data:
        content = item.get("content")
        if content not in unique_content:
            unique_content.add(content)
            filtered_data.append(item)

    with open(fr"{path}", "w") as f:
        json.dump(filtered_data, f, indent = 4)

folder_path = "TVL19_chat"
files = os.listdir(folder_path)

json_files = [file for file in files if file.endswith('.json')]

for file in tqdm(json_files):
    remove_duplicate_content(f"{folder_path}/{file}")