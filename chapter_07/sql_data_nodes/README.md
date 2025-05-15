# Setting SQL Data Nodes

This chapter's app uses Parquet files, which we generate from a PostgreSQL database. We made this choice for two reasons:

- Parquet files are a great way to handle analytical data, and we wanted the book to have an app that uses them.
    
- Database systems are harder to implement for the average reader. There is also a great diversity of DBMS, so some users might not want to use PostgreSQL because they already have a different database. We chose a PostgreSQL database because it's free and open source, and therefore accessible. However, some users may not want to deal with installing PostgreSQL or getting it from an online service.
    

 But... Some readers would probably like to test the application by connecting directly to the database. We decided to create a separate directory (this one!) to set up all the configuration files to use the database directly. We won't explain the Data Node configuration in detail (you can refer to Chapter 3), nor the app's context (you can see that in Chapter 7).

 ## How to use these files

First, make sure your database is up and running. For this, you can follow the steps in the notebook, which you'll find in `pre_process/select_data.ipynb`. If the notebook runs without errors, then the Data Nodes should work too.

You need to replace the `config.py` file in the app's `configuration` directory. You also need to move the `.sql` files that the SQL Data Nodes use to read the data from the database.

 ## Considerations

While we won't cover the details of the configuration file, here are some important considerations:

* Notice how the `sales` and `items` columns in the SQL queries have forced types (we use the `::int` and `::float` syntax). This is important so our pandas DataFrame doesn't end up having `object` types, which would interfere with the forecasting model.
    
* In `config.py`, we create a placeholder function called `dont_write_anything` to pass to the `write_query_builder` mandatory argument (this is an element that might get improved in future versions of Taipy: allowing the SQL Data Node to have one method to either read or write instead of forcing both). Here is the function that does the trick:

 ```python
def dont_write_anything():
    pass
```
