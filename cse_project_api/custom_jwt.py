def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "fullName": user.get_full_name()
    }
