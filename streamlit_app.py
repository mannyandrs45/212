import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="🧱 GHG Assistant")
st.title('🧱 GHG Assistant')

# Fetch API key from environment variable
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Your fine-tuned Mistral model ID
MISTRAL_MODEL_ID = "ft:ministral-3b-latest:2bdc962c:20250302:976e6230"

# Function to send request to Mistral API
def generate_response(input_text):
    if not MISTRAL_API_KEY:
        st.error("API key is missing! Please check your `.env` file.", icon="⚠")
        return

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MISTRAL_MODEL_ID,  # Your fine-tuned model
        "messages": [{"role": "user", "content": input_text}],
        "temperature": 0.7
    }

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",  # Mistral API endpoint
        headers=headers,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        output = response.json()
        st.info(output["choices"][0]["message"]["content"])
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

# Form for user input
with st.form('my_form'):
    text = st.text_area('Enter text:', 'Hi! How may I assist you today?')
    submitted = st.form_submit_button('Submit')

    if submitted:
        generate_response(text)
