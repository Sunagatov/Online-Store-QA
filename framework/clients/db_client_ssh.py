import logging
from typing import Optional, List

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from sshtunnel import SSHTunnelForwarder


class DBClient:
    def __init__(
        self,
        ssh_username: str,
        ssh_password: str,
        local_server_ip: str,
        db_username: str,
        db_password: str,
        database_name: str,
        remote_server_ip: str,
        port_ssh: int,
    ):
        """
        Initializes a database connection tunnel via SSH.

        Creates an SSH tunnel to a remote server, binds to the remote PostgresSQL port,
        and starts the SSH server, then connects to a PostgresSQL database through the tunnel.

        Args:
            ssh_username: SSH server username.
            ssh_password: SSH server password.
            local_server_ip: IP address of local Postgres server.
            db_username: Database username.
            db_password: Database password.
            database_name: Name of database to connect.
            remote_server_ip: IP address of remote SSH server.
            port_ssh: SSH server port.
        """
        # Start SSH tunnel
        self.server = SSHTunnelForwarder(
            (remote_server_ip, port_ssh),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            remote_bind_address=(local_server_ip, 5432),
            local_bind_address=("localhost", 0),  # Automatically select a free port
        )
        self.server.start()
        logging.info(
            f"SSH tunnel established. Local port: {self.server.local_bind_port}"
        )

        # Connect to PostgresSQL through the tunnel
        self.conn = connect(
            host="localhost",
            port=self.server.local_bind_port,
            dbname=database_name,
            user=db_username,
            password=db_password,
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        logging.info("Database connection established")

    def close(self) -> None:
        """Close the cursor, database connection, and SSH tunnel"""
        if self.cur:
            self.cur.close()
            logging.info("Cursor closed")
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed")
        if self.server:
            self.server.stop()
            logging.info("SSH tunnel closed")

    # def execute(self, query: str) -> None:
    #     """Execute a query to the Postgres database without returning data"""
    #     logging.debug(f"Executing query: {query}")
    #     self.cur.execute(query)
    #
    # def fetch_all(self, query: str) -> Optional[List[dict]]:
    #     """Execute a query to the Postgres database and return data as a list of dictionaries"""
    #     self.execute(query)
    #     records = self.cur.fetchall()
    #     return [dict(rec) for rec in records] if records else []
    def fetch_all(self, query: str, params: tuple = ()) -> List[tuple]:
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute(self, query: str, params: tuple = ()) -> None:
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            self.conn.commit()
