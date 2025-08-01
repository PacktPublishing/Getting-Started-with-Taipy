# Chapter 12: Handling Large Data in Taipy Application

- [Chapter 12: Handling Large Data in Taipy Application](#chapter-12-handling-large-data-in-taipy-application)
  - [NYC taxi application](#nyc-taxi-application)
  - [Data Sources](#data-sources)

## NYC taxi application

We code a small NYC trip data application. The goal is to use distributed computing tools like Dask and Spark. The application's GUI looks like this:

![Screenshot of NYC Taxi app](./img/trip_app.png)

Here's the pipeline we code, with a pre-processing step, and several analytical processing steps:

![NYC Scenario pipeline](./img/pipeline.png)

## Data Sources

The NYC trip data application uses data from [NYC's taxi and limousine commission (TLC)](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
