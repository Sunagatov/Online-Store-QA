import json


from faker import Faker
from hamcrest import assert_that, is_
from requests import Response

fake = Faker()


def generate_fake_review():
    review_body = fake.text(max_nb_chars=1505)

    return {"body": review_body}


text = generate_fake_review()


def verify_user_review_by_user_name_in_all_product_reviews(
    response_body: Response, user_info: dict
) -> bool:
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


def verify_user_review_in_all_reviews(
    response_body: Response, user_info: dict, text_review: str, rating: int
):
    """
    Checks if a given user has posted a specific text review and product rating in the response body.

    The function first ensures the response body is valid JSON and contains the expected data structure.
    It then iterates through the reviews in the response and checks if there is a review matching the given user info and text.

    Args:
       response_body: The response body to check for reviews.
       rating: The rating of the review to check for.
       user_info: A dict containing firstName and lastName keys for the user.
       text_review: The text of the review to check for.

    Returns:
       bool: True if the user has posted the given text review and product rating, False otherwise."""

    try:
        data = response_body.json()
    except json.JSONDecodeError as e:
        raise ValueError("The response body is not valid JSON.") from e

    if "reviewsWithRatings" not in data:
        raise ValueError("Expected data structure is missing from the response.")

    user_reviews = [
        review
        for review in data.get("reviewsWithRatings", [])
        if review.get("userName") == user_info.get("firstName")
        and review.get("userLastName") == user_info.get("lastName")
    ]

    if not user_reviews:
        return (
            False,
            f"No reviews found for user {user_info.get('firstName')} {user_info.get('lastName')}.",
        )

    for review in user_reviews:
        text_matches = review.get("text") == text_review
        rating_matches = review.get("rating") == rating

        if text_matches and rating_matches:
            return True, "Review matches the given user and criteria."

        mismatches = []
        if not text_matches:
            mismatches.append(
                f"Review text mismatch: expected '{text_review}', found '{review.get('text')}'"
            )
        if not rating_matches:
            mismatches.append(
                f"Rating mismatch: expected {rating}, found {review.get('rating')}"
            )

        return False, " | ".join(mismatches)

    return (
        False,
        f"User {user_info.get('firstName')} {user_info.get('lastName')} has no review matching the given criteria.",
    )


def verify_user_review(
    response_body: Response,
    user_info: dict,
    expected_text_review: str,
    expected_rating: int,
    key: str,
):
    """
    Checks if a given user has posted a specific text review and product rating in the response body.

    The function first ensures the response body is valid JSON and contains the expected data structure.
    It then iterates through the reviews in the response and checks if there is a review matching the given user info and text.

    Args:
       key: specific key in the response body
       response_body: The response body to check for reviews.
       expected_rating: The rating of the review to check for.
       user_info: A dict containing firstName and lastName keys for the user.
       expected_text_review: The text of the review to check for.

    Returns:
       bool: True if the user has posted the given text review and product rating, False otherwise."""

    try:
        data = response_body.json()
    except json.JSONDecodeError as e:
        raise ValueError("The response body is not valid JSON.") from e

    actual_product_rating = data["rating"]
    actual_first_name = data["userName"]
    actual_last_name = data["userLastName"]
    actual_text_review = data["text"]
    expected_user_first_name, expected_user_last_name = (
        user_info["firstName"],
        user_info["lastName"],
    )

    assert_that(
        actual_product_rating,
        is_(expected_rating),
        reason=f"Expected rating product is '{expected_rating}', found: '{actual_product_rating}'",
    )
    assert_that(
        actual_first_name,
        is_(expected_user_first_name),
        reason=f"Expected first name is '{expected_user_first_name}', found: '{actual_first_name}'",
    )
    assert_that(
        actual_last_name,
        is_(expected_user_last_name),
        reason=f"Expected last name is '{expected_user_last_name}', found: '{actual_last_name}'",
    )
    assert_that(key in data, f"Key '{key}' not found in response")
    assert_that(
        actual_text_review,
        is_(expected_text_review),
        reason=f"Expected text review is '{expected_text_review}', found: '{actual_text_review}'",
    )

    value = data[key]
    assert_that(value is not None, f"Value for key '{key}' is None.")
    assert_that(value != "", f"Value for key '{key}' is empty.")
