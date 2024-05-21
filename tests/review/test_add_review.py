import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, is_, equal_to

from data.text_review import parameterize_text_review_positive
from framework.asserts.common import assert_content_type
from framework.endpoints.product_api import ProductAPI
from framework.endpoints.review_api import ReviewAPI
from framework.tools.favorite_methods import extract_random_product_ids
from framework.tools.matcher import is_timestamp_valid
from framework.tools.review_methods import (
    verify_user_review,
    verify_user_review_in_all_reviews,
    verify_user_review_by_user_name_in_all_product_reviews,
)


@pytest.mark.critical
@feature("Adding review and rating to product")
class TestReviewWithRating:
    @pytest.mark.parametrize(
        "text_review,expected_length,rating",
        parameterize_text_review_positive,
    )
    @title("Test add review  and rating to product")
    @description(
        "GIVEN user is registered and has not posted any review on product"
        "WHEN user post review and rating to product"
        "THEN status HTTP CODE = 200 and response body contains user's name, text of review, rating, id's review and data posted review"
    )
    def test_add_review(
        self, create_authorized_user, text_review, expected_length, rating
    ):
        with step("Verify review text length for test purpose"):

            if expected_length is not None:
                assert (
                    len(text_review) == expected_length
                ), f"Review text should be exactly {expected_length} characters long"
            else:
                assert (
                    len(text_review) > 0
                ), "Review text should not be empty when no expected length is specified"

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
            response_get_review = ReviewAPI().get_all_product_reviews(
                product_id=product_id
            )
            assert_that(
                verify_user_review_by_user_name_in_all_product_reviews(
                    response_get_review, user
                ),
                is_(False),
                "user has review",
            )

        with step("Add review to randomly selected product"):
            response_post_review = ReviewAPI().add_product_review(
                token=token,
                product_id=product_id,
                text_review=text_review,
                rating=rating,
            )
        with step(
            "Verify first name, last name, text review, rating and productReviewId in response body after post review"
        ):
            verify_user_review(
                response_body=response_post_review,
                user_info=user,
                expected_text_review=text_review,
                expected_rating=rating,
                key="productReviewId",
            )

        with step("Verify content-type"):
            assert_content_type(response_post_review, "application/json")

        with step("Verify data format"):
            actual_timestamp = response_post_review.json().get("createdAt", "")
            time_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{2,6}Z"
            assert_that(
                is_timestamp_valid(actual_timestamp, time_pattern),
                reason=f"Timestamp '{actual_timestamp}' does not match the expected format YYYY-MM-DD HH:MM:SS",
            )

        with step(
            "Verify that the user's review is successfully added to the product by retrieving all product reviews"
        ):
            response_get_all_review = ReviewAPI().get_all_product_reviews(
                product_id=product_id
            )

            result, message = verify_user_review_in_all_reviews(
                response_get_all_review, user, text_review=text_review, rating=rating
            )
            assert_that(result, is_(equal_to(True)), reason=message)

        with step("Verify user review by getting user's review through API"):
            response_get_user_review = ReviewAPI().get_user_product_review(
                token=token, product_id=product_id
            )
            verify_user_review(
                response_body=response_get_user_review,
                user_info=user,
                expected_text_review=text_review,
                expected_rating=rating,
                key="productReviewId",
            )
