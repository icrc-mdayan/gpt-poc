import os
import shutil
import seaborn as sns
import matplotlib.pyplot as plt

def count_characters_in_files(directory):
    country_character_counts = {}
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            country_name = filename.replace("_", " ").replace(".txt", "")
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                content = file.read()
                character_count = len(content)
                country_character_counts[country_name] = character_count
    
    return country_character_counts

def categorize_files(directory):
    empty_dir = os.path.join(directory, "cards_empty")
    big_dir = os.path.join(directory, "cards_5000")
    rest_dir = os.path.join(directory, "cards_big")

    # Create directories if they don't exist
    os.makedirs(empty_dir, exist_ok=True)
    os.makedirs(big_dir, exist_ok=True)
    os.makedirs(rest_dir, exist_ok=True)

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                character_count = len(content)
                
                if character_count == 0:
                    shutil.copy(file_path, empty_dir)
                elif character_count > 5000:
                    shutil.copy(file_path, big_dir)
                else:
                    shutil.copy(file_path, rest_dir)

# Directory containing the .txt files
input_dir = "country_cards"

# Count characters in each file
character_counts = count_characters_in_files(input_dir)

# Categorize files based on character count
categorize_files(input_dir)

# Create a seaborn plot
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))
sns.barplot(x=list(character_counts.keys()), y=list(character_counts.values()))
plt.xticks(rotation=90)
plt.xlabel("Country")
plt.ylabel("Number of Characters")
plt.title("Character Count in Health Sections of African Countries")
plt.tight_layout()

# Show plot
plt.show()
