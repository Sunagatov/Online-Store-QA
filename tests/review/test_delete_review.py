import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, is_, equal_to

from data.text_review import text_review_750_char
from framework.endpoints.product_api import ProductAPI
from framework.endpoints.review_api import ReviewAPI
from framework.tools.review_methods import (
    verify_user_review_in_all_reviews,
    extract_product_info_from_list_of_products,
)


@pytest.mark.critical
@feature("Delete review and rating to product")
class TestReviewWithRating:
    @pytest.mark.parametrize(
        "add_review_to_product",
        [{"text_review": text_review_750_char, "rating": 5}],
        indirect=True,
    )
    @title("Test delete review  and rating to product")
    @description(
        "GIVEN user is registered and  posted review on product"
        "WHEN user delete review and rating to product"
        "THEN status HTTP CODE = 200 and product review count and average rating getting from statistics request"
        "  and products request should be equal"
    )
    def test_delete_review_and_rating(self, add_review_to_product):
        with step("Registration of user and add review to randomly selected product"):
            random_product_id = add_review_to_product["random_product_id"]
            user = add_review_to_product["user"]
            token = add_review_to_product["token"]
            product_review_id = add_review_to_product["product_review_id"]

        with step(
            "Extract review count and average rating for product before delete review"
        ):
            response_get_all_products = ProductAPI().get_all()
            product_info = extract_product_info_from_list_of_products(
                response_get_all_products, random_product_id
            )
            product_review_count_before_delete_review = product_info[0]["reviewsCount"]
            product_average_rating_before_delete_review = product_info[0][
                "averageRating"
            ]

        with step("Get statistic for product before delete review"):
            response_get_statistic = ReviewAPI().get_product_review_statistics(
                product_id=random_product_id
            )
            product_review_count_statistic_before_delete_review = (
                response_get_statistic.json().get("reviewsCount")
            )
            product_average_rating_statistic_before_delete_review = (
                response_get_statistic.json().get("avgRating")
            )

        with step(
            "Compare data from statistic response with data from get product response before delete review"
        ):
            assert_that(
                product_review_count_before_delete_review,
                is_(equal_to(product_review_count_statistic_before_delete_review)),
            )

            assert_that(
                float(product_average_rating_before_delete_review),
                is_(
                    equal_to(
                        float(product_average_rating_statistic_before_delete_review)
                    )
                ),
            )

        with step("Delete review"):
            response_after_delete_review = ReviewAPI().delete_product_review(
                token=token, product_id=random_product_id, review_id=product_review_id
            )

        with step(
            "Extract review count and average rating for product after delete review"
        ):
            response_get_all_products = ProductAPI().get_all()
            product_info = extract_product_info_from_list_of_products(
                response_get_all_products, random_product_id
            )
            product_review_count_after_delete_review = product_info[0]["reviewsCount"]
            product_average_rating_after_delete_review = product_info[0][
                "averageRating"
            ]

        with step("Verify that review was deleted"):
            response_get_all_review = ReviewAPI().get_all_product_reviews(
                product_id=random_product_id
            )
            result, message = verify_user_review_in_all_reviews(
                response_get_all_review,
                user,
                text_review=text_review_750_char,
                rating=5,
            )
            assert_that(result, is_(equal_to(False)), reason=message)

        with step("Get statistic for product after delete review"):
            response_get_statistic = ReviewAPI().get_product_review_statistics(
                product_id=random_product_id
            )
            product_review_count_statistic_after_delete_review = (
                response_get_statistic.json().get("reviewsCount")
            )
            product_average_rating_statistic_after_delete_review = (
                response_get_statistic.json().get("avgRating")
            )

        with step(
            "Compare data from statistic response with data from get product response after delete review"
        ):
            assert_that(
                product_review_count_after_delete_review,
                is_(equal_to(product_review_count_statistic_after_delete_review)),
            )

            assert_that(
                float(product_average_rating_after_delete_review),
                is_(
                    equal_to(
                        float(product_average_rating_statistic_after_delete_review)
                    )
                ),
            )
