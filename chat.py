import os
import openai



def chat(messages):
    print(messages)

    # create a chat completion
    openai.api_base = "http://localhost:8080/v1"
    openai.api_key = "key-1234567890"
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    # print the completion
    print(chat_completion.choices[0].message.content)

    return chat_completion.choices[0].message.content
