
import requests

from django.conf import settings


def api_get(endpoint, token=None):

    headers = {}

    if token:
        headers["Authorization"] = (
            f"Bearer {token}"
        )

    return requests.get(
        f"{settings.BACKEND_API_URL}/{endpoint}",
        headers=headers,
        timeout=90
    )


def api_post(endpoint, token, data):

    return requests.post(
        f"{settings.BACKEND_API_URL}/{endpoint}",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=90
    )

def api_patch(
    endpoint,
    token,
    data=None
):

    return requests.patch(
        f"{settings.BACKEND_API_URL}/{endpoint}",
        json=data,
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        timeout=90
    )

# services.py

def api_post_file(
    endpoint,
    token,
    data,
    files
):

    return requests.post(
        f"{settings.BACKEND_API_URL}/{endpoint}",
        data=data,
        files=files,
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        timeout=90
    )

def api_put_file(
    endpoint,
    token,
    data,
    files
):

    return requests.put(
        f"{settings.BACKEND_API_URL}/{endpoint}",
        data=data,
        files=files,
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        timeout=90
    )

import time
import requests

def login_user(username, password):

    wake_url = settings.BACKEND_API_URL
    login_url = (
        f"{settings.BACKEND_API_URL}/token/"
    )

    print("WAKE URL:", wake_url)

    try:

        requests.get(
            wake_url,
            timeout=30
        )

        print(
            "Wake-up request sent."
        )

        time.sleep(8)

    except Exception as e:

        print(
            "Wake-up failed:",
            str(e)
        )

    print(
        "LOGIN URL:",
        login_url
    )

    last_response = None

    for attempt in range(3):

        try:

            print(
                f"Login attempt {attempt + 1}/3"
            )

            response = requests.post(
                login_url,
                json={
                    "username": username,
                    "password": password,
                },
                timeout=90
            )

            print(
                "STATUS:",
                response.status_code
            )

            if response.status_code not in (
                502,
                503,
                504
            ):
                return response

            last_response = response

        except requests.RequestException as e:

            print(
                "REQUEST ERROR:",
                str(e)
            )

        if attempt < 2:

            print(
                "Waiting for backend wake-up..."
            )

            time.sleep(15)

    return last_response

def get_current_user(token):

    response = requests.get(
        f"{settings.BACKEND_API_URL}/current-user/",
        headers={
            "Authorization":
                f"Bearer {token}"
        },
        timeout=90
    )
    

    return response
def api_put(
    endpoint,
    token,
    data
):

    return requests.put(
        f"{settings.BACKEND_API_URL}/{endpoint}",
        json=data,
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        timeout=90
    )

def api_delete(
    endpoint,
    token
):

    return requests.delete(
        f"{settings.BACKEND_API_URL}/{endpoint}",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        timeout=90
    )
