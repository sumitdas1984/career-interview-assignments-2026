"""URL shortener FastAPI service.

Endpoints:

* ``POST /``        — create (or reuse, for idempotency) a short URL.
* ``GET  /{key}``   — 307 redirect to the original URL; 404 if unknown.
* ``GET  /info/{key}`` — return the current visit count for a key.

The base URL prepended to the short key is read from the ``BASE_URL``
environment variable and defaults to ``https://company.com`` to match
the example response in the assignment.
"""

import os
import secrets
import string
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl


BASE_URL = os.environ.get("BASE_URL", "https://company.com").rstrip("/")
CODE_LENGTH = 5
CHARACTERS = string.ascii_letters + string.digits


# long URL -> short key
url_to_key = {}

# short key -> URL details
key_to_url = {}

app = FastAPI(title="URL Shortener")


class URLRequest(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    short_url: str


class URLInfo(BaseModel):
    visits: int


def generate_key():
    """Generate a unique 5-character key."""
    while True:
        key = "".join(
            secrets.choice(CHARACTERS)
            for _ in range(CODE_LENGTH)
        )

        if key not in key_to_url:
            return key
        

@app.post("/", response_model=URLResponse, status_code=201)
def create_short_url(request: URLRequest):
    long_url = str(request.url)

    # Idempotency:
    # If this URL was already shortened, return the same short URL.
    if long_url in url_to_key:
        key = url_to_key[long_url]

        return {
            "short_url": f"{BASE_URL}/{key}"
        }

    key = generate_key()

    key_to_url[key] = {
        "url": long_url,
        "visits": 0
    }

    url_to_key[long_url] = key

    return {
        "short_url": f"{BASE_URL}/{key}"
    }


@app.get("/{key}")
def redirect_to_original_url(key: str):
    if key not in key_to_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    url_data = key_to_url[key]

    # Count successful redirects
    url_data["visits"] += 1

    return RedirectResponse(
        url=url_data["url"],
        status_code=307
    )


@app.get("/info/{key}", response_model=URLInfo)
def get_url_info(key: str):
    if key not in key_to_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return {
        "visits": key_to_url[key]["visits"]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)