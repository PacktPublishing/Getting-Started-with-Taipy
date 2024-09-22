import pandas as pd
import taipy as tp
from taipy import Config, Core, Scope

## 1.1 Configure a SQL TABLE Data Node ##

cities_postgresql_table_node_config = Config.configure_sql_table_data_node(
    id="most_populated_cities_postgresql_table",
    db_username="postgres",
    db_password="your-password",
    db_port="5432",
    db_name="cities",
    db_engine="postgresql",
    table_name="CITIES",
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


cities_postgresql_node_config = Config.configure_sql_data_node(
    id="most_populated_cities_postgresql",
    db_username="postgres",
    db_password="your-password",
    db_port="5432",
    db_name="cities",
    db_engine="postgresql",
    read_query=cities_and_countries_query,
    write_query_builder=create_cities,
    scope=Scope.GLOBAL,
)

core = Core()
core.run()

# 2.1 Create a data node from the a config file SQL table
cities_postgresql_table_data_node = tp.create_global_data_node(
    cities_postgresql_table_node_config
)
df_cities = cities_postgresql_table_data_node.read()

print("Data from a postgresql file table:")
print(df_cities.head(10))

# 2.2 Create a data node from the a config file with a SQL query:
cities_postgresql_data_node = tp.create_global_data_node(cities_postgresql_node_config)
df_cities_with_countries = cities_postgresql_data_node.read()

print("Data from a postgresql file and complex query:")
print(df_cities_with_countries.head(10))
