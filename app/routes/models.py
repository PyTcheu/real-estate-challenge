from fastapi import APIRouter, HTTPException
from app.schemas.model_schemas import ModelInput
from app.services.model_manager import Model, ModelRegistry
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize model registry
MODEL_REGISTRY_PATH = "app/model_registry/model_registry.csv"
model_registry = ModelRegistry(MODEL_REGISTRY_PATH)

@router.post("/")
def create_or_update_model(input_data: ModelInput):
    """
    Create or update a model. Automatically increments the version.
    """
    try:
        model_id = input_data.model_id
        model_name = input_data.model_name
        features_list = input_data.features
        author = input_data.author
        pickle_path = input_data.pickle_path

        next_version = model_registry.get_next_version(model_id)

        # Create and save the model
        model = Model(model_id=model_id, model_name=model_name, version=next_version, features=features_list, author=author, pickle_path=pickle_path)
        model.save()
        model_registry.add_entry(model)

        return {"message": f"Model {model_id} version {next_version} created successfully."}
    except Exception as e:
        logger.exception("Error creating or updating model.")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/latest/{model_id}")
def get_latest_model_version(model_id: str):
    """
    Get the latest version of a given model id.
    """
    try:
        latest_model = model_registry.get_latest_version(model_id)
        if not latest_model:
            raise HTTPException(status_code=404, detail=f"No model found with id {model_id}")
        return latest_model
    except Exception as e:
        logger.exception("Error retrieving latest model version.")
        raise HTTPException(status_code=500, detail=str(e))