
import requests
from datetime import datetime
import os

def text2audio(content: str):
    url = 'http://localhost:8080/tts'
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'model': 'en-us-ryan-high.onnx',
        'input': content,
    }

    audio_dir = "./audio"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    response = requests.post(url, headers=headers, json=json_data)

    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    audio_file = f"{audio_dir}/{current_time}_answerAudio.wav"
    with open(audio_file, "wb") as output:
        output.write(response.content)

    return audio_file
    


    

# if __name__ == "__main__":
#     text2audio("Sun Wukong (also known as the Great Sage of Qi Tian, Sun Xing Shi, and Dou Sheng Fu) is one of the main characters in the classical Chinese novel Journey to the West")