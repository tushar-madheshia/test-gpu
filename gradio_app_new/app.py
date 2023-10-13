import gradio as gr
import os
def echo(message, history):
    return message

demo = gr.ChatInterface(fn=echo, examples=["hello", "hola", "merhaba"], title="Echo Bot")
demo.queue().launch(root_path=os.environ["BASE_URL"])