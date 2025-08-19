# Alternative Version - Analyze Data

The app for Chapter 12 uses Spark and AWS S3 storage. To give options to all readers, we created an app that downloads the files from and S3 bucket and then processes them. This way, it's easier for readers that don't want to set up an AWS account or an S3 bucket to change the app to use local files directly.

While downloading files locally may make sense for some use cases (if the app reads them often for example), you can also use Spark to read directly from the S3 bucket (and write to it).

This directory has an alternative app that doesn't download data from the S3 bucket prior to using Spark, instead, it lets Spark read directly from S3 and then writes locally. The rest of the pipeline is the same, with Dask creating the aggregations (refer to the book's Chapter for context).

## Main changes

Here are the changes we did to the app to read from an S3 instead of downloading data directly:

1. We removed the `download_nyc_tlc.py` file, and we removed all the imports of the `read_s3` function
2. We removed the `check_spark_data_node_config` Data Node configuration file, and the `download_task` from te `config.py` file
3. We remove the `check_download` from the `run_spark_processing` function (and the `if` condition statement at the begining of the function)
4. In `process_nyc_tlc.py`, we change the `data_folder` value to add the S3 path: `"s3a://taipy-nyc-tlc-trip-data"`. We also change the reading function in `spark_process_nyc_tlc.py` to remove the `os.path` function, since the S3 path isn't a file system path:

```python
def read_nyc_tlc_df(file_path: str, spark):
    try:
        df = spark.read.parquet(file_path)
        return df.toDF(*[c.lower() for c in df.columns])
    except Exception as e:
        print(f"File not found or error reading {file_path}: {e}")
        return None
```

5. In `process_nyc_tlc.py`, we add the packages Spark needs to interact with the S3 bucket, these are version specific, so you may need to change it, this is how we set it up for ours:

```python
"--packages",
"org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.367",
"--conf",
"spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem",
"--conf",
"spark.hadoop.fs.s3a.aws.credentials.provider=com.amazonaws.auth.EnvironmentVariableCredentialsProvider",
```

6. In `spark_process_nyc_tlc.py`, we need to change the configuration to the `SparkSession` object. Specifically, we add the configuration for Spark to use the S3 remote file system, and the configuration to log into our AWS account:

```python
spark = (
    SparkSession.builder.appName("NYC TLC Processing")
    .config("spark.sql.shuffle.partitions", "400")
    .config("spark.default.parallelism", "8")
    # ADD THESE LINES for S3 configuration!
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "com.amazonaws.auth.EnvironmentVariableCredentialsProvider",
    )
    .getOrCreate()
)
```

> **Important**
> This AWS cnfiguration expects your envirnoment variables to be like this (for the other versions of the app as well):
> 
```bash
export AWS_ACCESS_KEY_ID="YOUR-KEY"
export AWS_SECRET_ACCESS_KEY="YOUR/API/KEY"
```

## Possibilities are Endless

You can use Spark to write to the S3 bucket, and you can read, and write to the S3 bucket using Dask as well as other libraries; you can also use Taipy's S3 Data Nodes (although, they generate pandas DataFrames).

Your can use Taipy with almost any setup.
