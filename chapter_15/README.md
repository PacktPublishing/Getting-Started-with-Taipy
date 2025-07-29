# Chapter 15: Exploring Taipy Designer (Enterprise Version)

- [Chapter 15: Exploring Taipy Designer (Enterprise Version)](#chapter-15-exploring-taipy-designer-enterprise-version)
  - [Taipy-Designer Installation](#taipy-designer-installation)
  - [Unit converter app](#unit-converter-app)
  - [Cities App](#cities-app)
    - [Data](#data)

In this chapter, we discover how to use Taipy Designer.

## Taipy-Designer Installation

We cover the installation process in the book, you need to create a new environment and `pip install .` the file sent by Taipy's team. This will also install Taipy. For this reason, we don't provide a `requirements.txt`. The app also uses GeoPandas and Matplotlib, you'll need to install them as well.

## Unit converter app

We start creating a unit converter app, the goal is to discover the basic workflows of Taipy Designer:

![GIF Screen record of Taipy converter app](img/conver_app.gif)

## Cities App

We create a small demonstration app with world cities. The app displays the top 10 cities for a given country (or "All" countries, or all capitals). The app displays a table, a leaflet map and a matplotlib bar chart. The app also shows two metric cards:

- The total city population for a given selection (the top 10 of a country, capitals, or whole world)
- And the percentage of total population for that selection

![GIF screen recording of Taipy Designer app](img/cities.gif)

### Data

The dataset comes from [Simplemaps](https://simplemaps.com/data/world-cities) (many thanks to them).
