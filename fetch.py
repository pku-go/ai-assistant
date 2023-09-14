import requests
from bs4 import BeautifulSoup

def fetch(url: str):

    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, "html.parser")

            p_tags = soup.find_all("p")
            extracted_text = p_tags[1].text
            search_content = extracted_text.strip()

            question = f"Act as a summarizer. Please summarize {url}. The following is the content: {search_content}"

            return question
        
        else:
            print(f"Error: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")
