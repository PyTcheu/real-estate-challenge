import json
import pathlib
import pickle
from typing import List, Tuple
import pandas as pd
from sklearn import model_selection, neighbors, pipeline, preprocessing
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

SALES_PATH = "data/kc_house_data.csv"
DEMOGRAPHICS_PATH = "data/zipcode_demographics.csv"  # optional for future
OUTPUT_DIR = "new_model/"

SALES_COLUMN_SELECTION = [
    'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
    'sqft_above', 'sqft_basement', 'zipcode'
]

ALL_FEATURES = [
    'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
    'waterfront', 'view', 'condition', 'grade', 'sqft_above', 'sqft_basement',
    'yr_built', 'yr_renovated', 'zipcode', 'lat', 'long',
    'sqft_living15', 'sqft_lot15'
]

def load_data(path: str, features: List[str], demographics_path: str = DEMOGRAPHICS_PATH) -> Tuple[pd.DataFrame, pd.Series]:
    """Load home sale data and merge with demographics by zipcode."""
    data = pd.read_csv(path, usecols=features, dtype={'zipcode': str})
    demographics = pd.read_csv(demographics_path, dtype={'zipcode': str})

    # Merge on zipcode
    merged_data = data.merge(demographics, how="left", on="zipcode")
    merged_data = merged_data.drop(columns="zipcode")  # Drop zipcode after merge

    # Separate target
    y = merged_data.pop('price')
    x = merged_data
    return x, y

def train_models(x_train, x_test, y_train, y_test, feature_set_name):
    """Trains KNN, RandomForest, GradientBoosting, XGBoost and returns metrics."""
    models = {
        "KNR": neighbors.KNeighborsRegressor(),
        "RandomForest": RandomForestRegressor(n_estimators=200, max_depth=None, random_state=42, n_jobs=-1),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
        "XGBoost": XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1, tree_method="hist")
    }

    metrics_list = []

    for name, model_obj in models.items():
        pipe = pipeline.make_pipeline(preprocessing.RobustScaler(), model_obj)
        pipe.fit(x_train, y_train)
        y_pred = pipe.predict(x_test)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        metrics_list.append({
            "Model": name,
            "Feature_Set": feature_set_name,
            "MAE": mae,
            "MSE": mse,
            "R2": r2
        })

    return metrics_list

def main():
    all_metrics = []

    # Sales subset features
    x, y = load_data(SALES_PATH, SALES_COLUMN_SELECTION)
    x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, random_state=42)
    all_metrics += train_models(x_train, x_test, y_train, y_test, "Sales_Subset")

    # All features selections
    x_all, y_all = load_data(SALES_PATH, ALL_FEATURES)
    x_train_all, x_test_all, y_train_all, y_test_all = model_selection.train_test_split(x_all, y_all, random_state=42)
    all_metrics += train_models(x_train_all, x_test_all, y_train_all, y_test_all, "All_Features")

    # Display of the final table after training
    metrics_df = pd.DataFrame(all_metrics)
    print("\n=== Model Comparison ===")
    print(metrics_df.pivot(index="Model", columns="Feature_Set", values=["MAE","MSE","R2"]))

    # save training results into a CSV file
    metrics_df.to_csv(pathlib.Path(OUTPUT_DIR) / "training_metrics.csv", index=False)

    # Code for selecting and saving the best model as artifacts
    best_row = metrics_df.sort_values("R2", ascending=False).iloc[0]
    best_feature_set = SALES_COLUMN_SELECTION if best_row["Feature_Set"] == "Sales_Subset" else ALL_FEATURES
    x_best, y_best = load_data(SALES_PATH, best_feature_set)
    x_train, x_test, y_train, y_test = model_selection.train_test_split(x_best, y_best, random_state=42)
    
    # Save the best model as an artifact
    if best_row["Model"] == "KNN":
        best_model_obj = neighbors.KNeighborsRegressor()
    elif best_row["Model"] == "RandomForest":
        best_model_obj = RandomForestRegressor(n_estimators=200, max_depth=None, random_state=42, n_jobs=-1)
    elif best_row["Model"] == "GradientBoosting":
        best_model_obj = GradientBoostingRegressor(n_estimators=100, random_state=42)
    else:
        best_model_obj = XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1, tree_method="hist")

    best_pipe = pipeline.make_pipeline(preprocessing.RobustScaler(), best_model_obj)
    best_pipe.fit(x_train, y_train)

    # Save artifacts
    output_dir = pathlib.Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    pickle.dump(best_pipe, open(output_dir / "new_model.pkl", "wb"))
    json.dump(list(x_train.columns), open(output_dir / "model_features.json", "w"))

if __name__ == "__main__":
    main()