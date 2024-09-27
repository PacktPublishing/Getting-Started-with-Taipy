import io

import pandas as pd
import taipy as tp
from taipy import Config, Core, Scope

cities_s3_node_config = Config.configure_s3_object_data_node(
    id="most_populated_cities_csv_from_s3",
    aws_access_key="AKIAIOSFODNN7EXAMPLE",  # Example access key
    aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",  # Example secret access key
    aws_s3_bucket_name="cities",
    aws_s3_object_key="cities.csv",
    scope=Scope.GLOBAL,
)

core = Core()
core.run()
cities_s3_data_node = tp.create_global_data_node(cities_s3_node_config)

csv_string = cities_s3_data_node.read()

print("Data from a CSV file:")
print(csv_string)

# Convert to DataFrame
df_cities = pd.read_csv(io.StringIO(csv_string))
print(df_cities.head())
