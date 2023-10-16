# import gradio as gr

# def echo(message, history):
#     return message


import torch
from transformers import pipeline
pipe = pipeline("text-generation", model="/data/huggingface/cache/models--HuggingFaceH4--starchat-beta/snapshots/b1bcda690655777373f57ea6614eb095ec2c886f", torch_dtype=torch.bfloat16, device_map="cpu")



# demo = gr.ChatInterface(fn=echo, examples=["hello", "hola", "merhaba"], title="Echo Bot")

#demo.queue().launch(root_path="/test")

from fastapi import FastAPI
import gradio as gr
import uvicorn
import os

path = os.environ["BASE_URL"]

examples = [
    "How can I write a Python function to generate the nth Fibonacci number?",
    "How do I get the current date using shell commands? Explain how it works.",
    "What's the meaning of life?",
    "Write a function in Javascript to reverse words in a given string.",
    "Give the following data {'Name':['Tom', 'Brad', 'Kyle', 'Jerry'], 'Age':[20, 21, 19, 18], 'Height' : [6.1, 5.9, 6.0, 6.1]}. Can you plot one graph with two subplots as columns. The first is a bar graph showing the height of each person. The second is a bargraph showing the age of each person? Draw the graph in seaborn talk mode.",
    "Create a regex to extract dates from logs",
    "How to decode JSON into a typescript object",
    "Write a list into a jsonlines file and save locally",
]

def echo(message, history):
    prompt_template = "<|system|>\n<|end|>\n<|user|>\n{query}<|end|>\n<|assistant|>"
    prompt = prompt_template.format(query=message)
    outputs = pipe(prompt, max_new_tokens=356, do_sample=True, temperature=0.2, top_k=50, top_p=0.95, eos_token_id=49155)
    return str(outputs[0]["generated_text"].split("<|assistant|>")[1])


print("base url is ",path)

app = FastAPI()

g_app = gr.ChatInterface(fn=echo, examples=examples, title="StarChat Bot")
g_app.queue(concurrency_count=3)
#g_app = gr.ChatInterface(fn=echo, examples=examples, title="Echo Bot")
app = gr.mount_gradio_app(app, g_app, path=path)
uvicorn.run(app,host="0.0.0.0",port=7860)


