from hamcrest import assert_that, is_, contains_string
from requests import Response


def assert_status_code(response: Response, expected_status_code: int) -> None:
    """Asserts that the actual status code matches the expected status code.

    Args:
        response: The response object from the API call.
        expected_status_code: The expected status code.
    """
    assert_that(
        response.status_code,
        is_(expected_status_code),
        reason=f"Expected status code {expected_status_code}, found: {response.status_code}",
    )


def assert_content_type(response: Response, expected_content_type: str) -> None:
    """Asserts that the Content-Type of the response matches the expected Content-Type.

    Args:
        response: The response object from the API call.
        expected_content_type: The expected Content-Type string.
    """
    content_type = response.headers.get("Content-Type", "")
    assert_that(
        content_type,
        contains_string(expected_content_type),
        reason=f"Expected Content-Type '{expected_content_type}', found: '{content_type}'",
    )


def assert_response_message(response: Response, expected_message: str) -> None:
    """Asserts that the message in the response body matches the expected message.

    Args:
        response: The response object from the API call.
        expected_message: The expected message string.
    """
    actual_message = response.json().get("message", "")
    assert_that(
        actual_message,
        is_(expected_message),
        reason=f"Expected message '{expected_message}', found: '{actual_message}'",
    )


def assert_message_in_response(response: Response, expected_message: str) -> None:
    """Asserts that the message in the response body matches the expected message.

    Args:
        response: The response object from the API call.
        expected_message: The expected message string.
    """
    actual_message = response.json().get("message", "")
    assert_that(
        actual_message,
        contains_string(expected_message),
        reason=f"Expected response contains '{expected_message}', found: '{actual_message}'",
    )


def assert_review_text(response: Response, expected_review: str) -> None:
    """Asserts that the message in the response body matches the expected message.

    Args:
        response: The response object from the API call.
        expected_review: The expected review string.
    """
    actual_review_text = response.json().get("text", "")
    assert_that(
        actual_review_text,
        is_(expected_review),
        reason=f"Expected text review is '{expected_review}', found: '{actual_review_text}'",
    )


def assert_rating(response: Response, expected_rating: int) -> None:
    """Asserts that the product rating in the response body matches the expected product rating.

    Args:
        response: The response object from the API call.
        expected_rating: The expected product rating.
    """
    actual_product_rating = response.json()["rating"]
    assert_that(
        actual_product_rating,
        is_(expected_rating),
        reason=f"Expected rating product is '{expected_rating}', found: '{actual_product_rating}'",
    )


def assert_user_name_in_response(
    response: Response, expected_first_name: str, expected_last_name: str
) -> None:
    """Asserts that the user's name in the response body matches the expected user's name.

    Args:
        response: The response object from the API call.
        expected_first_name: User's first name.
        expected_last_name: User's last name.
    """
    actual_first_name = response.json()["userName"]
    actual_last_name = response.json()["userLastName"]
    assert_that(
        actual_first_name,
        is_(expected_first_name),
        reason=f"Expected first name is '{expected_first_name}', found: '{actual_first_name}'",
    )
    assert_that(
        actual_last_name,
        is_(expected_last_name),
        reason=f"Expected last name is '{expected_last_name}', found: '{actual_last_name}'",
    )


def assert_key_and_value_in_response(response: Response, *key: str) -> None:
    """Asserts that the id review in the response body

    Args:
        key: specific key in the response body
        response: The response object from the API call.

    """

    data = response.json()
    assert key in data, f"Key '{key}' not found in response"

    value = data[key]
    assert_that(value is not None, f"Value for key '{key}' is None.")
    assert_that(value != "", f"Value for key '{key}' is empty.")
