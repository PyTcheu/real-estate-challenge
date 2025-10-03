from fastapi import FastAPI
from app.routes import models, predictions
from app.utils.logger import configure_logging

# Configure logging
configure_logging()

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(models.router, prefix="/models", tags=["Models"])
app.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])