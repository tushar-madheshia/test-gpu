# import gradio as gr

def echo(message, history):
    return message

# demo = gr.ChatInterface(fn=echo, examples=["hello", "hola", "merhaba"], title="Echo Bot")

#demo.queue().launch(root_path="/test")

from fastapi import FastAPI
import gradio as gr
import uvicorn
import os

path = os.environ["BASE_URL"]

print("base url is ",path)

app = FastAPI()


g_app = gr.ChatInterface(fn=echo, examples=["hello", "hola", "merhaba"], title="Echo Bot")
app = gr.mount_gradio_app(app, g_app, path=path)
uvicorn.run(app,host="0.0.0.0",port=7860)


