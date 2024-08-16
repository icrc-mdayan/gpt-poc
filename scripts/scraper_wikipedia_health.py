import os
import requests
from bs4 import BeautifulSoup, Tag
import re

# List of African countries
african_countries = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", 
    "Cameroon", "Central African Republic", "Chad", "Comoros", "Congo", "Democratic Republic of the Congo", 
    "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", 
    "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", 
    "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", 
    "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", 
    "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", 
    "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
]

def fetch_health_section(country_url):
    response = requests.get(country_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page: {country_url}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    html_lines = str(soup).split('\n')
    
    start_extracting = False
    health_content = []

    for line in html_lines:
        if '<h3 id="Health">' in line:
            start_extracting = True
        elif ('<h3 id="Education">' in line or '<h2 id="Culture">' in line or 'h2 id="Urbanization">' in line) and start_extracting:
            break
        if start_extracting:
            health_content.append(line.strip())

    return ' '.join(health_content)

def remove_bracketed_numbers(text):
    # Use regular expression to find and remove brackets with numbers inside
    cleaned_text = re.sub(r'\[\d+\]', '', text)
    return cleaned_text

# Create directory to save country health info
output_dir = "country_cards"
os.makedirs(output_dir, exist_ok=True)

base_url = "https://en.wikipedia.org/wiki/"

for country in african_countries:
    country_name = country.replace(" ", "_")
    country_url = f"{base_url}{country_name}#Health"
    try:
        health_info = fetch_health_section(country_url)
        soup = BeautifulSoup(health_info, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        cleaned_text = remove_bracketed_numbers(text)
        
        # Save to a .txt file
        with open(os.path.join(output_dir, f"{country_name}.txt"), "w", encoding="utf-8") as file:
            file.write(cleaned_text)
        
        print(f"Saved health info for {country}")
    except Exception as e:
        print(f"Failed to fetch health info for {country}: {e}")
