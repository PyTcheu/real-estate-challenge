import os
import json
import logging
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

MODEL_BASE_PATH = "app/model_registry/models/"

class Model:
    """
    Represents a model with its metadata and file storage.
    """
    def __init__(self, model_id: str, model_name: str, version: str, features: list, author: str, pickle_path: str):
        self.model_id = model_id
        self.model_name = model_name
        self.version = version
        self.features = features
        self.author = author
        self.pickle_path = pickle_path

    def save(self):
        """
        Save the model metadata and pickle path to the appropriate versioned folder.
        """
        version_path = os.path.join(MODEL_BASE_PATH, self.model_id, self.version)
        os.makedirs(version_path, exist_ok=True)

        # Save the pickle path as a reference
        pickle_path_file = os.path.join(version_path, "model_path.txt")
        with open(pickle_path_file, "w") as f:
            f.write(self.pickle_path)
        logger.info(f"Model pickle path saved at {pickle_path_file}")

        # Save the features as JSON
        features_path = os.path.join(version_path, "model_features.json")
        with open(features_path, "w") as f:
            json.dump(self.features, f)
        logger.info(f"Model features saved at {features_path}")



class ModelRegistry:
    """
    Manages the model registry, including metadata and versioning.
    """
    def __init__(self, registry_path: str):
        self.registry_path = registry_path

    def get_next_version(self, model_id: str) -> str:
        """
        Get the next version for a given model ID.
        """
        registry = pd.read_csv(self.registry_path)
        print(registry)
        model_versions = registry[registry["model_id"] == model_id]["version"]
        print(model_versions)
        if model_versions.empty:
            # If no versions exist for this model ID, start with v1
            return "v1"

        # Extract the numeric part of the version and find the maximum
        numeric_versions = [int(v[1:]) for v in model_versions if v.startswith("v")]
        latest_version = max(numeric_versions)
        next_version = f"v{latest_version + 1}"
        return next_version

    def add_entry(self, model: Model):
        """
        Add a new entry to the model registry.
        """
        new_entry = {
            "model_id": model.model_id,
            "model_name": model.model_name,
            "version": model.version,
            "features": json.dumps(model.features),
            "author": model.author,
            "pickle_path": model.pickle_path,
        }
        registry = pd.read_csv(self.registry_path)
        registry = pd.concat([registry, pd.DataFrame([new_entry])], ignore_index=True)
        registry.to_csv(self.registry_path, index=False)
        logger.info(f"Model {model.model_name} version {model.version} added to registry.")

    def get_latest_version(self, model_id: str):
        """
        Get the latest version of a given model name.
        """
        registry = pd.read_csv(self.registry_path)
        model_versions = registry[registry["model_id"] == model_id]
        if model_versions.empty:
            return None
        latest_version = model_versions.iloc[-1]
        return {
            "model_id": latest_version["model_id"],
            "model_name": latest_version["model_name"],
            "version": latest_version["version"],
            "features": json.loads(latest_version["features"]),
            "author": latest_version["author"],
            "pickle_path": latest_version["pickle_path"],
        }
    

class ModelRegistry:
    """
    Manages the model registry, including metadata and versioning.
    """
    def __init__(self, registry_path: str):
        self.registry_path = registry_path

    def get_next_version(self, model_id: str) -> str:
        """
        Get the next version for a given model ID.
        """
        registry = pd.read_csv(self.registry_path)
        print(registry)
        model_versions = registry[registry["model_id"] == model_id]["version"]
        print(model_versions)
        if model_versions.empty:
            # If no versions exist for this model ID, start with v1
            return "v1"

        # Extract the numeric part of the version and find the maximum
        numeric_versions = [int(v[1:]) for v in model_versions if v.startswith("v")]
        latest_version = max(numeric_versions)
        next_version = f"v{latest_version + 1}"
        return next_version

    def add_entry(self, model: Model):
        """
        Add a new entry to the model registry.
        """
        new_entry = {
            "model_id": model.model_id,
            "model_name": model.model_name,
            "version": model.version,
            "features": json.dumps(model.features),
            "author": model.author,
            "pickle_path": model.pickle_path,
        }
        registry = pd.read_csv(self.registry_path)
        registry = pd.concat([registry, pd.DataFrame([new_entry])], ignore_index=True)
        registry.to_csv(self.registry_path, index=False)
        logger.info(f"Model {model.model_name} version {model.version} added to registry.")

    def get_latest_version(self, model_id: str):
        """
        Get the latest version of a given model name.
        """
        registry = pd.read_csv(self.registry_path)
        model_versions = registry[registry["model_id"] == model_id]
        if model_versions.empty:
            return None
        latest_version = model_versions.iloc[-1]
        return {
            "model_id": latest_version["model_id"],
            "model_name": latest_version["model_name"],
            "version": latest_version["version"],
            "features": json.loads(latest_version["features"]),
            "author": latest_version["author"],
            "pickle_path": latest_version["pickle_path"],
        }