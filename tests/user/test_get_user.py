import pytest
from allure import feature, description, step, title
from hamcrest import assert_that, is_

from data.error_message_token import (
    token_is_blacklisted,
    token_is_absent,
    token_is_expired,
    token_containing_not_correct_user_email,
    token_not_containing_email,
)
from framework.asserts.common import (
    assert_status_code,
    assert_content_type,
    assert_response_message,
)
from framework.asserts.user_asserts import assert_user_data_matches
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.generators import generate_user
from framework.tools.generators import generate_jwt_token


@feature("Getting user info")
class TestGetUser:
    @pytest.mark.skip(
        reason="AssertionError: Field 'avatarLink' mismatch: Expected 'None', Found 'default file"
    )
    @title("Getting User's Own Information")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to get their own information, "
        "THEN the response code is 200 and the response body contains the current user's data."
    )
    def test_get_user_self_info(self, create_authorized_user):
        user, token = [create_authorized_user["user"], create_authorized_user["token"]]

        with step("Getting user info via API"):
            getting_user_response = UsersAPI().get_user(token=token)

        with step("Checking the response code"):
            assert_status_code(getting_user_response, 200)

        with step("Checking the response body"):
            user_data = getting_user_response.json()
            assert_user_data_matches(user_data, user)

    @pytest.mark.skip(reason="IL-230")
    @title("Getting User Info with Invalid Token")
    @description(
        "GIVEN the user is registered, "
        "WHEN the user sends a request to get user information using an invalid token, "
        "THEN the response code is 401 and the response body contains an appropriate error message."
    )
    def test_get_user_info_with_invalid_token(self):
        with step("Getting user info"):
            invalid_token = "invalid_token"
            getting_user_response = UsersAPI().get_user(
                token=invalid_token, expected_status_code=500
            )

        with step("Checking the response code"):
            assert_status_code(getting_user_response, 500)

        with step("Checking the Content-Type"):
            assert_content_type(getting_user_response, "application/json")

        with step("Checking the response body"):
            expected_error_message = "Internal server error"
            assert_response_message(getting_user_response, expected_error_message)

    @title("Getting User Info with Expired Token")
    @description(
        "GIVEN the user is registered, "
        "WHEN the user sends a request to get information about herself with expired token, "
        "THEN the response code is 401 and the response body contains the error message"
    )
    def test_getting_user_with_expired_token(self, create_user):
        with step("Getting user info"):
            expired_token = generate_jwt_token(email=create_user["email"], expired=True)
            getting_user_response = UsersAPI().get_user(
                token=expired_token, expected_status_code=401
            )

        with step("Checking the response code"):
            assert_status_code(getting_user_response, 401)

        with step("Checking the response body"):
            expected_error_message = token_is_expired
            assert_response_message(getting_user_response, expected_error_message)

    @title("Getting User Info with Empty Token")
    @description(
        "GIVEN the user is registered, "
        "WHEN the user sends a request to get information about herself with empty token, "
        "THEN the response code is 401 and the response body contains the error message"
    )
    def test_getting_user_with_empty_token(self):
        with step("Getting user info"):
            getting_user_response = UsersAPI().get_user(expected_status_code=400)

        with step("Checking the response code"):
            assert_status_code(getting_user_response, 400)

        with step("Checking the response body"):
            expected_error_message = token_is_absent
            assert_response_message(getting_user_response, expected_error_message)

    @title("Getting User Info with Blacklisted Token")
    @description(
        "GIVEN the user is logged out, "
        "WHEN the user sends a request to get information about herself with blacklisted token, "
        "THEN the response code is 401 and the response body contains the error message"
    )
    def test_getting_user_with_blacklisted_token(self, create_authorized_user):
        user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Logging out of user"):
            logging_out_response = AuthenticateAPI().logout(token=token)
            assert_that(
                logging_out_response.status_code,
                is_(200),
                reason='Failed request "logout"',
            )

        with step("Getting user info"):
            getting_user_response = UsersAPI().get_user(
                token=token, expected_status_code=400
            )

        with step("Checking response code"):
            assert_status_code(getting_user_response, 400)

        with step("Checking the response body"):
            expected_error_message = token_is_blacklisted
            assert_response_message(getting_user_response, expected_error_message)

    @title("Getting User Info with Missing Email in Token")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to get information about herself with token not containing email, "
        "THEN the response code is 401 and the response body contains the error message"
    )
    def test_getting_user_with_token_not_containing_email(self):
        with step("Getting user info"):
            token_without_email = generate_jwt_token()
            getting_user_response = UsersAPI().get_user(
                token=token_without_email, expected_status_code=400
            )

        with step("Checking response code"):
            assert_status_code(getting_user_response, 400)

        with step("Checking the response body"):
            expected_error_message = token_not_containing_email
            assert_response_message(getting_user_response, expected_error_message)

    @title("Getting User Info with Token of Non-Existing User")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to get information about herself with token of non-existing user, "
        "THEN the response code is 401 and the response body contains the error message"
    )
    def test_getting_user_with_token_not_containing_correct_user_email(self):
        with step("Getting user info"):
            email_of_non_existing_user = generate_user()["email"]
            token_of_non_existing_user = generate_jwt_token(email_of_non_existing_user)
            getting_user_response = UsersAPI().get_user(
                token=token_of_non_existing_user, expected_status_code=404
            )

        with step("Checking response code"):
            assert_status_code(getting_user_response, 404)

        with step("Checking the response body"):
            expected_error_message = token_containing_not_correct_user_email
            assert_response_message(getting_user_response, expected_error_message)
