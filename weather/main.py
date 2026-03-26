import asyncio
import aiohttp
import json
import os
import logging
from dotenv import load_dotenv
from model import ai_generate_apology

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),   # file log
        logging.StreamHandler()           # console log
    ]
)

# Here i use below commeted List for testing purpose
# DELAY_WEATHER = ["Rain", "Snow", "Extreme", "Clouds"] for testing purpose

DELAY_WEATHER = ["Rain", "Snow", "Extreme"]

def generate_apology(customer, city, weather, ai_apology=False):
    if ai_apology:
        return ai_generate_apology(customer,city,weather)

    return f"Hi {customer}, your order to {city} is delayed due to {weather.lower()}. We appreciate your patience!"

async def get_weather(session, city):
    try:
        params = {"q": city, "appid": API_KEY}

        async with session.get(BASE_URL, params=params) as response:
            if response.status != 200:
                error_text = await response.text()
                logging.error(f"Error for {city}: {error_text}")
                return {"city": city, "error": True}

            data = await response.json()
            weather_main = data["weather"][0]["main"]

            logging.info(f"Weather for {city}: {weather_main}")

            return {
                "city": city,
                "weather": weather_main
            }

    except Exception as e:
        logging.error(f"Exception for {city}: {str(e)}")
        return {"city": city, "error": True}

async def process_orders():
    logging.info("Starting order processing...")

    with open("D:\Projects\Yellow AI Assignment\weather\orders.json", "r") as file:
        orders = json.load(file)

    async with aiohttp.ClientSession() as session:
        tasks = [get_weather(session, order["city"]) for order in orders]

        results = await asyncio.gather(*tasks)

    for i, order in enumerate(orders):
        result = results[i]

        if result.get("error"):
            logging.warning(f"Skipping invalid city: {order['city']}")
            continue

        if result["weather"] in DELAY_WEATHER:
            order["status"] = "Delayed"

            message = generate_apology(
                order["customer"],
                order["city"],
                result["weather"]
            )

            logging.info(f"DELAYED ORDER: {order['order_id']}")
            logging.info(f"Message: {message}")

    with open("orders_updated.json", "w") as file:
        json.dump(orders, file, indent=2)

    logging.info("Processing complete. Output saved to orders_updated.json")

if __name__ == "__main__":
    asyncio.run(process_orders())