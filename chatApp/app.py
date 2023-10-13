import streamlit as st
import torch
from transformers import pipeline

#pipe = pipeline("text-generation", model="/data/huggingface/cache/models--HuggingFaceH4--starchat-beta/snapshots/b1bcda690655777373f57ea6614eb095ec2c886f", torch_dtype=torch.bfloat16, device_map="auto")


st.title("StarCoder")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type Something?"):

    #prompt_template = "<|system|>\n<|end|>\n<|user|>\n{query}<|end|>\n<|assistant|>"
    #prompt = prompt_template.format(query=prompt)
    # We use a special <|end|> token with ID 49155 to denote ends of a turn
    #outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.2, top_k=50, top_p=0.95, eos_token_id=49155)
    #preds = str(outputs[0]["generated_text"].split("<|assistant|>")[1])

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})