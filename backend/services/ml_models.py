import os

from models.crop_recommendation import CropRecommendationModel
from models.fertilizer_recommendation import FertilizerRecommendationModel


crop_model = None
fertilizer_model = None


def load_models():
    """Load ML models used across portals (crop & fertilizer)."""
    global crop_model, fertilizer_model

    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    saved_models_dir = os.path.join(backend_dir, "saved_models")
    os.makedirs(saved_models_dir, exist_ok=True)

    crop_model_path = os.path.join(saved_models_dir, "crop_model.pkl")
    crop_scaler_path = os.path.join(saved_models_dir, "crop_scaler.pkl")

    try:
        if crop_model is None:
            crop_model = CropRecommendationModel()
            if os.path.isfile(crop_model_path) and os.path.isfile(crop_scaler_path):
                crop_model.load_model(model_path=crop_model_path, scaler_path=crop_scaler_path)
                print("\u2713 Crop model loaded")
            else:
                print(f"\u26a0 Crop model artifacts not found in {saved_models_dir}")

        if fertilizer_model is None:
            fertilizer_model = FertilizerRecommendationModel(use_ml=False)
            print("\u2713 Fertilizer model initialized")

    except Exception as e:
        print(f"Error loading models: {str(e)}")
