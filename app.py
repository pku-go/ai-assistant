import gradio as gr
import os
from chat import *

from mnist import *
from pdf import *
from stt import *
from tts import *
from image_generate import *
# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.

messages = []
current_file_text = None


def get_chatResponse(messages):
    response = chat(messages)
    results = ""
    for chunk in response:
        try:
            results += chunk['choices'][0]['delta']['content']
            yield results
        except KeyError:
            pass

def get_textResponse(prompt):
    response = generate_text(prompt)
    results = ""
    for chunk in response:
        try:
            results += chunk['choices'][0]['text']
            yield results
        except KeyError:
            pass

def add_text(history, text):
    history = history + [(text, None)]
    if text.startswith("/search"):
        pass
    elif text.startswith("/fetch"):
        pass
    elif text.startswith("/file"):
        content = text[6:]
        file_name = history[-2][0][0]
        with open(file_name, 'r', encoding="utf-8") as f:
            current_file_text = f.read()
            # current_file_text = f.read().replace('\n', ' ')
        new_message = {
            "role": "user",
            "content": generate_answer(current_file_text, content)
        }
        messages.append(new_message)
    else:
        new_message = {
            "role": "user",
            "content": history[-1][0]
        }
        messages.append(new_message)
    return history, gr.update(value="", interactive=False)


def add_file(history, file):
    history = history + [((file.name,), None)]
    if file.name.endswith((".wav")):
        new_message = {
            "role": "user",
            "content": audio2text(file)
        }
        messages.append(new_message)
    elif file.name.endswith((".png")):
        new_message = {
            "role": "user",
            "content": f"Please classify {file.name}"
        }
        messages.append(new_message)
    elif file.name.endswith((".txt")):
        with open(file.name, 'r', encoding="utf-8") as f:
            current_file_text = f.read()
            # current_file_text = f.read().replace('\n', ' ')
        new_message = {
            "role": "user",
            "content": generate_summary(current_file_text)
        }
        messages.append(new_message)
    return history


def bot(history):
    if type(history[-1][0]) == str:
        '''
        TODO refresh history[-1][1] and messages
        '''
        if history[-1][0].startswith(("/search")):
            pass

        elif history[-1][0].startswith(("/fetch")):
            pass

        elif history[-1][0].startswith(("/image")):
            content = history[-1][0][7:]
            url = image_generate(content)
            new_message = {
                "role": "assistant",
                "content": url
            }
            messages.append(new_message)
            history[-1][1] = (url,)
            yield history

        elif history[-1][0].startswith(("/audio")):
            messages[-1]["content"] = messages[-1]["content"][7:]
            for new_history in get_chatResponse(messages):
                history[-1][1] = new_history
            path = text2audio(history[-1][1])
            messages[-1]["content"] = "/audio " + messages[-1]["content"]
            new_message = {
                "role": "assistant",
                "content": history[-1][1]
            }
            messages.append(new_message)
            history[-1][1] = (path,)
            yield history

        elif history[-1][0].startswith(("/file")):
            question = messages[-1]["content"]
            for new_history in get_textResponse(question):
                history[-1][1] = new_history
                yield history
            # history[-1][1] = ""
            # for chunk in generate_text(question):
            #     try:
            #         history[-1][1] += chunk['choices'][0]['text']
            #         yield history
            #     except KeyError:
            #         pass
            new_message = {
                "role": "assistant",
                "content": history[-1][1]
            }
            messages.append(new_message)

        elif history[-1][0].startswith(("/function")):
            pass

        else:
            for new_history in get_chatResponse(messages):
                history[-1][1] = new_history
                yield history
            new_message = {
                "role": "assistant",
                "content": history[-1][1]
            }
            messages.append(new_message)

    elif type(history[-1][0]) == tuple:

        if history[-1][0][0].endswith((".wav")):
            for new_history in get_chatResponse(messages):
                history[-1][1] = new_history
                yield history

        elif history[-1][0][0].endswith((".png")):
            new_message = {
                "role": "assistant",
                "content": image_classification(history[-1][0][0])
            }
            messages.append(new_message)
            history[-1][1] = new_message['content']
            yield history
        elif history[-1][0][0].endswith((".txt")):
            summary_prompt = messages[-1]['content']
            for new_history in get_textResponse(summary_prompt):
                history[-1][1] = new_history
                yield history
            # history[-1][1] = ""
            # for chunk in generate_text(summary_prompt):
            #     try:
            #         history[-1][1] += chunk['choices'][0]['text']
            #         yield history
            #     except KeyError:
            #         pass
            new_message = {
                "role": "assistant",
                "content": history[-1][1]
            }
            messages.append(new_message)

    return history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        avatar_images=(
            None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        clear_btn = gr.Button('Clear')
        btn = gr.UploadButton(
            "📁", file_types=["image", "video", "audio", "text"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt],
                         queue=False).then(bot, chatbot, chatbot)
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot],
                          queue=False).then(bot, chatbot, chatbot)
    clear_btn.click(lambda: messages.clear(), None, chatbot, queue=False)

demo.queue()
demo.launch()
