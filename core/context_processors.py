def current_user_context(request):

    return {
        "current_user":
            getattr(
                request,
                "current_user",
                None
            ),

        "user_role":
            getattr(
                request,
                "user_role",
                None
            ),

        "username":
            getattr(
                request,
                "username",
                None
            ),
    }

