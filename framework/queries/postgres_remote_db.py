from typing import List, Optional

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

    def get_data_by_filter(
        self, table: str, field: str, value: str
    ) -> Optional[List[dict]]:
        """Retrieve data from a specified table by filtering on a specified field"""
        query = f"""
           SELECT *
           FROM {table}
           WHERE {field} = '{value}';
       """
        return self.db.fetch_all(query)

    def get_random_products(self, quantity: int = 1) -> Optional[List[dict]]:
        """Retrieve a specified number of random active products"""
        query = f"""
           SELECT *
           FROM product
           WHERE active = true
           ORDER BY RANDOM()
           LIMIT {quantity};
       """
        return self.db.fetch_all(query)

    def get_product_by_filter(
        self, field: str, ascend: bool = False, size: int = -1, page: int = -1
    ) -> Optional[List[dict]]:
        """Getting sorted products by size and page by page


        Args:
            field:  field for sorted;
            ascend: ascending sorted, True - ascending, False - descending;
            size:   the amount of data per page;
            page:   page number.
        """
        response = f"""
           SELECT *
           FROM product
           ORDER BY {field} {'ASC' if ascend else 'DESC'}
       """
        if size > 0:
            response += f" LIMIT {size}"
        if page >= 0:
            response += f" OFFSET {size * page}"
        return self.db.fetch_all(response)

    def get_random_users(self, quantity: int = 1) -> List[dict]:
        """Getting a random user


        Args:
            quantity: number of random users
        """
        response = self.db.fetch_all(
            f"""
               SELECT *
               FROM user_details
               ORDER BY RANDOM()
               LIMIT {quantity};
           """
        )
        return response

    def create_user(self, user: dict) -> None:
        """Inserting user into database


        Args:
            user: user data:
                - id - user of id;
                - first_name - first name of user;
                - last_name - last name of user;
                - email - email of user;
                - password - password for user;
                - hashed_password - hash of password for user.
        """
        self.db.execute(
            f"""
               INSERT INTO public.user_details(id
                   , first_name
                   , last_name
                   , stripe_customer_token
                   , birth_date
                   , phone_number
                   , email
                   , password
                   , address_id
                   , account_non_expired
                   , account_non_locked
                   , credentials_non_expired
                   , enabled
               )
               VALUES ('{user["id"]}'
                   , '{user["first_name"]}'
                   , '{user["last_name"]}'
                   , '{user["stripe_customer_token"]}'
                   , '{user["birth_date"]}'
                   , '{user["phone_number"]}'
                   , '{user["email"]}'
                   , '{user["hashed_password"]}'
                   , null
                   , true
                   , true
                   , true
                   , true
               );
           """
        )

    def create_random_users(self, quantity: int = 1) -> List[dict]:
        """Creating random user(s)


        Args:
            quantity: number of random users
        """
        users = [self.create_user(generate_user()) for _ in range(quantity)]

        return users

    def delete_user(self, user_id: str) -> None:
        """Deletes a user from the database based on user ID


        Args:
            user_id: user ID
        """
        delete_query = f"DELETE FROM public.user_details WHERE id = '{user_id}';"
        self.db.execute(delete_query)

    def select_user_by_email(self, email) -> Optional[List[dict]]:
        """Search user by email in BD


        Args:
            email: user's email
        """
        select_query = f"SELECT COUNT(*) FROM user_details WHERE email = '{email}'"
        return self.db.fetch_all(select_query)

    # Additional methods would continue here...


# Example usage:
# db = PostgresDB()
# users = db.get_random_users(5)
# db.close()
