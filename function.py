import os
import requests
from typing import List, Dict
import openai
import json
openai.api_key = "sk-1234567890"
openai.api_base = "http://166.111.80.169:8080/v1"


def lookup_location_id(location: str):
    # 调用城市搜索API获取地理位置ID
    api_key = "fe9f0bfd2146458687c3cebe84d6c3e8"
    url = f"https://geoapi.qweather.com/v2/city/lookup?location={location}&key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        location_id = data["location"][0]["id"] if data else None
        return location_id
    except Exception as e:
        print(f"Error looking up location ID: {e}")
        return None

def get_current_weather(location: str):
    location_id = lookup_location_id(location)
    if location_id:
        # 调用实时天气API获取天气信息
        api_key = "fe9f0bfd2146458687c3cebe84d6c3e8"
        url = "https://devapi.qweather.com/v7/weather/now"
        params = {"location": location_id, "key": api_key}

        try:
            response = requests.get(url, params=params)
            data = response.json()
            temperature = data["now"]['feelsLike']
            description = data["now"]["text"]
            humidity = data["now"]['humidity']
            weather_info = f"Temperature: {temperature} Description: {description} Humidity: {humidity}"
            return weather_info
        except Exception as e:
            print(f"Error getting current weather: {e}")
            return "Unable to retrieve weather information"
    else:
        return "Location not found"


# 记录TODO项的列表
todo_list = []


def add_todo(todo):
    # 将TODO项添加到列表中
    todo_list.append(todo)
    return "\n".join(todo_list)


functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
            },
            "required": ["location"],
        },
    },
    {
        "name": "add_todo",
        "description": "Add a TODO item to the list",
        "parameters": {
            "type": "object",
            "properties": {
                "todo": {
                    "type": "string",
                    "description": "add something to the todo list",
                },
            },
        },
    }
]


def function_calling(messages):
    response = openai.ChatCompletion.create(
        model="ggml-openllama.bin",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    function_call = response["choices"][0]["message"]["function_call"]
    function = function_call["function"]
    function_args = json.loads(function_call["arguments"])
    if function == "get_current_weather":
        location = function_args["location"]
        return get_current_weather(location)
    elif function == "add_todo":
        todo = function_args["todo"]
        return add_todo(todo)
if __name__ == "__main__":
    messages = [{"role": "user", "content": "What's the weather like in Beijing?"}]
    response = function_calling(messages)
    print(response)

    messages = [{"role": "user", "content": "Add a todo: walk"}]
    response = function_calling(messages)
    print(response)