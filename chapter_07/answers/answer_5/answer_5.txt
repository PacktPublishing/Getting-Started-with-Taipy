############################################################
## Answer 5                                               ##
## To add a data_node element instead of a table to       ##
## display results, follow these steps in forecast.py     ##
############################################################

# Add a selected_data_node_results variable, initial value can be None:
selected_data_node_results = None

# Add the Data Node element:
tgb.data_node(data_node="{selected_data_node_results}")

# update the value in the Callbacks, like this:
state.selected_data_node_results = state.selected_scenario.forecast_df
# Or like this if the Data Node isn't written:
state.selected_data_node_results = None
