import os
import re

def generate_text(prompt):
    """
    TODO
    """
    pass

def generate_answer(current_file_text: str, content: str):

    # TODO
    content = f"Please answer {content} based on the following text: \n\n{current_file_text}"

    pass

def generate_summary(current_file_text: str):    

    pass

if __name__ == "__main__":
    prompt = generate_answer("Hello", "Who is Sun Wukong?")
    generate_text(prompt)