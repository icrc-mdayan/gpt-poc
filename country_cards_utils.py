import requests
import json
import pandas as pd
from tqdm import tqdm
import os
from fuzzywuzzy import process

def filter_csv(age_group, sex, location):
    df_original = pd.read_csv(f"scripts/cards/{location}.csv")
    df = df_original[(df_original['age_group_name'] == age_group) & (df_original['sex_label'] == sex)]
    
    if len(df) == 0:
        df = df_original[(df_original['age_group_name'] == "All Ages") & (df_original['sex_label'] == sex)]

    df['mean_estimate'] = pd.to_numeric(df['mean_estimate'], errors='coerce')

    ranked_df = df.groupby('indicator_name').agg({'mean_estimate': 'mean'}).reset_index()
    ranked_df = ranked_df.sort_values(by='mean_estimate', ascending=False).reset_index(drop=True)

    return ranked_df

def process_csv(df):
    df = df.head(3)
    text_information = "Based on the location, sex and age group you selected, here are the most prevalent diseases from this region:\n"

    for i, row in df.iterrows():
        text_information += f"{i+1}.{row['indicator_name']}\n"

    return text_information

sex_label_dict = {"Male": "Males", "Female": "Females", "Other": "Both sexes"}

age_group_dict = {
    (0, 0): "Neonatal",
    (1, 4): "Under 5",
    (15, 49): "15-49 years"
}

def get_age_group(age):
    for age_range, category in age_group_dict.items():
        if age_range[0] <= int(age) <= age_range[1]:
            return category
    return "Age-standardized"


def get_closest_location(user_input, location_name_dict):
    location_names = list(location_name_dict.values())
    closest_match = process.extractOne(user_input, location_names)
    # closest_match is a tuple (matched_string, score)
    if closest_match[0]:
        return closest_match[0]
    return None

def process_user_entries(age, sex, user_location):
    location_name_dict = json.load(open('scripts/location_name_dict.json'))
    age_group = get_age_group(age)
    sex_label = sex_label_dict[sex]
    location = get_closest_location(user_location, location_name_dict)

    return age_group, sex_label, location