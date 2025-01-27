import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def preprocess_data(df_mpg):
    """Preprocesses the data by handling missing values and scaling features."""
    # Missing values are question marks... ?
    df_mpg = df_mpg.replace("?", pd.NA)
    df_mpg.dropna(inplace=True)

    # Separate features and target
    X = df_mpg.drop("mpg", axis=1)
    y = df_mpg["mpg"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler


def split_data(X, y):
    """Splits the data into training and testing sets."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    """Trains a linear regression model on the training data."""
    regression_model = LinearRegression()
    regression_model.fit(X_train, y_train)
    return regression_model


def evaluate_model(regression_model, X_test, y_test):
    """Evaluates
    the model's performance on the testing data."""
    y_pred = regression_model.predict(X_test)
    mse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(mse, r2)

    return mse, r2
