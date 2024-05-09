import psycopg2
import sshtunnel

from configs import (
    database_name,
    db_username,
    db_password,
    local_server_ip,
    remote_server_ip,
    port_ssh,
    ssh_username,
    ssh_password,
)


def connect_to_database(local=True):
    if local:
        # Connect directly to the local database
        conn = psycopg2.connect(
            dbname=database_name,
            user=db_username,
            password=db_password,
            host=local_server_ip,
            port="5432",
        )
    else:
        # Establish an SSH tunnel to the remote server
        with sshtunnel.SSHTunnelForwarder(
            (remote_server_ip, port_ssh),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            remote_bind_address=(local_server_ip, 5432),
        ) as tunnel:
            # Once the SSH tunnel is established, connect to the database
            conn = psycopg2.connect(
                dbname=database_name,
                user=db_username,
                password=db_password,
                host=tunnel.local_bind_host,
                port=tunnel.local_bind_port,
            )

    return conn
