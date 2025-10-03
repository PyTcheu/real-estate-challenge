from pydantic import BaseModel
from typing import List

class ModelInput(BaseModel):
    model_id: str
    model_name: str
    features: List[str]
    author: str
    pickle_path: str