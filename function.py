import os
import requests
from typing import List, Dict

def lookup_location_id(location: str):
    """
    TODO
    """
    pass

def get_current_weather(location: str):
    """
    TODO
    """
    pass

def add_todo(todo: str):
    """
    TODO
    """
    pass

def function_calling(messages: List[Dict]):
    """
    TODO
    """
    pass

if __name__ == "__main__":
    messages = [{"role": "user", "content": "What's the weather like in Beijing?"}]
    response = function_calling(messages)
    print(response)

    messages = [{"role": "user", "content": "Add a todo: walk"}]
    response = function_calling(messages)
    print(response)