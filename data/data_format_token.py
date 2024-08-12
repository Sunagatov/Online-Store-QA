# data for format token = code, expected_status_code, expected_message_part
incorrect_format_token = [
    (" ", 400, "ErrorMessage: Token cannot be empty"),
    (
        "testtest",
        400,
        "Incorrect token format, token must be #########",
    ),
    ("1234567890", 400, "Incorrect token format, token must be #########"),
    ("1234567", 400, "Incorrect token format, token must be #########"),
    ("12345678", 400, "Incorrect token format, token must be #########"),
    ("$*@!_+_*&%", 400, "Incorrect token format, token must be #########"),
    ("356-234-123", 400, "Incorrect token format, token must be #########"),
]
