import gradio as gr
import os
import time
from chat import *
from stt import *

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


def add_text(history, text):
    history = history + [(text, None)]
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
    elif file.name.endswith((".png")):
        '''
        TODO
        '''
        pass
    elif file.name.endswith((".txt")):
        '''
        TODO
        '''
        pass
    messages.append(new_message)
    return history


def bot(history):
    print(history)
    if type(history[-1][0]) == str:
        '''
        TODO refresh history[-1][1]
        '''
        if history[-1][0].startswith(("/search")):
            pass
        elif history[-1][0].startswith(("/fetch")):
            pass
        elif history[-1][0].startswith(("/image")):
            pass
        elif history[-1][0].startswith(("/audio")):
            pass
        elif history[-1][0].startswith(("/file")):
            pass
        elif history[-1][0].startswith(("/function")):
            pass
        else:
            for new_history in get_chatResponse(messages):
                history[-1][1] = new_history
                yield history
    elif type(history[-1][0]) == tuple:
        if history[-1][0][0].endswith((".wav")):
            for new_history in get_chatResponse(messages):
                history[-1][1] = new_history
                yield history
        elif history[-1][0][0].endswith((".png")):
            '''
            TODO refresh history[-1][1]
            '''
            pass
        elif history[-1][0][0].endswith((".txt")):
            pass
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

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear_btn.click(lambda: messages.clear(), None, chatbot, queue=False)

demo.queue()
demo.launch()
