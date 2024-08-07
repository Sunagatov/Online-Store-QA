import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, is_, equal_to

from framework.asserts.common import assert_content_type
from framework.endpoints.review_api import ReviewAPI
from framework.tools.review_methods import (
    assert_reviews_sorted_by_createdAt_in_descending_order,
    assert_total_elements_reviews,
    assert_reviews_sorted_by_createdAt_in_ascending_order,
    assert_page_number_in_reviews_body,
    calculate_total_pages,
    get_amount_of_reviews_with_particular_rating,
)


@pytest.mark.critical
@feature("Get all product reviews")
class TestGetProductReviews:
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


@pytest.mark.critical
@feature("Get all product reviews")
class TestReviewWithRating:
    parameter_sets = [8]

    @title("Test get all product reviews with custom parameter size")
    @description(
        "WHEN user sent request get all product reviews with parameter size = 3"
        "THEN status HTTP CODE = 200 and response body contains all product reviews with  parameters:"
        "page = 0, size = 3, sort_attribute = createdAt, sort_direction = desc and amount of totalPages = amount of product/size"
    )
    @pytest.mark.parametrize(
        "create_certain_number_of_reviews", parameter_sets, indirect=True
    )
    def test_get_all_product_reviews_with_custom_parameter_size(
        self, create_certain_number_of_reviews
    ):
        with step("Getting all products via API without parameters"):
            product_id = create_certain_number_of_reviews
            response_get_all_review_with_default_parameters = (
                ReviewAPI().get_all_product_reviews(product_id=product_id)
            )

        with step("Getting all products via API with custom parameter size"):
            size_of_reviews_per_page = 3
            response_get_all_review_with_custom_parameter = (
                ReviewAPI().get_all_product_reviews(
                    product_id=product_id, size=size_of_reviews_per_page
                )
            )

        with step("Verify content-type"):
            assert_content_type(
                response_get_all_review_with_custom_parameter, "application/json"
            )

        # with step("Verify that default parameters page is correct"):
        #     assert_page_number_in_reviews_body(response_get_all_review_with_custom_parameter, 1)

        with step("Verify that custom parameters size is displayed correctly"):
            assert_that(
                response_get_all_review_with_custom_parameter.json().get("size", 0),
                is_(equal_to(size_of_reviews_per_page)),
                reason=f"Expected page number is {size_of_reviews_per_page}, found: '{response_get_all_review_with_custom_parameter.json().get('size', 0)}'",
            )

        with step(
            "Verify that default parameters sort_attribute and sort_direction are correct"
        ):
            assert_reviews_sorted_by_createdAt_in_descending_order(
                response_get_all_review_with_custom_parameter
            )

        with step(
            "Verify expected total number of reviews is equal to actual total number of reviews"
        ):
            expected_total_reviews = (
                response_get_all_review_with_default_parameters.json().get(
                    "totalElements"
                )
            )
            assert_total_elements_reviews(
                response_get_all_review_with_custom_parameter, expected_total_reviews
            )

        with step("Verify that total pages are correct"):
            expected_total_pages = calculate_total_pages(
                expected_total_reviews, size_of_reviews_per_page
            )
            actual_total_pages = (
                response_get_all_review_with_custom_parameter.json().get("totalPages")
            )
            assert_that(
                actual_total_pages,
                is_(equal_to(expected_total_pages)),
                reason=f"Expected total pages is {expected_total_pages}, found: '{actual_total_pages}'",
            )


@pytest.mark.critical
@feature("Get all product reviews")
class TestReviewWithRating:
    parameter_sets = [8]

    @title("Test get all product reviews with custom parameter size and sort direction")
    @description(
        "WHEN user sent request get all product reviews with parameter size = 3 and sort_direction = asc"
        "THEN status HTTP CODE = 200 and response body contains all product reviews with  parameters:"
        "page = 0, size = 3, sort_attribute = createdAt, sort_direction = asc and amount of totalPages = amount of product/size"
    )
    @pytest.mark.parametrize(
        "create_certain_number_of_reviews", parameter_sets, indirect=True
    )
    def test_get_all_product_reviews_with_custom_parameter_size_in_asc_order(
        self, create_certain_number_of_reviews
    ):
        with step("Getting all products via API without parameters"):
            product_id = create_certain_number_of_reviews
            response_get_all_review_with_default_parameters = (
                ReviewAPI().get_all_product_reviews(product_id=product_id)
            )

        with step("Getting all products via API with custom parameter size"):
            size_of_reviews_per_page = 3
            response_get_all_review_with_custom_parameter = (
                ReviewAPI().get_all_product_reviews(
                    product_id=product_id,
                    size=size_of_reviews_per_page,
                    sort_direction="asc",
                )
            )

        with step("Verify content-type"):
            assert_content_type(
                response_get_all_review_with_custom_parameter, "application/json"
            )

        # with step("Verify that default parameters page is correct"):
        #     assert_page_number_in_reviews_body(response_get_all_review_with_custom_parameter, 1)

        with step("Verify that custom parameters size is displayed correctly"):
            assert_that(
                response_get_all_review_with_custom_parameter.json().get("size", 0),
                is_(equal_to(size_of_reviews_per_page)),
                reason=f"Expected page number is {size_of_reviews_per_page}, found: '{response_get_all_review_with_custom_parameter.json().get('size', 0)}'",
            )

        with step(
            "Verify that default parameters sort_attribute and sort_direction are correct"
        ):
            assert_reviews_sorted_by_createdAt_in_ascending_order(
                response_get_all_review_with_custom_parameter
            )

        with step(
            "Verify expected total number of reviews is equal to actual total number of reviews"
        ):
            expected_total_reviews = (
                response_get_all_review_with_default_parameters.json().get(
                    "totalElements"
                )
            )
            assert_total_elements_reviews(
                response_get_all_review_with_custom_parameter, expected_total_reviews
            )

        with step("Verify that total pages are correct"):
            expected_total_pages = calculate_total_pages(
                expected_total_reviews, size_of_reviews_per_page
            )
            actual_total_pages = (
                response_get_all_review_with_custom_parameter.json().get("totalPages")
            )
            assert_that(
                actual_total_pages,
                is_(equal_to(expected_total_pages)),
                reason=f"Expected total pages is {expected_total_pages}, found: '{actual_total_pages}'",
            )


@pytest.mark.xfail(reason="Bug:")
@pytest.mark.critical
@feature("Get all product reviews")
class TestReviewWithRating:
    parameter_sets = [8]

    @title("Test get all product reviews with custom parameter size and page")
    @description(
        "WHEN user sent request get all product reviews with parameter size = 3 and page = 2"
        "THEN status HTTP CODE = 200 and response body contains all product reviews with  parameters:"
        "page = 2, size = 3, sort_attribute = createdAt, sort_direction = desc and amount of totalPages = amount of product/size"
    )
    @pytest.mark.parametrize(
        "create_certain_number_of_reviews", parameter_sets, indirect=True
    )
    def test_get_all_product_reviews_with_custom_parameter_size_and_page(
        self, create_certain_number_of_reviews
    ):
        with step("Getting all products via API without parameters"):
            product_id = create_certain_number_of_reviews
            response_get_all_review_with_default_parameters = (
                ReviewAPI().get_all_product_reviews(product_id=product_id)
            )

        with step("Getting all products via API with custom parameter size"):
            size_of_reviews_per_page = 3
            page = 2
            response_get_all_review_with_custom_parameter = (
                ReviewAPI().get_all_product_reviews(
                    product_id=product_id,
                    size=size_of_reviews_per_page,
                    sort_direction="asc",
                    page=page,
                )
            )
            print(response_get_all_review_with_custom_parameter.json())

        with step("Verify content-type"):
            assert_content_type(
                response_get_all_review_with_custom_parameter, "application/json"
            )

        with step("Verify that default parameters page is correct"):
            assert_page_number_in_reviews_body(
                response_get_all_review_with_custom_parameter, 2
            )

        with step("Verify that custom parameters size is displayed correctly"):
            assert_that(
                response_get_all_review_with_custom_parameter.json().get("size", 0),
                is_(equal_to(size_of_reviews_per_page)),
                reason=f"Expected page number is {size_of_reviews_per_page}, found: '{response_get_all_review_with_custom_parameter.json().get('size', 0)}'",
            )

        with step(
            "Verify that default parameters sort_attribute and sort_direction are correct"
        ):
            assert_reviews_sorted_by_createdAt_in_descending_order(
                response_get_all_review_with_custom_parameter
            )

        with step(
            "Verify expected total number of reviews is equal to actual total number of reviews"
        ):
            expected_total_reviews = (
                response_get_all_review_with_default_parameters.json().get(
                    "totalElements"
                )
            )
            assert_total_elements_reviews(
                response_get_all_review_with_custom_parameter, expected_total_reviews
            )

        with step("Verify that total pages are correct"):
            expected_total_pages = calculate_total_pages(
                expected_total_reviews, size_of_reviews_per_page
            )
            actual_total_pages = (
                response_get_all_review_with_custom_parameter.json().get("totalPages")
            )
            assert_that(
                actual_total_pages,
                is_(equal_to(expected_total_pages)),
                reason=f"Expected total pages is {expected_total_pages}, found: '{actual_total_pages}'",
            )


@pytest.mark.critical
@feature("Get all product reviews")
class TestReviewWithRating:
    parameter_sets = [8]

    @title(
        "Test get all product reviews with custom parameter size and filter product_ratings"
    )
    @description(
        "WHEN user sent request get all product reviews with parameter size = 4 and product_ratings = 3"
        "THEN status HTTP CODE = 200 and response body contains all product reviews with  parameters:"
        "page = 0, size = 4, sort_attribute = createdAt, sort_direction = desc, product_ratings = 3"
        " and amount of totalPages = amount of product/size"
    )
    @pytest.mark.parametrize(
        "create_certain_number_of_reviews", parameter_sets, indirect=True
    )
    def test_get_all_product_reviews_with_custom_parameter_size_and_filter_product_ratings(
        self, create_certain_number_of_reviews
    ):
        with step("Getting all products via API with custom rating parameter"):
            product_rating = 3
            product_id = create_certain_number_of_reviews
            response_get_all_review_with_default_parameters = (
                ReviewAPI().get_all_product_reviews(product_id=product_id)
            )
            expected_number_reviews_with_custom_rating = (
                get_amount_of_reviews_with_particular_rating(
                    response_get_all_review_with_default_parameters,
                    rating=product_rating,
                )
            )

        with step("Getting all products via API with custom parameter size and rating"):
            size_of_reviews_per_page = 3
            response_get_all_review_with_custom_parameter = (
                ReviewAPI().get_all_product_reviews(
                    product_id=product_id,
                    size=size_of_reviews_per_page,
                    product_ratings=product_rating,
                )
            )

        with step("Verify content-type"):
            assert_content_type(
                response_get_all_review_with_custom_parameter, "application/json"
            )

        # with step("Verify that default parameters page is correct"):
        #     assert_page_number_in_reviews_body(response_get_all_review_with_custom_parameter, 1)

        with step("Verify that custom parameters rating is displayed correctly"):
            actual_number_reviews_with_custom_rating = (
                get_amount_of_reviews_with_particular_rating(
                    response_get_all_review_with_custom_parameter, rating=product_rating
                )
            )
            assert_that(
                actual_number_reviews_with_custom_rating,
                is_(equal_to(expected_number_reviews_with_custom_rating)),
                reason=f"Expected reviews with rating is {expected_number_reviews_with_custom_rating}, found: '{actual_number_reviews_with_custom_rating}'",
            )

        with step("Verify that custom parameters size is displayed correctly"):
            assert_that(
                response_get_all_review_with_custom_parameter.json().get("size", 0),
                is_(equal_to(size_of_reviews_per_page)),
                reason=f"Expected page number is {size_of_reviews_per_page}, found: '{response_get_all_review_with_custom_parameter.json().get('size', 0)}'",
            )

        with step(
            "Verify that default parameters sort_attribute and sort_direction are correct"
        ):
            assert_reviews_sorted_by_createdAt_in_descending_order(
                response_get_all_review_with_custom_parameter
            )

        with step(
            "Verify expected total number of reviews is equal to actual total number of reviews"
        ):
            expected_total_reviews = expected_number_reviews_with_custom_rating
            assert_total_elements_reviews(
                response_get_all_review_with_custom_parameter, expected_total_reviews
            )

        with step("Verify that total pages are correct"):
            expected_total_pages = calculate_total_pages(
                expected_total_reviews, size_of_reviews_per_page
            )
            actual_total_pages = (
                response_get_all_review_with_custom_parameter.json().get("totalPages")
            )
            assert_that(
                actual_total_pages,
                is_(equal_to(expected_total_pages)),
                reason=f"Expected total pages is {expected_total_pages}, found: '{actual_total_pages}'",
            )
