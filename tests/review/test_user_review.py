import pytest
from allure import feature, title, description, step
from hamcrest import assert_that, equal_to, is_
from hamcrest import has_key

from framework.asserts.common import assert_content_type
from framework.endpoints.product_api import ProductAPI
from framework.endpoints.review_api import ReviewAPI
from framework.tools.generators import generate_jwt_token
from framework.tools.review_methods import (
    extract_random_product_info,
    verify_user_review_body,
)


@pytest.mark.critical
@feature("GET user's product review")
class TestGetUserReview:
    parameter_sets = [1]

    @title("Test get user's review")
    @description(
        "GIVEN user is registered"
        "AND user has posted review on product"
        "WHEN user sent request get user's review"
        "THEN status HTTP CODE = 200 and response body contains: productReviewId, productId, productRating"
        "textReview, likesCount, dislikesCount,createdAt,userName, userLastName"
    )
    @pytest.mark.parametrize(
        "create_certain_number_of_reviews", parameter_sets, indirect=True
    )
    def test_get_user_review(self, create_certain_number_of_reviews):
        with step("Create user's review and get token"):
            token = create_certain_number_of_reviews["token"]
            product_id = create_certain_number_of_reviews["product_id"]

        with step("Get user's review"):
            response_get_user_review = ReviewAPI().get_user_product_review(
                token=token, product_id=product_id
            )

            data_to_verify = response_get_user_review.json()

        with step("Verify response body"):
            assert_that(data_to_verify, has_key("productReviewId"))
            assert_that(data_to_verify, has_key("productId"))
            assert_that(data_to_verify, has_key("productRating"))
            assert_that(data_to_verify, has_key("text"))
            assert_that(data_to_verify, has_key("likesCount"))
            assert_that(data_to_verify, has_key("dislikesCount"))
            assert_that(data_to_verify, has_key("createdAt"))
            assert_that(data_to_verify, has_key("userName"))
            assert_that(data_to_verify, has_key("userLastname"))

        with step("Verify content-type"):
            assert_content_type(response_get_user_review, "application/json")

        with step("Verify productId is correct"):
            assert_that(data_to_verify["productId"], is_(equal_to(product_id)))

    parameter_sets = [1]

    @title("Test get user's review with empty product id")
    @description(
        "GIVEN user is registered"
        "AND user has posted review on product"
        "WHEN user sent request get user's review with empty product id"
        "THEN status HTTP CODE = 400 and response body contains: error message"
    )
    @pytest.mark.parametrize(
        "create_certain_number_of_reviews", parameter_sets, indirect=True
    )
    def test_get_user_review_with_empty_product_id(
        self, create_certain_number_of_reviews
    ):
        with step("Create user's review and get token"):
            token = create_certain_number_of_reviews["token"]

        with step("Get user's review with empty product id"):
            ReviewAPI().get_user_product_review(
                token=token, product_id="", expected_status_code=400
            )

    parameter_sets = [1]

    @title("Test get user's review with invalid product id")
    @description(
        "GIVEN user is registered"
        "AND user has posted review on product"
        "WHEN user sent request get user's review with invalid product id"
        "THEN status HTTP CODE = 400 and response body contains: error message"
    )
    @pytest.mark.parametrize(
        "create_certain_number_of_reviews", parameter_sets, indirect=True
    )
    def test_get_user_review_with_invalid_product_id(
        self, create_certain_number_of_reviews
    ):
        with step("Create user's review and get token"):
            token = create_certain_number_of_reviews["token"]
            invalid_product_id = "eec8a16-4864-4c1b-aa8b-dedfddc6e356"

        with step("Get user's review with invalid product id"):
            ReviewAPI().get_user_product_review(
                token=token, product_id=invalid_product_id, expected_status_code=404
            )

    parameter_sets = [1]

    @title("Test get user's review with EMPTY token")
    @description(
        "GIVEN user is registered"
        "AND user has posted review on product"
        "WHEN user sent request get user's review with empty token"
        "THEN status HTTP CODE = 400 and response body contains: error message"
    )
    @pytest.mark.parametrize(
        "create_certain_number_of_reviews", parameter_sets, indirect=True
    )
    def test_get_user_review_with_empty_token(self, create_certain_number_of_reviews):
        with step("Create user's review and get token"):
            product_id = create_certain_number_of_reviews["product_id"]

        with step("Get user's review with empty token"):
            ReviewAPI().get_user_product_review(
                token="", product_id=product_id, expected_status_code=400
            )

    parameter_sets = [1]

    @title("Test get user's review with blacklisted token")
    @description(
        "GIVEN user is registered"
        "AND user has posted review on product"
        "WHEN user sent request get user's review with blacklisted token"
        "THEN status HTTP CODE = 401 and response body contains: error message"
    )
    @pytest.mark.parametrize(
        "create_certain_number_of_reviews", parameter_sets, indirect=True
    )
    def test_get_user_review_with_blacklisted_token(
        self, create_authorized_user, create_certain_number_of_reviews
    ):
        with step("Get user's review with blacklisted token"):
            product_id = create_certain_number_of_reviews["product_id"]
            user = create_certain_number_of_reviews["user"]
            email = user["email"]
            blacklisted_token = generate_jwt_token(email=email, expired=True)
            ReviewAPI().get_user_product_review(
                token=blacklisted_token, product_id=product_id, expected_status_code=401
            )

    parameter_sets = [1]

    @title("Test get user's review for product that user has not reviewed")
    @description(
        "GIVEN user is registered"
        "WHEN user sent request get user's review for product that user has not reviewed"
        "THEN status HTTP CODE = 200 and response body with key's values = null"
    )
    @pytest.mark.parametrize(
        "create_certain_number_of_reviews", parameter_sets, indirect=True
    )
    def test_get_review_for_product_that_user_has_not_reviewed(
        self, create_authorized_user, create_certain_number_of_reviews
    ):
        with step("Get user's review for product that user has not reviewed"):
            response_get_all_product = ProductAPI().get_all()

            extract_product_info = extract_random_product_info(
                response_get_all_product, product_quantity=1
            )
            product_id = extract_product_info[0]["id"]
            token = create_certain_number_of_reviews["token"]

            response_user_review = ReviewAPI().get_user_product_review(
                token=token, product_id=product_id, expected_status_code=200
            )

        with step("Verify response body does not contain any data"):
            verify_user_review_body(response_user_review, value=None)
