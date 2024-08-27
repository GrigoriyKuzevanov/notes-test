import httpx
from httpx import HTTPStatusError

SPELLER_URL = "https://speller.yandex.net/services/spellservice.json/checkText"
LANGUAGES = "ru,en"


def verify_with_speller(text: str, available_exception):
    data = {
        "text": text,
        "lang": LANGUAGES,
    }

    response = httpx.post(url=SPELLER_URL, data=data)
    if not response.status_code == 200:
        raise available_exception

    return response.json()
