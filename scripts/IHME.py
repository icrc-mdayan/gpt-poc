import requests
import json
import pandas as pd

# Your API Secret Key (replace 'YOUR_SECRET_KEY' with the actual key)
api_key = 'p3a88u9bwh8d8npn53g7htra8cxgeh8y'

# Set the base URL for the API request
base_url = "https://api.healthdata.org/sdg/v1/GetResultsByLocation"

location_id = 149 

# Set the year you are interested in
year = 2023  # Replace with the desired year

# Define the headers with your API key
headers = {
    'Content-Type': 'application/json',
    'Authorization': api_key
}

# Construct the full API request URL
url = f"{base_url}?location_id={location_id}&year={year}"

print(url)

# Make the GET request to the API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # If successful, parse the JSON data
    data = response.json()

    # save the json in a json file
    with open('palestine_.json', 'w') as f:
        json.dump(data, f)

    df = pd.DataFrame(data["results"])
    with open('palestine.csv', 'w') as f:
        df.to_csv(f)

    # Assuming the API returns a URL to download the CSV file
    csv_url = data.get("csv_url")

    if csv_url:
        # Download the CSV file
        csv_response = requests.get(csv_url)

        # Save the CSV file locally
        with open("nigeria_most_deaths.csv", "wb") as file:
            file.write(csv_response.content)

        print("CSV file downloaded and saved as 'nigeria_most_deaths.csv'.")
    else:
        print("CSV URL not found in the response.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    print(f"Response: {response.text}")

print(df.head(1))

