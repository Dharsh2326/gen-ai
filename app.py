import requests
from bs4 import BeautifulSoup
import gradio as gr

def get_answer(topic):
    search_url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paras = soup.find_all('p')
    for para in paras:
        if para.text.strip():
            return f"Q: What is {topic}?\nA: {para.text.strip()}"
    return "Sorry, no info found."

gr.Interface(fn=get_answer, inputs="text", outputs="text",
             title="Interview QA Generator from Wiki").launch()
