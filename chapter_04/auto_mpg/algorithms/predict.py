import pandas as pd


def create_prediction_dataframe(
    list_columns,
    prediction_cylinders,
    prediction_displacement,
    prediction_horsepower,
    prediction_weight,
    prediction_acceleration,
    prediction_model_year,
    prediction_origin,
):
    """
    Creates a Pandas DataFrame with specified columns and prediction values.

    Args:
        list_columns (list): A list of column names to include in the DataFrame.
        prediction_cylinders (int): The predicted value for the "cylinders" column.
        prediction_displacement (float): The predicted value for the "displacement" column.
        prediction_horsepower (int): The predicted value for the "horsepower" column.
        prediction_weight (int): The predicted value for the "weight" column.
        prediction_acceleration (float): The predicted value for the "acceleration" column.
        prediction_model_year (int): The predicted value for the "model_year" column.
        prediction_origin (int): The predicted value for the "origin" column.

    Returns:
        pd.DataFrame: A DataFrame with the specified columns and prediction values.
    """

    prediction_data = {}
    for column in list_columns:
        if column == "cylinders":
            prediction_data[column] = prediction_cylinders
        elif column == "displacement":
            prediction_data[column] = prediction_displacement
        elif column == "horsepower":
            prediction_data[column] = prediction_horsepower
        elif column == "weight":
            prediction_data[column] = prediction_weight
        elif column == "acceleration":
            prediction_data[column] = prediction_acceleration
        elif column == "model year":
            prediction_data[column] = prediction_model_year
        elif column == "origin":
            prediction_data[column] = prediction_origin

    # Create a DataFrame from the prediction data
    prediction_df = pd.DataFrame(prediction_data, index=[0])

    return prediction_df


def make_predictions(model, new_data, scaler):
    """Makes predictions on new data.
    Uses the scaler from the training process"""
    new_data_scaled = scaler.transform(new_data)
    predictions = model.predict(new_data_scaled)

    print(predictions)
    return predictions
