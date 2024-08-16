import requests
import xml.etree.ElementTree as ET

def get_dimension_values(xml_response, dimension_label):
    """
    Extracts all possible values for a given dimension from the XML response.

    Args:
    - xml_response: The XML response as a string.
    - dimension_label: The label of the dimension (e.g., 'SEX', 'AGEGROUP', 'COUNTRY', 'YEAR').

    Returns:
    - A list of possible values for the specified dimension.
    """
    # Parse the XML response
    root = ET.fromstring(xml_response)
    
    # Initialize an empty list to store the possible values
    dimension_values = []
    
    # Find all Code elements under the specified Dimension element
    for code in root.findall(f".//Dimension[@Label='{dimension_label}']/Code"):
        # Extract the Label attribute which represents the value
        dimension_value = code.get('Label')
        # Append the value to the list
        dimension_values.append(dimension_value)
    
    return dimension_values

dimension_code = "SEX"
indicator_code = "MLE"
url = f"http://apps.who.int/gho/athena/api/{dimension_code}/{indicator_code}"
response = requests.get(url)
print(response.text)