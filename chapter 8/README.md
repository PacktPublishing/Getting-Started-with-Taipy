# Chapter 8

This chapter covers the creation of an optimization app. This app allows users to visualize candidate warehouse and customer locations, so they can select the best warehouses to minimize supply cost and CO2e emissions.

The app has 4 tabs: 

* `Analysis` : Shows the raw data
* `Scenario`: Allows users to select parameters for the optimization Sceneario, run it and see the results
* `Comparison`: Allows users to compare two Scenarios, next to each other
* `Admin`: Shows all the application's Scenario elements

## Application overview

![](./img/app_1.gif)

![](./img/app_2.gif)

## Scenario pipeline

Here is how the Scenario's pipeline looks:

![](./img/pipeline.png)

## Data

To create our datasets, we asked Chat GPT to generate some JSON structures, with European cities and coordinates. We also added some random amounts for the operation costs and facility CO2e emissions, and we used `faker` to create the company names. You can find the notebook to create the data in [create_data.ipynb](create_data.ipynb), and the datasets in [the app's data directory](./src/data). Also note that you can generate new versions of the dataset to play around with the app and get different results. 