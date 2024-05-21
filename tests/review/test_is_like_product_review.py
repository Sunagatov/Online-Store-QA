import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, is_, equal_to

from framework.asserts.common import assert_content_type
from framework.endpoints.product_api import ProductAPI
from framework.endpoints.review_api import ReviewAPI
from framework.tools.favorite_methods import extract_random_product_ids
from framework.tools.review_methods import (
    verify_user_review_by_user_name_in_all_product_reviews,
    extract_data_from_random_review,
)


@pytest.mark.critical
@feature("Adding like or dislike to product review")
class TestIsLikeProductReview:
    @title("Test add like to product's review")
    @description(
        "GIVEN user is registered"
        "AND user has not posted review on product"
        "AND the user has not post any of the Like or Dislike on the specified review"
        "WHEN user post like to product's review"
        "THEN status HTTP CODE = 200 and likesCount increased by 1"
    )
    def test_add_like_to_product_review(self, create_authorized_user):
        with step("Registration of user"):
            user, token = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )

        with step("Getting all products via API"):
            response_get_product = ProductAPI().get_all()

        with step("Getting random product"):
            get_random_product = extract_random_product_ids(
                response_get_product, product_quantity=1
            )

            (product_id,) = get_random_product

        with step("Getting random product's review and it's data"):
            response_get_review = ReviewAPI().get_all_product_reviews(
                product_id=product_id
            )
            product_data = extract_data_from_random_review(response_get_review)
            review_id = None
            likes_count = None
            if product_data is None:
                get_random_product = extract_random_product_ids(
                    response_get_product, product_quantity=1
                )
                (product_id,) = get_random_product
                response_get_review = ReviewAPI().get_all_product_reviews(
                    product_id=product_id
                )
                product_data = extract_data_from_random_review(response_get_review)
            if product_data:
                review_id = product_data.get("productReviewId", "")
                likes_count = product_data.get("likesCount", 0)

            else:
                raise ValueError("Product data is None, unable to extract review data.")

        with step("Verify that user has not review for product"):
            assert_that(
                verify_user_review_by_user_name_in_all_product_reviews(
                    response_get_review, user
                ),
                is_(False),
                "user has review",
            )

        with step(
            "Add like to the product review and verify that likesCount increased by 1"
        ):
            response_is_like = ReviewAPI().like_dislike_product_review(
                token=token,
                is_like=True,
                product_review_id=review_id,
                product_id=product_id,
            )

            actual_like_count_after_like = response_is_like.json()["likesCount"]

            like_count_before_like = likes_count
            expected_like_count_after_like = like_count_before_like + 1
            assert_that(
                actual_like_count_after_like, equal_to(expected_like_count_after_like)
            )

        with step("Verify content-type"):
            assert_content_type(response_is_like, "application/json")

    @title("Test add dislike to product's review")
    @description(
        "GIVEN user is registered"
        "AND user has not posted review on product"
        "AND the user has not post any of the Like or Dislike on the specified review"
        "WHEN user post dislike to product's review"
        "THEN status HTTP CODE = 200 and dislikesCount increased by 1"
    )
    def test_add_dislike_to_product_review(self, create_authorized_user):
        with step("Registration of user"):
            user, token = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )

        with step("Getting all products via API"):
            response_get_product = ProductAPI().get_all()

        with step("Getting random product"):
            get_random_product = extract_random_product_ids(
                response_get_product, product_quantity=1
            )
            (product_id,) = get_random_product

        with step("Getting random product's review and it's data"):
            response_get_review = ReviewAPI().get_all_product_reviews(
                product_id=product_id
            )
            product_data = extract_data_from_random_review(response_get_review)
            review_id = None
            dislikes_count = None
            if product_data is None:
                get_random_product = extract_random_product_ids(
                    response_get_product, product_quantity=1
                )
                (product_id,) = get_random_product
                response_get_review = ReviewAPI().get_all_product_reviews(
                    product_id=product_id
                )
                product_data = extract_data_from_random_review(response_get_review)
            if product_data:
                review_id = product_data.get("productReviewId", "")
                dislikes_count = product_data.get("dislikesCount", 0)

            else:
                raise ValueError("Product data is None, unable to extract review data.")

        with step("Verify that user has not review for product"):
            assert_that(
                verify_user_review_by_user_name_in_all_product_reviews(
                    response_get_review, user
                ),
                is_(False),
                "user has review",
            )

        with step(
            "Add like to the product review and verify that likesCount increased by 1"
        ):
            response_is_dislike = ReviewAPI().like_dislike_product_review(
                token=token,
                is_like=False,
                product_review_id=review_id,
                product_id=product_id,
            )
            actual_dislike_count_after_like = response_is_dislike.json()[
                "dislikesCount"
            ]
            expected_dislike_count_after_like = dislikes_count + 1
            assert_that(
                actual_dislike_count_after_like,
                equal_to(expected_dislike_count_after_like),
            )

        with step("Verify content-type"):
            assert_content_type(response_is_dislike, "application/json")
