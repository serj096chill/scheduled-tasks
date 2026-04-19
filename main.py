import os
import json
import requests

if "PYTHONANYWHERE_DOMAIN" in os.environ:
    proxy_url = "http://proxy.server:3128"
    os.environ["http_proxy"] = proxy_url
    os.environ["https_proxy"] = proxy_url

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

weather_params = {
    "lat": 33.893791,
    "lon": 35.501778,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

# --- Send Notification ---
if will_rain:
    # This is the Telegram API URL for sending messages
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    telegram_params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "It's going to rain today. Bring an umbrella! ☔️"
    }

    # Sending the request to Telegram
    tel_response = requests.get(telegram_url, params=telegram_params)
    tel_response.raise_for_status()
    print("Telegram message sent successfully!")
else:
    print("No rain forecast for the next 12 hours.")
