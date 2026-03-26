# Weather-Aware Order Tracker

## Overview

This Python project automatically checks the weather for customer orders and flags potential delivery delays. Orders are read from a local JSON file (`orders.json`) and updated in `orders_updated.json`. The project uses **parallel API calls** for efficiency and generates **AI-style apology messages** for delayed orders.

---

## Features

- **Parallel Weather Fetching** – Uses `asyncio` and `aiohttp` to check weather for all cities concurrently.
- **Delay Detection** – Marks orders as `Delayed` if weather is `Rain`, `Snow`, or `Extreme`.
- **AI-Style Apology Messages** – Generates friendly, personalized messages for delayed orders.
- **Error Handling** – Safely logs invalid cities and continues processing without crashing.
- **Logging** – Tracks all activity in `app.log` with INFO, WARNING, and ERROR levels.
- **Secure API Keys** – Stores OpenWeather API key in a `.env` file (not hardcoded).

---

## Getting Started

### Prerequisites

- Python 3.9+
- Libraries: `aiohttp`, `asyncio`, `python-dotenv`, `transformers`, `torch` (optional for local AI message generation)

```bash
pip install aiohttp python-dotenv openai
```
