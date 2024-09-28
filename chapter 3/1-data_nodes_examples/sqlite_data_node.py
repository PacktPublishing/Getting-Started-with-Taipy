import pandas as pd
import taipy as tp
from taipy import Config, Core, Scope

## 1.1 Configure a SQL TABLE Data Node ##

cities_sqlite_table_node_config = Config.configure_sql_table_data_node(
    id="most_populated_cities_sqlite_table",
    db_name="cities",
    db_engine="sqlite",
    table_name="CITIES",
    sqlite_folder_path="../data",
    sqlite_file_extension=".db",
    scope=Scope.GLOBAL,
)

## 1.2 Configure a SQL Data Node, with a "complex" query

cities_and_countries_query = """SELECT 
	Ranking,
	City,
	Population,
	CountryName
FROM 
	CITIES
	JOIN COUNTRIES
		ON CITIES.CountryID = COUNTRIES.CountryID"""


def create_cities(data: pd.DataFrame):
    insert_data = data[["Ranking", "City", "CountryID", "Population"]].to_dict(
        "records"
    )
    return [
        "DELETE FROM CITIES",  # Clear the table before inserting new data
        (
            "INSERT INTO CITIES (Ranking, City, CountryID, Population) VALUES (:Ranking, :City, :CountryID, :Population)",
            insert_data,
        ),
    ]


cities_sqlite_node_config = Config.configure_sql_data_node(
    id="most_populated_cities_sqlite",
    db_name="cities",
    db_engine="sqlite",
    read_query=cities_and_countries_query,
    write_query_builder=create_cities,
    sqlite_folder_path="../data",
    sqlite_file_extension=".db",
    scope=Scope.GLOBAL,
)


core = Core()
core.run()

# 2.1 Create a data node from the a config file SQL table
cities_sqlite_table_data_node = tp.create_global_data_node(
    cities_sqlite_table_node_config
)
df_cities = cities_sqlite_table_data_node.read()

print("Data from a SQLite file table:")
print(df_cities.head(10))

# 2.2 Create a data node from the a config file with a SQL query:
cities_sqlite_data_node = tp.create_global_data_node(cities_sqlite_node_config)
df_cities_with_countries = cities_sqlite_data_node.read()

print("Data from a SQLite file and complex query:")
print(df_cities_with_countries.head(10))
