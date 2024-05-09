from typing import List, Optional

from framework.clients.db_client_ssh import DBClient as RemoteDBClient
from framework.clients.db_client import DBClient as LocalDBClient
from framework.tools.generators import generate_user


class PostgresDB:
    def __init__(
        self,
        remote: bool = False,
        ssh_username: Optional[str] = None,
        ssh_password: Optional[str] = None,
        local_server_ip: Optional[str] = None,
        remote_server_ip: Optional[str] = None,
        db_username: Optional[str] = None,
        db_password: Optional[str] = None,
        database_name: Optional[str] = None,
        port_ssh: Optional[int] = None,
    ):
        """
        Initializes the database connection.

        Args:
            remote: Whether to connect to a remote database (default: False).
            ssh_username: SSH server username.
            ssh_password: SSH server password.
            local_server_ip: IP address of local Postgres server.
            remote_server_ip: IP address of remote SSH server.
            db_username: Database username.
            db_password: Database password.
            database_name: Name of the database to connect.
            port_ssh: SSH server port.
        """
        self.remote = remote
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.local_server_ip = local_server_ip
        self.remote_server_ip = remote_server_ip
        self.db_username = db_username
        self.db_password = db_password
        self.database_name = database_name
        self.port_ssh = port_ssh
        self.db = None

        self._connect()

    def _connect(self):
        """Establishes the database connection based on the connection type."""
        if self.remote:
            self.db = RemoteDBClient(
                ssh_username=self.ssh_username,
                ssh_password=self.ssh_password,
                local_server_ip=self.local_server_ip,
                db_username=self.db_username,
                db_password=self.db_password,
                database_name=self.database_name,
                remote_server_ip=self.remote_server_ip,
                port_ssh=self.port_ssh,
            )
        else:
            self.db = LocalDBClient(
                dbname=self.database_name,
                host=self.local_server_ip,
                port=self.port_ssh,
                user=self.db_username,
                password=self.db_password,
            )

    def close(self) -> None:
        """Close the database connection"""
        self.db.close()

    def get_data_by_filter(
        self, table: str, field: str, value: str
    ) -> Optional[List[dict]]:
        """Getting data from table by filter field and its value

        Args:
            table: table in database;
            field: field of table;
            value: field value.
        """
        response = self.db.fetch_all(
            """
                SELECT *
                FROM {}
                WHERE {} = %s;
            """.format(
                table, field
            ),
            (value,),
        )

        return response

    def get_random_products(self, quantity: int = 1) -> Optional[List[dict]]:
        """Getting a random product

        Args:
            quantity: number of random products
        """
        response = self.db.fetch_all(
            """
                SELECT *
                FROM product
                WHERE active = true
                ORDER BY RANDOM()
                LIMIT %s;
            """,
            (quantity,),
        )
        return response

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
            response += " LIMIT %s"
        if page >= 0:
            response += " OFFSET %s"
        return self.db.fetch_all(response, (size, size * page))

    def get_random_users(self, quantity: int = 1) -> List[dict]:
        """Getting a random user

        Args:
            quantity: number of random users
        """
        response = self.db.fetch_all(
            """
                SELECT *
                FROM user_details
                ORDER BY RANDOM()
                LIMIT %s;
            """,
            (quantity,),
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
            """
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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, null, true, true, true, true);
            """,
            (
                user["id"],
                user["first_name"],
                user["last_name"],
                user["stripe_customer_token"],
                user["birth_date"],
                user["phone_number"],
                user["email"],
                user["hashed_password"],
            ),
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
        delete_query = "DELETE FROM public.user_details WHERE id = %s;"
        self.db.execute(delete_query, (user_id,))

    def select_user_by_email(self, email) -> Optional[List[dict]]:
        """Search user by email in BD

        Args:
            email: user's email
        """
        select_query = "SELECT COUNT(*) FROM user_details WHERE email = %s"
        return self.db.fetch_all(select_query, (email,))
