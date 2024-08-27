import httpx
from app.config import settings


SPELLER_URL = settings.speller_url
LANGUAGES = settings.languages


def verify_with_speller(text: str, available_exception):
    data = {
        "text": text,
        "lang": LANGUAGES,
    }

    response = httpx.post(url=SPELLER_URL, data=data)
    if not response.status_code == 200:
        raise available_exception

    return response.json()
