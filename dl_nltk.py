import nltk
import os

def download_resources(data_dir):
    # Set the NLTK data path to the specified directory
    nltk.data.path.append(data_dir)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Download the required NLTK resource into the specified directory
    nltk.download('punkt', download_dir=data_dir)
    nltk.download('punkt_tab', download_dir=data_dir)

if __name__ == "__main__":
    data_dir = os.path.join(os.getcwd(), 'data')
    download_resources(data_dir)
