import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

def search(content: str):
    """
    TODO
    """
    url = "https://serpapi.com/search"

    params = {
        "engine": "bing",
        "q": content,
        "api_key": "73e3bed51180c24bb080792cc1dd281cfc6230433db299b1d8a74deddf82f5d7",
    }

    try:
        response = requests.get(url, params)
        
        if response.status_code == 200:
            
            search_results = response.json()

            # 获取第一条搜索结果的snippet字段
            snippet = search_results["organic_results"][0]["snippet"]

            question = f"Please answer {content} based on the search result: {snippet}"

            return question
        
        else:
            print(f"Error: {response.status_code}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    search("Sun Wukong")