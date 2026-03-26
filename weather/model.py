import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def ai_generate_apology(customer, city, weather):
    prompt = (
        f"Write a friendly, professional, one-line message for {customer} "
        f"whose order to {city} is delayed due to {weather}. "
        f"Make it polite and empathetic."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )

    return response.choices[0].message.content.strip()