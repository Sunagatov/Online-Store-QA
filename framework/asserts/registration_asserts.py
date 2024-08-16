from hamcrest import assert_that, is_
import bcrypt


def check_mapping_api_to_db(api_request: dict, database_data: tuple) -> None:
    """Checking the mapping of data from the request API to the database

    Args:
        api_request:    reference data, data from an API request;
        database_data:  compared data, data from the database (a dictionary).
    """
    fields_api_to_db = {
        "email": database_data[6],
        "firstName": database_data[1],
        "lastName": database_data[2],
        "password": database_data[7],
    }

    hashed_password = bcrypt.hashpw(
        api_request["password"].encode("utf-8"),
        fields_api_to_db["password"].encode("utf-8"),
    ).decode("utf-8")

    for key_api, value_db in fields_api_to_db.items():
        if key_api == "password":
            assert_that(
                hashed_password,
                is_(value_db),
                reason=f'"{key_api}" not equal to the expected value in the database',
            )
        else:
            assert_that(
                api_request[key_api],
                is_(value_db),
                reason=f'"{key_api}" not equal to the expected value in the database',
            )
