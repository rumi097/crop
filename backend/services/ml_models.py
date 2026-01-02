import os

from models.crop_recommendation import CropRecommendationModel
from models.fertilizer_recommendation import FertilizerRecommendationModel


crop_model = None
fertilizer_model = None


def load_models():
    """Load ML models used across portals (crop & fertilizer)."""
    global crop_model, fertilizer_model

    try:
        if crop_model is None:
            crop_model = CropRecommendationModel()
            if os.path.exists('saved_models/crop_model.pkl'):
                crop_model.load_model()
                print("\u2713 Crop model loaded")
            else:
                print("\u26a0 Crop model not found")

        if fertilizer_model is None:
            fertilizer_model = FertilizerRecommendationModel(use_ml=False)
            print("\u2713 Fertilizer model initialized")

    except Exception as e:
        print(f"Error loading models: {str(e)}")
