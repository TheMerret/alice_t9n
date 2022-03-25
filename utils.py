import os

import requests

URL = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
API_KEY = os.getenv("API_KEY")
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
}


def translate(text, lang_from="ru", lang_to="en"):
    params = {
        "langpair": f"{lang_from}|{lang_to}",
        "q": text,
    }

    resp = requests.get(URL, params=params, headers=HEADERS)
    resp_json = resp.json()
    status_code = resp_json["responseStatus"]
    status_code = 200 if status_code is None else int(status_code)
    resp.status_code = status_code
    reason = resp_json["responseDetails"]
    resp.reason = reason
    resp.raise_for_status()
    response_data = resp_json["responseData"]
    translation = response_data["translatedText"]
    return translation