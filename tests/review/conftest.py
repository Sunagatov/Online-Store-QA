import random

from allure_commons._allure import step

from data.text_review import parameterize_text_review_positive
from data.text_reviews_for_product import reviews
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.product_api import ProductAPI
from framework.endpoints.review_api import ReviewAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.favorite_methods import extract_random_product_ids
from framework.tools.generators import generate_user
from framework.tools.review_methods import (
    verify_user_review_by_user_name_in_all_product_reviews,
)

import pytest
from hamcrest import assert_that, is_


def generate_and_insert_user(postgres):
    """Generating and inserting a user into the database

    Args:
        postgres: connection to Postgres DataBase
    """

    user = generate_user()

    key_mapping = {
        "firstName": "first_name",
        "lastName": "last_name",
        "birthDate": "birth_date",
        "phoneNumber": "phone_number",
        "stripeCustomerToken": "stripe_customer_token",
    }
    user_to_insert = {key_mapping.get(k, k): v for k, v in user.items()}

    postgres.create_user(user_to_insert)

    return user


def create_and_authorize_user(postgres):
    """Creating and authorizing a user within the test.

    Args:
        postgres: connection to Postgres DataBase
    """
    with step("Creating user in DB"):
        user_to_create = generate_and_insert_user(postgres)

    with step("Authentication of user and getting token"):
        authentication_response = AuthenticateAPI().authentication(
            email=user_to_create["email"], password=user_to_create["password"]
        )
        token = authentication_response.json()["token"]
        refresh_token = authentication_response.json()["refreshToken"]
    return {"user": user_to_create, "token": token, "refreshToken": refresh_token}


def delete_user(token):
    """Deleting a user from the database.

    Args:
        token (): Authentication token of the user to delete
    """
    with step("Deleting user"):
        UsersAPI().delete_user(token=token)


@pytest.fixture(scope="function")
def create_certain_number_of_reviews(postgres, request):
    created_users = []
    num_reviews = request.param
    selected_reviews = random.sample(reviews, num_reviews)
    try:
        with step("Getting all products via API"):
            response_get_product = ProductAPI().get_all()

        with step("Verify that user does not have review for product"):
            get_random_product = extract_random_product_ids(
                response_get_product, product_quantity=1
            )
            (product_id,) = get_random_product
            response_get_all_review = ReviewAPI().get_all_product_reviews(
                product_id=product_id
            )

        for i, review in enumerate(selected_reviews):
            with step("Creating and authorizing user"):
                user_data = create_and_authorize_user(postgres)
                user, token = user_data["user"], user_data["token"]
                created_users.append(token)

            with step("Verify that user does not have review for product"):
                assert_that(
                    verify_user_review_by_user_name_in_all_product_reviews(
                        response_get_all_review, user
                    ),
                    is_(False),
                    f"user {i + 1} has review",
                )

            with step("Add review to randomly selected product by user"):
                response_post_review = ReviewAPI().add_product_review(
                    token=token,
                    product_id=product_id,
                    text_review=review["text_review"],
                    rating=review["rating"],
                )

            with step(
                "Verify that the user's review is successfully added to the product by retrieving all product reviews"
            ):
                response_get_all_review = ReviewAPI().get_all_product_reviews(
                    product_id=product_id
                )

        yield product_id
    finally:
        # Cleanup: delete all users created during the test
        for token in created_users:
            delete_user(token)
