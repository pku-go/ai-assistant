import openai

def generate_text(prompt):

    openai.api_base = "http://localhost:8080/v1"
    openai.api_key = "key-1234567890"

    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        temperature=0.7,
        stream=True
    )

    return response


def generate_answer(current_file_text: str, content: str):

    question = f"Please answer {content} based on the following text: \n\n{current_file_text}"

    return question


def generate_summary(current_file_text: str):    

    summary_prompt = f"Act as a summarizer. Please summarize the following text: \n\n{current_file_text}"

    return summary_prompt
