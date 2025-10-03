from fastapi import APIRouter, HTTPException
from app.schemas.prediction_schemas import PredictionInput
from app.utils.helpers import get_demographic_data
import pandas as pd
import pickle
import os
import json
import logging
from app.services.model_manager import ModelRegistry

MODEL_REGISTRY_PATH = "app/model_registry/model_registry.csv"
model_registry = ModelRegistry(MODEL_REGISTRY_PATH)

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/{model_id}")
def predict(model_id: str, input_data: PredictionInput):
    """
    Endpoint for making predictions with the latest version of a given model.
    """
    try:
        logger.info(f"Received prediction request for model ID: {model_id}")

        # Fetch the latest version of the model
        latest_model = model_registry.get_latest_version(model_id)
        if not latest_model:
            logger.error(f"No model found with ID: {model_id}")
            raise HTTPException(status_code=404, detail=f"No model found with ID: {model_id}")

        version = latest_model["version"]
        logger.info(f"Using model version: {version}")

        # Load the appropriate model and features based on the version
        model_path = os.path.join("app/model_registry/models/", model_id, version, "model_path.txt")
        features_path = os.path.join("app/model_registry/models/", model_id, version, "model_features.json")

        # Read the model path from the text file (This could be getting from the S3)
        try:
            with open(model_path, "r") as path_file:
                model_path = path_file.read().strip()
        except FileNotFoundError:
            logger.error(f"Model path file not found at path: {model_path}")
            raise HTTPException(status_code=500, detail=f"Model path file not found at path: {model_path}")

        # Load the pickle
        try:
            with open(model_path, "rb") as model_file:
                model = pickle.load(model_file)
        except FileNotFoundError:
            logger.error(f"Model file not found at path: {model_path}")
            raise HTTPException(status_code=500, detail=f"Model file not found at path: {model_path}")

        # Load the features
        try:
            with open(features_path, "r") as features_file:
                model_features = json.load(features_file)
        except FileNotFoundError:
            logger.error(f"Features file not found at path: {features_path}")
            raise HTTPException(status_code=500, detail=f"Features file not found at path: {features_path}")
        
        # Predicting after merging with demographic data
        input_dict = input_data.dict()
        input_df = pd.DataFrame([input_dict])
        zipcode = input_dict["zipcode"]
        demographic_data = get_demographic_data(zipcode)

        if demographic_data is None:
            logger.warning(f"No demographic data found for zipcode: {zipcode}")
            raise HTTPException(status_code=400, detail=f"No demographic data found for zipcode: {zipcode}")

        input_with_demographics = pd.concat([input_df, pd.DataFrame([demographic_data])], axis=1)

        missing_features = [feature for feature in model_features if feature not in input_with_demographics.columns]
        if missing_features:
            logger.error(f"Missing required features: {missing_features}")
            raise HTTPException(status_code=400, detail=f"Missing required features: {missing_features}")

        input_with_demographics = input_with_demographics[model_features]
        prediction = model.predict(input_with_demographics)
        logger.info("Prediction successful")
        return {"prediction": prediction.tolist()}

    except Exception as e:
        logger.exception("Error during prediction")
        raise HTTPException(status_code=500, detail=str(e))