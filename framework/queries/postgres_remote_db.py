from typing import Optional

from framework.clients.db_client_ssh import DBClient
from framework.tools.generators import generate_user


class PostgresDB:
    def __init__(
        self,
        ssh_username: str,
        ssh_password: str,
        local_server_ip: str,
        remote_server_ip: str,
        db_username: str,
        db_password: str,
        database_name: str,
        port_ssh: int,
    ):
        """Initialize the database connection"""
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.local_server_ip = local_server_ip
        self.remote_server_ip = remote_server_ip
        self.db_username = db_username
        self.db_password = db_password
        self.database_name = database_name
        self.port_ssh = port_ssh

        self.db = DBClient(
            ssh_username=self.ssh_username,
            ssh_password=self.ssh_password,
            local_server_ip=self.local_server_ip,
            db_username=self.db_username,
            db_password=self.db_password,
            database_name=self.database_name,
            remote_server_ip=self.remote_server_ip,
            port_ssh=self.port_ssh,
        )

    def close(self) -> None:
        """Close the database connection"""
        self.db.close()

    # def get_data_by_filter(self, table: str, field: str, value: str) -> list[tuple]:
    #     """Retrieve data from a specified table by filtering on a specified field"""
    #     query = f"SELECT * FROM {table} WHERE {field} = %s"
    #     return self.db.fetch_all(query, (value,))
    def get_data_by_filter(self, table: str, field: str, value: str) -> list[tuple]:
        """Retrieve data from a specified table by filtering on a specified field"""
        if not self.is_valid_identifier(table) or not self.is_valid_identifier(field):
            raise ValueError("Invalid table or field name")

        query = f"SELECT * FROM {table} WHERE {field} = %s"
        return self.db.fetch_all(query, (value,))

    @staticmethod
    def is_valid_identifier(identifier: str) -> bool:
        """Check if the identifier is a valid SQL identifier to prevent SQL injection"""
        # This checks if the identifier is composed of valid characters (letters, numbers, and underscores)
        return identifier.isidentifier() and not identifier.isnumeric()

    def get_random_products(self, quantity: int = 1) -> list[tuple]:
        """Retrieve a specified number of random active products"""
        query = """
           SELECT *
           FROM product
           WHERE active = true
           ORDER BY RANDOM()
           LIMIT %s;
       """
        return self.db.fetch_all(query, (quantity,))

    def get_product_by_filter(
        self, field: str, ascend: bool = False, size: int = -1, page: int = -1
    ) -> list[tuple]:
        """Get sorted products by size and paginate


        Args:
            field: field for sorting;
            ascend: ascending sort order, True - ascending, False - descending;
            size: the amount of data per page;
            page: page number.
        """
        query = f"""
           SELECT *
           FROM product
           ORDER BY {field} {'ASC' if ascend else 'DESC'}
       """
        params = ()
        if size > 0:
            query += " LIMIT %s"
            params += (size,)
        if page >= 0:
            query += " OFFSET %s"
            params += (size * page,)
        return self.db.fetch_all(query, params)

    def get_random_users(self, quantity: int = 1) -> list[tuple]:
        """Get random users


        Args:
            quantity: number of random users
        """
        query = """
           SELECT *
           FROM user_details
           ORDER BY RANDOM()
           LIMIT %s;
       """
        return self.db.fetch_all(query, (quantity,))

    def create_user(self, user: dict) -> None:
        """Insert a user into the database


        Args:
            user: user data:
                - id: user id;
                - first_name: first name of user;
                - last_name: last name of user;
                - email: email of user;
                - password: password for user;
                - hashed_password: hash of password for user.
        """
        query = """
           INSERT INTO public.user_details(
               id, first_name, last_name, stripe_customer_token, birth_date,
               phone_number, email, password, address_id, account_non_expired,
               account_non_locked, credentials_non_expired, enabled
           ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL, true, true, true, true);
       """
        params = (
            user["id"],
            user["first_name"],
            user["last_name"],
            user["stripe_customer_token"],
            user["birth_date"],
            user["phone_number"],
            user["email"],
            user["hashed_password"],
        )
        self.db.execute(query, params)

    def create_random_users(self, quantity: int = 1) -> list[None]:
        """Create random user(s)


        Args:
            quantity: number of random users
        """
        return [self.create_user(generate_user()) for _ in range(quantity)]

    def delete_user(self, user_id: str) -> None:
        """Delete a user from the database based on user ID


        Args:
            user_id: user ID
        """
        query = "DELETE FROM public.user_details WHERE id = %s"
        self.db.execute(query, (user_id,))

    def select_user_by_email(self, email: str) -> Optional[int]:
        """Search for a user by email in the database and return the count of users with that email.

        Args:
            email: user's email

        Returns:
            Optional[int]: The count of users with the given email or None if an error occurs.
        """
        query = "SELECT COUNT(*) FROM user_details WHERE email = %s"
        if result := self.db.fetch_all(query, (email,)):
            return result[0][0]  # Assuming fetch_all returns a list of tuples
        return None
