import json

from faker import Faker
from requests import Response

fake = Faker()


def generate_fake_review():
    review_body = fake.text(max_nb_chars=1505)

    return {"body": review_body}


text = generate_fake_review()


def verify_user_review_by_user_name(response_body: Response, user_info: dict) -> bool:
    """
    Checks if a given user has posted a specific text review in the response body.

    The function first ensures the response body is valid JSON and contains the expected data structure.
    It then iterates through the reviews in the response and checks if there is a review matching the given user info and text.

    Args:
       response_body: The response body to check for reviews.
       user_info: A dict containing firstName and lastName keys for the user.


    Returns:
       bool: True if the user has posted the given text review, False otherwise."""

    try:
        data = response_body.json()
    except json.JSONDecodeError as e:
        raise ValueError("The response body is not valid JSON.") from e

    if "reviewsWithRatings" not in data:
        raise ValueError("Expected data structure is missing from the response.")

    return any(
        review.get("userName") == user_info.get("firstName")
        and review.get("userLastName") == user_info.get("lastName")
        for review in data["reviewsWithRatings"]
    )


def verify_user_review_by_user_name_and_text(
    response_body: Response, user_info: dict, text_review: str
) -> bool:
    """
    Checks if a given user has posted a specific text review in the response body.

    The function first ensures the response body is valid JSON and contains the expected data structure.
    It then iterates through the reviews in the response and checks if there is a review matching the given user info and text.

    Args:
       response_body: The response body to check for reviews.
       user_info: A dict containing firstName and lastName keys for the user.
       text_review: The text of the review to check for.

    Returns:
       bool: True if the user has posted the given text review, False otherwise."""

    try:
        data = response_body.json()
    except json.JSONDecodeError as e:
        raise ValueError("The response body is not valid JSON.") from e

    if "reviewsWithRatings" not in data:
        raise ValueError("Expected data structure is missing from the response.")

    return any(
        review.get("userName") == user_info.get("firstName")
        and review.get("userLastName") == user_info.get("lastName")
        and review.get("reviewText") == text_review
        for review in data["reviewsWithRatings"]
    )
