import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, empty, none, any_of, is_

from data.text_review import text_review_750_char, text_review_1500_char
from framework.asserts.assert_favorite import assert_added_product_in_favorites
from framework.asserts.common import assert_content_type
from framework.endpoints.favorite_api import FavoriteAPI
from framework.endpoints.product_api import ProductAPI
from framework.endpoints.review_api import ReviewAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.favorite_methods import extract_random_product_ids


@pytest.mark.critical
@feature("Adding product to favorite ")
class TestReview:
    @pytest.mark.parametrize(
        "text_review,expected_length",
        [(text_review_750_char, 750), (text_review_1500_char, 1500)],
    )
    @title("Test add review to product")
    @description(
        "GIVEN user is registered and has not posted any review on product"
        "WHEN user post review to product"
        "THEN status HTTP CODE = 200 and response body contains text added review, id review and data posted review"
    )
    def test_add_review(self, create_authorized_user, text_review, expected_length):
        with step("Verify review text length"):
            assert (
                len(text_review) == expected_length
            ), f"Review text should be exactly {expected_length} characters long"

        with step("Registration of user"):
            user, token = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )
            print(user)

        with step("Getting all products via API"):
            response_get_product = ProductAPI().get_all()

        with step("Select and add random products to favorite"):
            get_random_product = extract_random_product_ids(
                response_get_product, product_quantity=1
            )
            (product_id,) = get_random_product
            response_post_review = ReviewAPI().add_product_review(
                token=token, product_id=product_id, text_review=text_review
            )
