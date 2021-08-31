import requests
import config


def authenticate(email, code):
    api_url = config.get().get("yeet_api_url")
    url = api_url + "bot/authenticate"
    data = {"email": email, "code": code}
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()


def update_yeet_user(yeet_id, telegram_id):
    api_url = config.get().get("yeet_api_url")
    url = api_url + "users/{0}/telegram".format(yeet_id)
    data = {"telegram_id": telegram_id}
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()


def fetch_subscriptions(yeet_id, type=None):
    api_url = config.get().get("yeet_api_url")
    url = api_url + (
        "users/{0}/subscriptions".format(yeet_id)
        if not type
        else "users/{0}/subscriptions/{1}".format(yeet_id, type)
    )
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_symbols(type):
    api_url = config.get().get("yeet_api_url")
    url = api_url + "symbols/{0}".format(type)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def send_update_mail(email, code):
    api_url = config.get().get("yeet_api_url")
    url = api_url + "bot/update"
    data = {"email": email, "code": code}
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()


def get_yeet_user(id):
    api_url = config.get().get("yeet_api_url")
    url = api_url + "users/{0}".format(id)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
