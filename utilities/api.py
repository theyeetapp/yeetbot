import requests
import config


def authenticate(email, code):
    api_url = config.get().get("yeet_api_url")
    url = api_url + "bot/authenticate"
    data = {"email": email, "code": code}
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()


def count_subscriptions(id):
    api_url = config.get().get("yeet_api_url")
    url = api_url + "users/{0}/subscriptions/count"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def update_yeet_user(yeet_id, telegram_id):
    api_url = config.get().get("yeet_api_url")
    url = api_url + "users/{0}/telegram/update".format(yeet_id)
    data = {"telegram_id": telegram_id}
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()
