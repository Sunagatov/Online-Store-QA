import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, empty, none, any_of, is_

from data.text_review import (
    text_review_750_char,
    text_review_1500_char,
    text_review_1499_char,
    text_review_1_char,
    text_review_2_char,
)
from framework.asserts.assert_favorite import assert_added_product_in_favorites
from framework.asserts.common import assert_content_type, assert_review_text
from framework.endpoints.favorite_api import FavoriteAPI
from framework.endpoints.product_api import ProductAPI
from framework.endpoints.review_api import ReviewAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.favorite_methods import extract_random_product_ids
from framework.tools.matcher import is_timestamp_valid
from framework.tools.review_methods import user_has_review


@pytest.mark.critical
@feature("Adding product to favorite ")
class TestReview:
    @pytest.mark.parametrize(
        "text_review,expected_length",
        [
            (text_review_750_char, 750),
            (text_review_1500_char, 1500),
            (text_review_1499_char, 1499),
            (text_review_1_char, 1),
            (text_review_2_char, 2),
        ],
    )
    @title("Test add review to product")
    @description(
        "GIVEN user is registered and has not posted any review on product"
        "WHEN user post review to product"
        "THEN status HTTP CODE = 200 and response body contains text added review, id review and data posted review"
    )
    def test_add_review(self, create_authorized_user, text_review, expected_length):
        with step("Verify review text length for test purpose"):
            assert (
                len(text_review) == expected_length
            ), f"Review text should be exactly {expected_length} characters long"

        with step("Registration of user"):
            user, token = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )

        with step("Getting all products via API"):
            response_get_product = ProductAPI().get_all()

        with step("Verify that user does not have review for product"):
            get_random_product = extract_random_product_ids(
                response_get_product, product_quantity=1
            )
            (product_id,) = get_random_product
            response_get_review = ReviewAPI().get_product_reviews(product_id=product_id)
            assert_that(
                user_has_review(response_get_review, user, text_review=text_review),
                is_(False),
                "user has review",
            )
        with step("Add review to randomly selected product"):
            response_post_review = ReviewAPI().add_product_review(
                token=token, product_id=product_id, text_review=text_review
            )

        with step("Verify that user's review for product posted"):
            response_get_review = ReviewAPI().get_product_reviews(product_id=product_id)
            assert_that(
                user_has_review(response_get_review, user, text_review=text_review),
                is_(True),
                "user has review",
            )
            assert_review_text(response_post_review, text_review)

        with step("Verify content-type"):
            assert_content_type(response_post_review, "application/json")

        with step("Verify data format"):
            actual_timestamp = response_post_review.json().get("createdAt", "")
            time_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z"
            assert_that(
                is_timestamp_valid(actual_timestamp, time_pattern),
                reason=f"Timestamp '{actual_timestamp}' does not match the expected format YYYY-MM-DD HH:MM:SS",
            )
