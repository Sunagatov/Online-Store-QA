import pytest
from allure import feature, description, link, step, title
from allure import severity
from hamcrest import assert_that, not_

from configs import (
    email_iced_late,
    imap_server2,
    email_address_to_connect2,
    gmail_password2,
    EMAIL_DOMAIN2,
    EMAIL_LOCAL_PART2,
)
from framework.asserts.common import assert_message_in_response
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.class_email import Email
from framework.tools.generators import (
    generate_password,
    generate_string,
    generate_numeric_password,
    generate_user,
    append_random_to_local_part_email,
)
from tests.conftest import generate_and_insert_user_with_custom_gmail


@feature("Reset password")
@link(
    url="http://localhost:8083/api/docs/swagger-ui/index.html#/Security/changePassword",
)
class TestResetPassword:
    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test change password through reset password")
    @description(
        "Give user registered."
        "WHEN user sent request to change password."
        "THEN status HTTP CODE = 200 "
    )
    def test_change_password_through_reset_password(self, postgres):
        with step("Registration user"):
            email_random = append_random_to_local_part_email(
                domain=EMAIL_DOMAIN2,
                email_local_part=EMAIL_LOCAL_PART2,
                length_random_part=5,
            )
            user_data = generate_user(email=email_random)
            registered_user = generate_and_insert_user_with_custom_gmail(
                postgres, user=user_data
            )
            email = registered_user["email"]
            password = registered_user["password"]

        with step("Get token by authentication"):
            response_auth = AuthenticateAPI().authentication(
                email=email, password=password
            )
            token = response_auth.json()["token"]

        with step("Sent request to reset password"):
            email_to_reset_password = email
            AuthenticateAPI().forgot_password(email=email_to_reset_password)

        with step("Verify reset code successfully delivered to user's email"):
            email_box = "Inbox"
            key = "from_"
            value = email_iced_late
            code_reset_from_email = Email(
                imap_server=imap_server2,
                email_address=email_address_to_connect2,
                mail_password=gmail_password2,
            ).extract_confirmation_code_from_email(
                email_box=email_box, key=key, value=value
            )

            assert_that(code_reset_from_email, not_(None), "Code should not be empty")

        with step("Sent request to reset password"):
            new_password = generate_password(8)
            AuthenticateAPI().change_password_through_reset(
                email=email,
                code_for_reset_password=code_reset_from_email,
                new_password=new_password,
            )

        with step(
            "Verify password reset successfully by Authorization request with new password"
        ):
            AuthenticateAPI().authentication(
                email=email, password=new_password, expected_status_code=200
            )

        with step("Deleting user"):
            UsersAPI().delete_user(token=token)

    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test change password through reset password. Incorrect code")
    @description(
        "Give user registered."
        "WHEN user sent request to change password with incorrect code."
        "THEN status HTTP CODE = 400 and appropriate error message"
    )
    @pytest.mark.parametrize(
        "code_for_reset_password,email, new_password, expected_status_code, expected_message_part",
        [
            pytest.param(
                " ", None, generate_password(8), 400, "Code is the mandatory attribute"
            ),
            pytest.param(
                "testtest",
                None,
                generate_password(8),
                400,
                "Incorrect token format, token must be ###-###-###",
            ),
            pytest.param(
                "123-123-123 ", None, generate_password(8), 400, "Incorrect token"
            ),
            pytest.param(
                "12345678910 ",
                None,
                generate_password(8),
                400,
                "Incorrect token format, token must be ###-###-###",
            ),
            pytest.param(
                "$*@!_+_*&%",
                None,
                generate_password(8),
                400,
                "Incorrect token format, token must be ###-###-###",
            ),
        ],
    )
    def test_reset_password_incorrect_code(
        self,
        create_authorized_user,
        code_for_reset_password,
        email,
        new_password,
        expected_status_code,
        expected_message_part,
    ):
        with step("Registration user"):
            user = create_authorized_user["user"]

        with step("Sent request to reset password"):
            email = user["email"] if email is None else email
            response_reset_password = AuthenticateAPI().change_password_through_reset(
                email=email,
                code_for_reset_password=code_for_reset_password,
                new_password=new_password,
                expected_status_code=400,
            )

        with step("Verify error message"):
            assert_message_in_response(
                response=response_reset_password, expected_message=expected_message_part
            )

        with step(
            "Verify password does not reset successfully by Authorization request with new password"
        ):
            AuthenticateAPI().authentication(
                email=email, password=new_password, expected_status_code=401
            )

    @pytest.mark.xfail(
        reason="Incorrect error message and status code."
        "Link: https://trello.com/c/MiA5Evtu/17-reset-password-with-invalid-email-unclear-error-message"
    )
    @pytest.mark.medium
    @severity(severity_level="MEDIUM")
    @title("Test change password through reset password, incorrect email")
    @description(
        "Give user registered."
        "WHEN user sent request to change password with incorrect code."
        "THEN status HTTP CODE = 400 and appropriate error message"
    )
    @pytest.mark.parametrize(
        "code_for_reset_password,email, new_password, expected_status_code, expected_message_part",
        [
            pytest.param(
                " ",
                "example.domain.com",
                generate_password(8),
                400,
                "Email must be valid",
            ),
            pytest.param(
                "123-123-123",
                "usernamegmail.com",
                generate_password(8),
                400,
                "Email must be valid",
            ),
            pytest.param(
                "123-123-123 ",
                "username@",
                generate_password(8),
                400,
                "Email must be valid",
            ),
            pytest.param(
                "123-123-123",
                "john doe@gmail.com",
                generate_password(8),
                400,
                "Email must be valid",
            ),
            pytest.param(
                "123-123-123",
                "user!name@gmail.com",
                generate_password(8),
                400,
                "Email must be valid",
            ),
            pytest.param(
                "123-123-123",
                "@gmail.com",
                generate_password(8),
                400,
                "Email must be valid",
            ),
            pytest.param(
                "123-123-123",
                "user@name@gmail.com",
                generate_password(8),
                400,
                "Email must be valid",
            ),
            pytest.param(
                "123-123-123",
                "username@gmail",
                generate_password(8),
                400,
                "Email must be valid",
            ),
            pytest.param(
                "123-123-123",
                "user@name@gmail.com",
                generate_password(8),
                400,
                "Email must be valid",
            ),
            pytest.param(
                "123-123-123",
                ".username@gmail.com",
                generate_password(8),
                400,
                "Email must be valid",
            ),
            pytest.param(
                "123-123-123",
                "username@example_gmail.com",
                generate_password(8),
                400,
                "Email must be valid",
            ),
            pytest.param(
                "123-123-123",
                "",
                generate_password(8),
                400,
                "Email is required field",
            ),
        ],
    )
    def test_reset_password_incorrect_email(
        self,
        create_authorized_user,
        code_for_reset_password,
        email,
        new_password,
        expected_status_code,
        expected_message_part,
    ):
        with step("Registration user"):
            user = create_authorized_user["user"]

        with step("Sent request to reset password"):
            email = user["email"] if email is None else email
            response_reset_password = AuthenticateAPI().change_password_through_reset(
                email=email,
                code_for_reset_password=code_for_reset_password,
                new_password=new_password,
                expected_status_code=400,
            )

        with step("Verify error message"):
            assert_message_in_response(
                response=response_reset_password, expected_message=expected_message_part
            )

        with step(
            "Verify password does not reset successfully by Authorization request with new password"
        ):
            AuthenticateAPI().authentication(
                email=email, password=new_password, expected_status_code=401
            )

    @pytest.mark.xfail(
        reason="app accepted password that does not meet requirements."
        "Bug: https://trello.com/c/ilaf1Luy/19-reset-password-the-app-allows-saving-passwords-that-do-not-meet-the-requirements"
    )
    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test change password through reset password with incorrect password")
    @description(
        "Give user registered."
        "WHEN user sent request to change password with incorrect password."
        "THEN status HTTP CODE = 400 and appropriate error message"
    )
    @pytest.mark.parametrize(
        "email_to_reset,code_for_reset_password, new_password,expected_status_code,expected_message_part",
        [
            pytest.param(
                None,
                None,
                generate_string(2),
                400,
                "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&",
            ),
            pytest.param(
                None,
                None,
                generate_string(9),
                400,
                "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&",
            ),
            pytest.param(
                None,
                None,
                generate_numeric_password(1),
                400,
                "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&",
            ),
            pytest.param(
                None,
                None,
                generate_numeric_password(9),
                400,
                "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&",
            ),
            pytest.param(
                None,
                None,
                f"{generate_numeric_password(length=7)}@$!%*?&",
                400,
                "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&",
            ),
            pytest.param(
                None,
                None,
                f"{generate_string(7)}@$!%*?&",
                400,
                "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&",
            ),
            pytest.param(
                None,
                None,
                "@$!%*?&",
                400,
                "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&",
            ),
            pytest.param(
                None,
                None,
                "___________",
                400,
                "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&",
            ),
        ],
    )
    def test_change_password_incorrect_password(
        self,
        email_to_reset,
        code_for_reset_password,
        new_password,
        expected_status_code,
        expected_message_part,
        postgres,
    ):
        with step("Registration user"):
            email_random = append_random_to_local_part_email(
                domain=EMAIL_DOMAIN2,
                email_local_part=EMAIL_LOCAL_PART2,
                length_random_part=5,
            )
            user_data = generate_user(email=email_random)
            registered_user = generate_and_insert_user_with_custom_gmail(
                postgres, user=user_data
            )
            email = (
                registered_user["email"] if email_to_reset is None else email_to_reset
            )
            password = registered_user["password"]

        with step("Get token by authentication"):
            response_auth = AuthenticateAPI().authentication(
                email=email, password=password
            )
            token = response_auth.json()["token"]

        with step("Sent request to reset password"):
            email_to_reset_password = email
            AuthenticateAPI().forgot_password(email=email_to_reset_password)

        with step("Verify reset code successfully delivered to user's email"):
            email_box = "Inbox"
            key = "from_"
            value = email_iced_late
            code_for_reset_password = (
                Email(
                    imap_server=imap_server2,
                    email_address=email_address_to_connect2,
                    mail_password=gmail_password2,
                ).extract_confirmation_code_from_email(
                    email_box=email_box, key=key, value=value
                )
                if code_for_reset_password is None
                else code_for_reset_password
            )

            assert_that(code_for_reset_password, not_(None), "Code should not be empty")

        with step("Sent request to reset password"):
            new_password = new_password
            response_reset_password = AuthenticateAPI().change_password_through_reset(
                email=email,
                code_for_reset_password=code_for_reset_password,
                new_password=new_password,
                expected_status_code=expected_status_code,
            )

        with step(
            "Verify password not reset successfully by Authorization request with new password"
        ):
            AuthenticateAPI().authentication(
                email=email, password=new_password, expected_status_code=401
            )
        with step("Verify error message"):
            assert_message_in_response(response_reset_password, expected_message_part)

        with step("Deleting user"):
            UsersAPI().delete_user(token=token)
