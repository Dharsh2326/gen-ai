import gradio as gr
import requests
from bs4 import BeautifulSoup

# Local dictionary of known acronyms & abbreviations
local_dict = {
    "NASA": "National Aeronautics and Space Administration",
    "AI": "Artificial Intelligence",
    "ML": "Machine Learning",
    "CPU": "Central Processing Unit",
    "GPU": "Graphics Processing Unit",
    "HTML": "HyperText Markup Language",
    "HTTP": "HyperText Transfer Protocol",
    "URL": "Uniform Resource Locator",
    "SQL": "Structured Query Language",
    "API": "Application Programming Interface",
    "OOPS": "Object Oriented Programming System"
}

# Function to get Wikipedia summary if not in local dict
def get_from_wikipedia(term):
    search_url = f"https://en.wikipedia.org/wiki/{term.replace(' ', '_')}"
    try:
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paras = soup.find_all('p')
        for para in paras:
            text = para.text.strip()
            if text and not text.lower().startswith("coordinates"):
                return text
        return "Wikipedia page found but no readable summary."
    except:
        return "Could not fetch data from Wikipedia."

# Main function
def expand(term):
    term = term.strip().upper()
    if term in local_dict:
        return f"Local Match: {local_dict[term]}"
    else:
        wiki_summary = get_from_wikipedia(term)
        return f"From Wikipedia:\n{wiki_summary}"

# Gradio UI
gr.Interface(
    fn=expand,
    inputs=gr.Textbox(label="Enter Acronym or Abbreviation"),
    outputs=gr.Textbox(label="Expanded Form / Info"),
    title="Acronym & Abbreviation Expander",
    description="Enter common acronyms like 'AI', 'OOPS', etc. If not found locally, it fetches from Wikipedia."
).launch()
