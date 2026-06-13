from django.shortcuts import redirect

from .services import (
    get_current_user
)


class AuthenticationMiddleware:

    EXEMPT_URLS = [

        "/login/",
        "/logout/",

        "/static/",
        "/media/",

        "/favicon.ico",
    ]

    def __init__(
        self,
        get_response
    ):

        self.get_response = (
            get_response
        )

    def __call__(
        self,
        request
    ):

        token = request.session.get(
            "access_token"
        )

        is_exempt = any(
            request.path.startswith(
                url
            )
            for url in self.EXEMPT_URLS
        )

        if (
            not token
            and not is_exempt
        ):

            return redirect(
                "login"
            )

        request.access_token = token

        request.current_user = None

        request.user_role = None

        request.username = None

        if token:

            response = get_current_user(
                token
            )

            if response.status_code == 200:

                user = response.json()

                request.current_user = (
                    user
                )

                request.user_role = (
                    user["role"]
                )

                request.username = (
                    user["username"]
                )

            else:

                request.session.flush()

                return redirect(
                    "login"
                )

        return self.get_response(
            request
        )