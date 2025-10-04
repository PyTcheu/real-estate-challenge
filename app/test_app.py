# Load data from a file
import requests
import pandas as pd
import json

# Create new model via api

requests.post("http://127.0.0.1:5000/models/", json={
    "model_id": "real_estate_model",
    "model_name": "Real Estate Price Predictor",
    "features": ["bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "sqft_above", "sqft_basement", "ppltn_qty", "urbn_ppltn_qty", "sbrbn_ppltn_qty", "farm_ppltn_qty", "non_farm_qty", "medn_hshld_incm_amt", "medn_incm_per_prsn_amt", "hous_val_amt", "edctn_less_than_9_qty", "edctn_9_12_qty", "edctn_high_schl_qty", "edctn_some_clg_qty", "edctn_assoc_dgre_qty", "edctn_bchlr_dgre_qty", "edctn_prfsnl_qty", "per_urbn", "per_sbrbn", "per_farm", "per_non_farm", "per_less_than_9", "per_9_to_12", "per_hsd", "per_some_clg", "per_assoc", "per_bchlr", "per_prfsnl"],
    "author": "John Doe",
    "pickle_path": "app/model/model.pkl"})

data_unseen = pd.read_csv("data/future_unseen_examples.csv")
with open("model/model_features.json", "r") as features_file:
    model_features = json.load(features_file)

# Make predictions and print results and API status codes
url = "http://127.0.0.1:5000/predictions/real_estate_model"

sample = data_unseen
for i, row in sample.iterrows():
    input_data = row.to_dict()

    # Ensure zipcode is a string
    input_data["zipcode"] = str(int(input_data["zipcode"]))
    
    response = requests.post(url, json=input_data)
    print("Price estimated:", response.json()['prediction'])  


# Create new model with all features

with open("new_model/model_features.json", "r") as features_file:
    model_features = json.load(features_file)

requests.post("http://127.0.0.1:5000/models/", json={
    "model_id": "real_estate_model_all_features",
    "model_name": "Real Estate Price Predictor with All Features",
    "features": model_features,
    "author": "John Doe",
    "pickle_path": "app/new_model/new_model.pkl"})

data_unseen = pd.read_csv("data/future_unseen_examples.csv")

with open("new_model/model_features.json", "r") as features_file:
    model_features = json.load(features_file)

# Make predictions and print results and API status codes
url = "http://127.0.0.1:5000/predictions/all_features/real_estate_model_all_features"

for i, row in data_unseen.iterrows():
    input_data = row.to_dict()

    # Ensure zipcode is a string
    input_data["zipcode"] = str(int(input_data["zipcode"]))
    
    response = requests.post(url, json=input_data)
    print("Price estimated with all features:", response.json()['prediction'])