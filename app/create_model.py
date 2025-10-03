import json
import pathlib
import pickle
from typing import List
from typing import Tuple

import pandas
from sklearn import model_selection
from sklearn import neighbors
from sklearn import pipeline
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

SALES_PATH = "data/kc_house_data.csv"  # path to CSV with home sale data
DEMOGRAPHICS_PATH = "data/kc_house_data.csv"  # path to CSV with demographics
# List of columns (subset) that will be taken from home sale data
SALES_COLUMN_SELECTION = [
    'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
    'sqft_above', 'sqft_basement', 'zipcode'
]
OUTPUT_DIR = "model"  # Directory where output artifacts will be saved


def load_data(
    sales_path: str, demographics_path: str, sales_column_selection: List[str]
) -> Tuple[pandas.DataFrame, pandas.Series]:
    """Load the target and feature data by merging sales and demographics.

    Args:
        sales_path: path to CSV file with home sale data
        demographics_path: path to CSV file with home sale data
        sales_column_selection: list of columns from sales data to be used as
            features

    Returns:
        Tuple containg with two elements: a DataFrame and a Series of the same
        length.  The DataFrame contains features for machine learning, the
        series contains the target variable (home sale price).

    """
    data = pandas.read_csv(sales_path,
                           usecols=sales_column_selection,
                           dtype={'zipcode': str})
    demographics = pandas.read_csv("data/zipcode_demographics.csv",
                                   dtype={'zipcode': str})

    merged_data = data.merge(demographics, how="left",
                             on="zipcode").drop(columns="zipcode")
    # Remove the target variable from the dataframe, features will remain
    y = merged_data.pop('price')
    x = merged_data

    return x, y


def main():
    """Load data, train model, and export artifacts."""
    x, y = load_data(SALES_PATH, DEMOGRAPHICS_PATH, SALES_COLUMN_SELECTION)
    x_train, _x_test, y_train, _y_test = model_selection.train_test_split(
        x, y, random_state=42)

    print("Training with KNN Regression")
    model = pipeline.make_pipeline(preprocessing.RobustScaler(),
                                   neighbors.KNeighborsRegressor()).fit(
                                       x_train, y_train)
    
    # Evaluate on test set
    y_pred = model.predict(_x_test)
    print("KNR MAE:", mean_absolute_error(_y_test, y_pred))
    print("KNR MSE:", mean_squared_error(_y_test, y_pred))
    print("KNR R2:", r2_score(_y_test, y_pred))

    # Train model with random forest regression
    print("Training with Random Forest Regression")
    rf_model = pipeline.make_pipeline(
        preprocessing.RobustScaler(),
        RandomForestRegressor(n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=2)
    ).fit(x_train, y_train)

    # Evaluate on test set
    y_pred_rf = rf_model.predict(_x_test)
    print("Random Forest MAE:", mean_absolute_error(_y_test, y_pred_rf))
    print("Random Forest MSE:", mean_squared_error(_y_test, y_pred_rf))
    print("Random Forest R2:", r2_score(_y_test, y_pred_rf))

    # Train model with gradient boosting regression
    print("Training with Gradient Boosting Regression")

    gb_model = pipeline.make_pipeline(
        preprocessing.RobustScaler(),
        GradientBoostingRegressor(n_estimators=100, random_state=42)
    ).fit(x_train, y_train)

    # Evaluate on test set
    y_pred_gb = gb_model.predict(_x_test)
    print("Gradient Boosting MAE:", mean_absolute_error(_y_test, y_pred_gb))
    print("Gradient Boosting MSE:", mean_squared_error(_y_test, y_pred_gb))
    print("Gradient Boosting R2:", r2_score(_y_test, y_pred_gb))

    print("Training with XGBoost Regression")
    xgb_model = pipeline.make_pipeline(
        preprocessing.RobustScaler(),
        XGBRegressor(n_estimators=100, random_state=42, n_jobs=2)
    ).fit(x_train, y_train)

    # Evaluate on test set
    y_pred_xgb = xgb_model.predict(_x_test)
    print("XGBoost MAE:", mean_absolute_error(_y_test, y_pred_xgb))
    print("XGBoost MSE:", mean_squared_error(_y_test, y_pred_xgb))
    print("XGBoost R2:", r2_score(_y_test, y_pred_xgb))

    output_dir = pathlib.Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    # Output model artifacts: pickled model and JSON list of features
    pickle.dump(model, open(output_dir / "model.pkl", 'wb'))
    json.dump(list(x_train.columns),
              open(output_dir / "model_features.json", 'w'))

if __name__ == "__main__":
    main()
