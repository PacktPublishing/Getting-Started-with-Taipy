import os

import pandas as pd
from sqlalchemy import create_engine

# Parameters:
username = "postgres"
password = os.getenv("postgres")
host = "localhost"
port = "5432"
database = "adventure_works_dw"


def create_connector(username, password, host, port, database):
    # SQLAlchemy connection string
    connection_string = (
        f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
    )

    engine = create_engine(connection_string)
    return engine


connector = create_connector(
    username=username,
    password=password,
    host=host,
    port=port,
    database=database,
)


def sql_to_df(query, connector=connector):
    df = pd.read_sql_query(query, con=connector)
    return df
