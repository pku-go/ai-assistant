import requests
import json
import os
import requests
import json

def image_generate(content):

    api_endpoint = "http://localhost:8080/v1/images/generations"
    
    payload = {
        "prompt": content,
        "size": "256x256"
    }

    try:
        response = requests.post(api_endpoint, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            result = response.json()
            generated_image_url = result['data'][0]['url']

            return generated_image_url
        else:
            return None

    except Exception as e:
        return None
    