import requests

def audio2text(file):
    url = 'http://localhost:8080/v1/audio/transcriptions'
    files = {
        'file': open(file.name, 'rb'),
        'model': (None, 'whisper-1')
    }

    response = requests.post(url=url, files=files)
    return response.json()['text']
