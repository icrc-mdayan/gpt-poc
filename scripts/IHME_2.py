from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

# Step 1: Set up Selenium WebDriver
# Make sure to download the correct WebDriver for your browser and specify the path
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

# Step 2: Open the webpage using Selenium
url = "https://www.healthdata.org/research-analysis/health-by-location/profiles/palestine#main-content"
driver.get(url)

# Optional: Wait for the page to fully load if necessary (increase time if needed)
time.sleep(10)  # Adjust the sleep time if the page takes longer to load

# Step 3: Locate the CSV download link
# This might require inspecting the element on the page; adjust the selector accordingly
try:
    # Example: If the link has specific text or attributes, adjust the By selector
    csv_link_element = driver.find_element(By.PARTIAL_LINK_TEXT, 'CSV')
    csv_link = csv_link_element.get_attribute('href')
    print(f"CSV link found: {csv_link}")

    # Step 4: Download the CSV file using requests
    csv_response = requests.get(csv_link)
    csv_response.raise_for_status()  # Check that the request was successful

    # Step 5: Save the CSV file locally
    with open('top_10_causes_of_death.csv', 'wb') as file:
        file.write(csv_response.content)
    print("CSV file downloaded successfully.")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Step 6: Close the Selenium WebDriver
    driver.quit()
