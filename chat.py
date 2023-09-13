import os
import openai


def chat(messages):

    # # create a chat completion
    openai.api_base = "http://localhost:8080/v1"
    openai.api_key = "key-1234567890"

    # a ChatCompletion request
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.7,
        stream=True
    )

    return response
