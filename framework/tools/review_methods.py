import json
import random
from datetime import datetime
from typing import Dict

from faker import Faker
from hamcrest import (
    assert_that,
    is_,
    equal_to,
    greater_than_or_equal_to,
    less_than_or_equal_to,
)
from requests import Response
from typing_extensions import Any

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
        and review.get("userLastname") == user_info.get("lastName")
    ]

    if not user_reviews:
        return (
            False,
            f"No reviews found for user {user_info.get('firstName')} {user_info.get('lastName')}.",
        )

    for review in user_reviews:
        text_matches = review.get("text") == text_review
        rating_matches = review.get("productRating") == rating

        if text_matches and rating_matches:
            return True, "Review matches the given user and criteria."

        mismatches = []
        if not text_matches:
            mismatches.append(
                f"Review text mismatch: expected '{text_review}', found '{review.get('text')}'"
            )
        if not rating_matches:
            mismatches.append(
                f"Rating mismatch: expected {rating}, found {review.get('productRating')}"
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

    actual_product_rating = data["productRating"]
    actual_first_name = data["userName"]
    actual_last_name = data["userLastname"]
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


def extract_data_from_random_review(response: Response) -> Any:
    """Extracts item review ID, likes count and dislike count of a randomly selected item from the JSON response.

    Args:
        response: The JSON response containing item details.

    """
    try:
        json_response = response.json()
    except ValueError:
        return {"error": "Invalid JSON response"}

    items = json_response.get("reviewsWithRatings", [])

    if not items:
        return None
    else:
        random_item = random.choice(items)
        if random_item:
            review_id = random_item.get("productReviewId", "")
            likes_count = random_item.get("likesCount", 0)
            dislikes_count = random_item.get("dislikesCount", 0)
            return {
                "productReviewId": review_id,
                "likesCount": likes_count,
                "dislikesCount": dislikes_count,
            }
        else:
            return None


def extract_random_product_info(response: Response, product_quantity: int) -> list:
    """Extract random product info from list of products.

    Selects a random sample of products from the response based on the given quantity.
    Returns a list of the values for those randomly selected products.

    Args:
        response: Response data from API request containing products
        product_quantity: Number of random products to select

    Raises:
        ValueError: If requested quantity exceeds products available
    """
    products = response.json()["products"]
    if product_quantity > len(products):
        raise ValueError("Requested amount exceeds the number of available products")

    selected_products = random.sample(products, product_quantity)
    return [
        {
            "id": product.get("id"),
            "averageRating": product.get("averageRating"),
            "reviewsCount": product.get("reviewsCount"),
        }
        for product in selected_products
    ]


def extract_product_info_from_list_of_products(
    response: Response, product_id: str
) -> list:
    """Extract random product info from the API response.

    Extracts product info from the response based on the given product ID.
    Returns a list of the values for that product.

    Args:
        response: Response data from API request containing products
        product_id: product id

    Raises:
        ValueError: If requested quantity exceeds products available
    """
    products = response.json()["products"]

    return [
        {
            "id": product.get("id"),
            "averageRating": product.get("averageRating"),
            "reviewsCount": product.get("reviewsCount"),
        }
        for product in products
        if product.get("id") == product_id
    ]


def assert_page_number_in_reviews_body(response, page_number):
    """Verify if the page number in the response body is equal to the expected page number.

    Args:
         response: The response object from the API call.
         page_number: The expected page number.

    """
    try:
        response_data = response.json()
    except ValueError as e:
        raise AssertionError(f"Response is not in valid JSON format: {e}") from e

    assert_that(
        response_data.get("page", 0),
        is_(equal_to(page_number)),
        reason=f"Expected page number is '{page_number}', found: '{response.json().get('page', 0)}'",
    )


def assert_size_reviews_per_page(response, reviews_size_per_page):
    """Verify if the page number in the response body is equal to the expected page number.

    Args:
         response: The response object from the API call.
         reviews_size_per_page: The expected size of reviews per page.

    """
    try:
        response_data = response.json()
    except ValueError as e:
        raise AssertionError(f"Response is not in valid JSON format: {e}") from e

    actual_size = len(response_data.get("reviewsWithRatings", []))

    assert_that(
        actual_size,
        is_(equal_to(reviews_size_per_page)),
        reason=f"Expected number of reviews per page is '{reviews_size_per_page}', found: '{actual_size}'",
    )


def assert_total_elements_reviews(response, total_elements):
    """Verify if the page number in the response body is equal to the expected page number.

    Args:
         total_elements: The expected total number of reviews.
         response: The response object from the API call.

    """
    try:
        response_data = response.json()
    except ValueError as e:
        raise AssertionError(f"Response is not in valid JSON format: {e}") from e
    # total_elements = response_data.get("totalElements", 0)

    actual_size = len(response_data.get("reviewsWithRatings", []))

    assert_that(
        actual_size,
        is_(equal_to(total_elements)),
        reason=f"Expected number of reviews per page is '{total_elements}', found: '{actual_size}'",
    )


def assert_reviews_sorted_by_createdAt_in_descending_order(response):
    """Verify if the reviews are sorted by createdAt in descending order.

    Args:
         response: The response object from the API call.

    """
    try:
        response_data = response.json()
    except ValueError as e:
        raise AssertionError(f"Response is not in valid JSON format: {e}") from e

    reviews = response_data.get("reviewsWithRatings", [])

    sorted_reviews = sorted(
        reviews,
        key=lambda x: datetime.strptime(x["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"),
        reverse=True,
    )
    assert_that(
        reviews,
        equal_to(sorted_reviews),
        "Reviews are not sorted by createdAt in descending order",
    )


def assert_reviews_sorted_by_createdAt_in_ascending_order(response):
    """Verify if the reviews are sorted by createdAt in ascending order.

    Args:
         response: The response object from the API call.
    """
    try:
        response_data = response.json()
    except ValueError as e:
        raise AssertionError(f"Response is not in valid JSON format: {e}") from e
    reviews = response_data.get("reviewsWithRatings", [])

    sorted_reviews = sorted(
        reviews,
        key=lambda x: datetime.strptime(x["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"),
    )
    assert_that(
        reviews,
        equal_to(sorted_reviews),
        "Reviews are not sorted by createdAt in ascending order",
    )


def assert_reviews_sorted_asc(response):
    """Verify if the reviews are sorted by createdAt in ascending order.

    Args:
         response: The response object from the API call.
    """
    try:
        response_data = response.json()
    except ValueError as e:
        raise AssertionError(f"Response is not in valid JSON format: {e}") from e
    reviews = response_data.get("reviewsWithRatings", [])

    for i in range(len(reviews) - 1):
        current_date = datetime.strptime(
            reviews[i]["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        next_date = datetime.strptime(
            reviews[i + 1]["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert_that(
            current_date,
            less_than_or_equal_to(next_date),
            "Reviews are not sorted by createdAt in ascending order",
        )


def assert_reviews_sorted_desc(response):
    """Verify if the reviews are sorted by createdAt in descending order.

    Args:
         response: The response object from the API call.
    """
    try:
        response_data = response.json()
    except ValueError as e:
        raise AssertionError(f"Response is not in valid JSON format: {e}") from e
    reviews = response_data.get("reviewsWithRatings", [])

    for i in range(len(reviews) - 1):
        current_date = datetime.strptime(
            reviews[i]["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        next_date = datetime.strptime(
            reviews[i + 1]["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert_that(
            current_date,
            greater_than_or_equal_to(next_date),
            "Reviews are not sorted by createdAt in descending order",
        )
