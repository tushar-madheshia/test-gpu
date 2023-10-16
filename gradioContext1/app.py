# import gradio as gr

def echo(message, history):
    return message


import torch
from transformers import pipeline
pipe = pipeline("text-generation", model="/data/huggingface/cache/models--HuggingFaceH4--starchat-beta/snapshots/b1bcda690655777373f57ea6614eb095ec2c886f", torch_dtype=torch.bfloat16, device_map="auto")



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


