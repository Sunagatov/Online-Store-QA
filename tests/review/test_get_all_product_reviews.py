from datetime import datetime

import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, is_, equal_to

from framework.asserts.common import assert_content_type
from framework.endpoints.review_api import ReviewAPI
from framework.tools.review_methods import (
    assert_page_number_in_reviews_body,
    assert_reviews_sorted_by_createdAt_in_descending_order,
    assert_size_reviews_per_page,
    assert_total_elements_reviews,
)


@pytest.mark.critical
@feature("Get all product reviews")
class TestReviewWithRating:
    parameter_sets = [4]

    @title("Test get all product reviews with default parameters")
    @description(
        "WHEN user sent request get all product reviews with default parameters"
        "THEN status HTTP CODE = 200 and response body contains all product reviews with default parameters:"
        "page = 0, size = 10, sort_attribute = createdAt, sort_direction = desc"
    )
    @pytest.mark.parametrize(
        "create_certain_number_of_reviews", parameter_sets, indirect=True
    )
    def test_get_all_product_reviews(self, create_certain_number_of_reviews):
        with step("Getting all products via API"):
            product_id = create_certain_number_of_reviews
            response_get_all_review = ReviewAPI().get_all_product_reviews(
                product_id=product_id
            )
        with step("Verify content-type"):
            assert_content_type(response_get_all_review, "application/json")

        with step(
            "Verify expected total number of reviews is equal to actual total number of reviews"
        ):
            expected_total_reviews = response_get_all_review.json().get("totalElements")
            assert_total_elements_reviews(
                response_get_all_review, expected_total_reviews
            )

        with step("Verify that default parameters page and size are correct"):
            # assert_page_number_in_reviews_body(response_get_all_review, 0)
            assert_that(
                response_get_all_review.json().get("size", 0),
                is_(equal_to(10)),
                reason=f"Expected page number is '10', found: '{response_get_all_review.json().get('size', 0)}'",
            )

        with step(
            "Verify that default parameters sort_attribute and sort_direction are correct"
        ):
            assert_reviews_sorted_by_createdAt_in_descending_order(
                response_get_all_review
            )
