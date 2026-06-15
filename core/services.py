
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
def login_user(username, password):

    response = requests.post(
        f"{settings.BACKEND_API_URL}/token/",
        json={
            "username": username,
            "password": password,
        },
        timeout=90
    )

    return response

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
