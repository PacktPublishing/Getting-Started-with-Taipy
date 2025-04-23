import taipy as tp
import taipy.gui.builder as tgb
from taipy import Config, Orchestrator, Scope
from taipy.gui import Gui

#################### GLOBAL DATA NODES using PARQUET FILES #########################################
###    Uncomment this and comment the S3 configuration objects if you want to work locally       ###
###    12 month configuration - 1 per parquet file                                               ###
####################################################################################################

month_1_node_config = Config.configure_parquet_data_node(
    id="month_1",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-01.parquet",
)
month_2_node_config = Config.configure_parquet_data_node(
    id="month_2",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-02.parquet",
)
month_3_node_config = Config.configure_parquet_data_node(
    id="month_3",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-03.parquet",
)
month_4_node_config = Config.configure_parquet_data_node(
    id="month_4",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-04.parquet",
)
month_5_node_config = Config.configure_parquet_data_node(
    id="month_5",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-05.parquet",
)
month_6_node_config = Config.configure_parquet_data_node(
    id="month_6",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-06.parquet",
)
month_7_node_config = Config.configure_parquet_data_node(
    id="month_7",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-07.parquet",
)
month_8_node_config = Config.configure_parquet_data_node(
    id="month_8",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-08.parquet",
)
month_9_node_config = Config.configure_parquet_data_node(
    id="month_9",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-09.parquet",
)
month_10_node_config = Config.configure_parquet_data_node(
    id="month_10",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-10.parquet",
)
month_11_node_config = Config.configure_parquet_data_node(
    id="month_11",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-11.parquet",
)
month_12_node_config = Config.configure_parquet_data_node(
    id="month_12",
    scope=Scope.GLOBAL,
    default_path="./data/raw_data/yellow_tripdata_2023-12.parquet",
)


#################### GLOBAL DATA NODES using an S3 bucket ##########################################
###    Uncomment this and comment the previous Parquet configuration objects if you want S3      ###
###    12 month configuration - 1 per S3 parquet file                                            ###
####################################################################################################


# aws_access_key_id= os.environ.get("AWS_ACCESS_KEY_ID")
# aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
# region_name='us-east-1'

# month_1_node_config = Config.configure_s3_object_data_node(
#     id="month_1",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-01.parquet",
#     scope=Scope.GLOBAL,
# )
# month_2_node_config = Config.configure_s3_object_data_node(
#     id="month_2",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-02.parquet",
#     scope=Scope.GLOBAL,
# )
# month_3_node_config = Config.configure_s3_object_data_node(
#     id="month_3",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-03.parquet",
#     scope=Scope.GLOBAL,
# )
# month_4_node_config = Config.configure_s3_object_data_node(
#     id="month_4",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-04.parquet",
#     scope=Scope.GLOBAL,
# )
# month_4_node_config = Config.configure_s3_object_data_node(
#     id="month_4",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-4.parquet",
#     scope=Scope.GLOBAL,
# )
# month_5_node_config = Config.configure_s3_object_data_node(
#     id="month_5",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-05.parquet",
#     scope=Scope.GLOBAL,
# )
# month_6_node_config = Config.configure_s3_object_data_node(
#     id="month_6",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-06.parquet",
#     scope=Scope.GLOBAL,
# )
# month_7_node_config = Config.configure_s3_object_data_node(
#     id="month_7",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-07.parquet",
#     scope=Scope.GLOBAL,
# )
# month_8_node_config = Config.configure_s3_object_data_node(
#     id="month_8",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-08.parquet",
#     scope=Scope.GLOBAL,
# )
# month_9_node_config = Config.configure_s3_object_data_node(
#     id="month_9",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-09.parquet",
#     scope=Scope.GLOBAL,
# )
# month_10_node_config = Config.configure_s3_object_data_node(
#     id="month_10",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-10.parquet",
#     scope=Scope.GLOBAL,
# )
# month_11_node_config = Config.configure_s3_object_data_node(
#     id="month_11",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-11.parquet",
#     scope=Scope.GLOBAL,
# )
# month_12_node_config = Config.configure_s3_object_data_node(
#     id="month_12",
#     aws_access_key=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_region = region_name,
#     aws_s3_bucket_name="taipy-nyc-tlc-trip-data",
#     aws_s3_object_key="yellow_tripdata_2023-12.parquet",
#     scope=Scope.GLOBAL,
# )


with tgb.Page() as read_page:
    tgb.text("# Reading some files!", mode="md")

    tgb.selector(
        value="{selected_month}",
        lov=list(range(1, 13)),
        on_change=lambda state: state.assign(
            "selected_month_node", select_node(int(state.selected_month))
        ),
        dropdown=True,
    )  # Comment this to use S3
    # on_change=lambda state: state.assign("df_selected_month",
    #                                       select_node(int(state.selected_month))),
    #  dropdown=True) #Uncomment this to use S3

    tgb.data_node("{selected_month_node}")  # Comment this to use S3
    # tgb.table("{df_selected_month}", rebuild=True) #Uncomment this to use S3

if __name__ == "__main__":

    Orchestrator().run()

    selected_month = 1
    month_data = {
        1: tp.create_global_data_node(month_1_node_config),
        2: tp.create_global_data_node(month_2_node_config),
        3: tp.create_global_data_node(month_3_node_config),
        4: tp.create_global_data_node(month_4_node_config),
        5: tp.create_global_data_node(month_5_node_config),
        6: tp.create_global_data_node(month_6_node_config),
        7: tp.create_global_data_node(month_7_node_config),
        8: tp.create_global_data_node(month_8_node_config),
        9: tp.create_global_data_node(month_9_node_config),
        10: tp.create_global_data_node(month_10_node_config),
        11: tp.create_global_data_node(month_11_node_config),
        12: tp.create_global_data_node(month_12_node_config),
    }

    def select_node(selected_month):
        selected_month_node = month_data.get(selected_month)
        return selected_month_node  # Comment this to use S3
        # parquet_file = BytesIO(selected_month_node.read()) #Uncomment this and below to use S3
        # df_month = pd.read_parquet(parquet_file)
        # return df_month

    selected_month_node = select_node(selected_month)  # Comment this to use S3
    # df_selected_month = select_node(selected_month)  # Uncomment this to use S3

    gui = Gui(page=read_page)

    gui.run(dark_mode=False, use_reloader=True)
