# ai_explainer.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from openai import RateLimitError

def explain_project(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant explaining data science projects."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content

    except RateLimitError:
        return "⚠️ AI service is temporarily unavailable. Please try again later."
    
