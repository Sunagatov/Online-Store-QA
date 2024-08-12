import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, is_, equal_to

from data.error_message_token import (
    token_is_absent,
    token_is_expired,
    token_is_blacklisted,
)
from data.text_review import (
    parameterize_text_review_positive,
    parameterize_text_review_invalid_text,
    parameterize_text_review_with_invalid_rating_and_empty_text,
    text_review_750_char,
    text_review_with_emojy,
)
from framework.asserts.common import (
    assert_content_type,
    assert_response_message,
    assert_message_in_response,
)
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.product_api import ProductAPI
from framework.endpoints.review_api import ReviewAPI
from framework.tools.favorite_methods import extract_random_product_ids
from framework.tools.generators import generate_jwt_token
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

    @pytest.mark.xfail(reason="Bug: https://github.com/Sunagatov/Iced-Latte/issues/309")
    @pytest.mark.parametrize(
        "text_review,rating, expected_status_code, expected_error_message",
        parameterize_text_review_with_invalid_rating_and_empty_text,
    )
    @title("Test add review  with empty rating or text review")
    @description(
        "GIVEN user is registered and has not posted any review on product"
        "WHEN user post review with empty rating or text review or both empty fields"
        "THEN status HTTP CODE = 400 and response body contains error message"
    )
    def test_add_review_with_invalid_rating_and_text_review(
        self,
        create_authorized_user,
        text_review,
        rating,
        expected_status_code,
        expected_error_message,
    ):

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

        with step(
            "Add review with empty rating or text review or both empty fields to randomly selected product"
        ):
            response_post_review = ReviewAPI().add_product_review(
                token=token,
                product_id=product_id,
                text_review=text_review,
                rating=rating,
                expected_status_code=expected_status_code,
            )

        with step("Verify error message"):
            assert_message_in_response(response_post_review, expected_error_message)

        with step(
            "Verify that the user's review is not successfully added to the product by retrieving all product reviews"
        ):
            response_get_all_review = ReviewAPI().get_all_product_reviews(
                product_id=product_id
            )

            result, message = verify_user_review_in_all_reviews(
                response_get_all_review, user, text_review=text_review, rating=rating
            )
            assert_that(result, is_(equal_to(False)), reason=message)

        with step(
            "Verify user review does not created via getting user's review through API"
        ):
            response_get_user_review = ReviewAPI().get_user_product_review(
                token=token, product_id=product_id
            )
            product_review_id = response_get_user_review.json().get(
                "productReviewId", ""
            )
            assert_that(
                product_review_id, is_(equal_to(None)), reason="review is created"
            )

    @title("Test add review with empty product id")
    @description(
        "GIVEN user is registered and has not posted any review on product"
        "WHEN user post review with empty product id"
        "THEN status HTTP CODE = 400 and response body contains error message"
    )
    def test_add_review_with_empty_product_id(self, create_authorized_user):

        with step("Registration of user"):
            user, token = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )

        with step("Add review with empty product id"):
            text_review = text_review_750_char
            product_id = ""
            rating = 5
            expected_status_code = 400
            response_post_review = ReviewAPI().add_product_review(
                token=token,
                product_id=product_id,
                text_review=text_review,
                rating=rating,
                expected_status_code=expected_status_code,
            )

        with step(
            "Verify that the user's review is not successfully added to the product by retrieving all product reviews"
        ):
            response_get_all_review = ReviewAPI().get_all_product_reviews(
                product_id=product_id, expected_status_code=400
            )

        with step(
            "Verify user review does not created via getting user's review through API"
        ):
            response_get_user_review = ReviewAPI().get_user_product_review(
                token=token, product_id=product_id, expected_status_code=400
            )

    @pytest.mark.xfail(
        reason="https://github.com/Sunagatov/Iced-Latte/issues/313, https://github.com/Sunagatov/Iced-Latte/issues/310"
    )
    @pytest.mark.parametrize(
        "text_review, expected_length,rating, expected_status_code, expected_error_message",
        parameterize_text_review_invalid_text,
    )
    @title("Test add review with text that do not match the requirement")
    @description(
        "GIVEN user is registered and has not posted any review on product"
        "WHEN user post review with text that do not match the requirement"
        "THEN status HTTP CODE = 400 and response body contains error message"
    )
    def test_add_review_with_invalid_text(
        self,
        create_authorized_user,
        text_review,
        expected_length,
        rating,
        expected_status_code,
        expected_error_message,
    ):
        with step("Verify review text length for test purpose"):

            if expected_length is not None:
                assert (
                    len(text_review) == expected_length
                ), f"Review text should be exactly {expected_length} characters long"
            else:
                assert (
                    len(text_review) >= 0
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

        with step(
            "Add review with text that do not match the requirement to randomly selected product"
        ):
            response_post_review = ReviewAPI().add_product_review(
                token=token,
                product_id=product_id,
                text_review=text_review,
                rating=rating,
                expected_status_code=expected_status_code,
            )

        with step("Verify error message"):
            assert_message_in_response(response_post_review, expected_error_message)

        with step(
            "Verify that the user's review is not successfully added to the product by retrieving all product reviews"
        ):
            response_get_all_review = ReviewAPI().get_all_product_reviews(
                product_id=product_id
            )

            result, message = verify_user_review_in_all_reviews(
                response_get_all_review, user, text_review=text_review, rating=rating
            )
            assert_that(result, is_(equal_to(False)), reason=message)

        with step(
            "Verify user review does not created via getting user's review through API"
        ):
            response_get_user_review = ReviewAPI().get_user_product_review(
                token=token, product_id=product_id
            )
            product_review_id = response_get_user_review.json().get(
                "productReviewId", ""
            )
            assert_that(
                product_review_id, is_(equal_to(None)), reason="review is created"
            )

    @pytest.mark.xfail(reason="https://github.com/Sunagatov/Iced-Latte/issues/314")
    @pytest.mark.parametrize(
        "add_review_to_product",
        [{"text_review": text_review_750_char, "rating": 5}],
        indirect=True,
    )
    @title("Test add twice the review by the same user")
    @description(
        "GIVEN user is registered and has already posted  review on product"
        "WHEN user post a second review to product"
        "THEN status HTTP CODE = 400 and response body contains error message"
    )
    def test_add_second_review_and_rating(self, add_review_to_product):
        with step("Registration of user and add review to randomly selected product"):
            random_product_id = add_review_to_product["random_product_id"]
            user = add_review_to_product["user"]
            user_id = user["id"]
            token = add_review_to_product["token"]
            product_review_id = add_review_to_product["product_review_id"]

        with step("Add second review to randomly selected product"):
            text_review = text_review_with_emojy
            rating = 5
            response_post_second_review = ReviewAPI().add_product_review(
                token=token,
                product_id=random_product_id,
                text_review=text_review,
                rating=rating,
                expected_status_code=400,
            )

        with step("Verify error message"):
            expected_error_message = (
                "Creation of the product's review for the user with "
                f"userId = {user_id} and the product"
                f" with productId = {random_product_id} is denied."
                f" Delete the previous product's review {product_review_id} first."
            )

            assert_message_in_response(
                response_post_second_review, expected_error_message
            )

    @title("Test add review with empty bearer token")
    @description(
        "WHEN user post review with empty bearer token"
        "THEN status HTTP CODE = 400 and response body contains error message"
    )
    def test_add_review_with_empty_bearer_token(self, create_authorized_user):
        with step("Registration of user"):
            user, _ = (
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

        with step("Add review with empty bearer token"):
            token = " "
            text_review = text_review_750_char
            rating = 5
            expected_status_code = 400
            response_post_review = ReviewAPI().add_product_review(
                token=token,
                product_id=product_id,
                text_review=text_review,
                rating=rating,
                expected_status_code=expected_status_code,
            )

        with step("Verify error message"):
            expected_error_message = token_is_absent
            assert_message_in_response(response_post_review, expected_error_message)

    @title("Test add review with expired bearer token")
    @description(
        "WHEN user post review with expired bearer token"
        "THEN status HTTP CODE = 401 and response body contains error message"
    )
    def test_add_review_with_expired_bearer_token(self, create_authorized_user):
        with step("Registration of user"):
            user, _ = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )

        with step("Generate expired bearer token"):
            expired_token = generate_jwt_token(email=user["email"], expired=True)

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

        with step("Add review with expired bearer token"):
            token = expired_token
            text_review = text_review_750_char
            rating = 5
            expected_status_code = 401
            response_post_review = ReviewAPI().add_product_review(
                token=token,
                product_id=product_id,
                text_review=text_review,
                rating=rating,
                expected_status_code=expected_status_code,
            )

        with step("Verify error message"):
            expected_error_message = token_is_expired
            assert_message_in_response(response_post_review, expected_error_message)

    @title("Test add review  with blacklist token")
    @description(
        "WHEN user post review with blacklist token"
        "THEN status HTTP CODE = 400 and response body contains error message"
    )
    def test_add_review_with_blacklist_token(self, create_authorized_user):
        user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Logging out of user"):
            logging_out_response = AuthenticateAPI().logout(token=token)
            assert_that(
                logging_out_response.status_code,
                is_(200),
                reason='Failed request "logout"',
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

        with step("Add review with blacklist bearer token"):
            token = token
            text_review = text_review_750_char
            rating = 5
            expected_status_code = 400
            response_post_review = ReviewAPI().add_product_review(
                token=token,
                product_id=product_id,
                text_review=text_review,
                rating=rating,
                expected_status_code=expected_status_code,
            )

        with step("Verify error message"):
            expected_error_message = token_is_blacklisted
            assert_message_in_response(response_post_review, expected_error_message)
