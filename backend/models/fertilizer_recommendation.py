"""
Fertilizer Recommendation System

This module implements a fertilizer recommendation system based on soil nutrient
deficiencies (N, P, K) and crop requirements. Uses both rule-based and ML approaches.

Author: ML Agriculture Team
Date: December 2025
"""

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os


class FertilizerRecommendationModel:
    """
    Fertilizer Recommendation System based on NPK deficiencies
    
    Fertilizer Types:
    - Urea (high N)
    - DAP (Diammonium Phosphate - high P)
    - MOP (Muriate of Potash - high K)
    - NPK (balanced)
    - Organic (general purpose)
    """
    
    # Define nutrient thresholds (in kg/ha or ppm)
    THRESHOLDS = {
        'N_low': 50,
        'N_medium': 100,
        'N_high': 150,
        'P_low': 25,
        'P_medium': 50,
        'P_high': 75,
        'K_low': 100,
        'K_medium': 200,
        'K_high': 300
    }
    
    # Crop-specific NPK requirements (N, P, K)
    CROP_REQUIREMENTS = {
        'rice': {'N': 120, 'P': 60, 'K': 40},
        'wheat': {'N': 120, 'P': 60, 'K': 40},
        'maize': {'N': 120, 'P': 60, 'K': 40},
        'cotton': {'N': 120, 'P': 60, 'K': 50},
        'sugarcane': {'N': 200, 'P': 100, 'K': 100},
        'groundnut': {'N': 25, 'P': 50, 'K': 75},
        'pulses': {'N': 20, 'P': 60, 'K': 40},
        'vegetables': {'N': 100, 'P': 80, 'K': 80},
        'fruits': {'N': 150, 'P': 100, 'K': 120},
        'default': {'N': 100, 'P': 60, 'K': 60}
    }
    
    def __init__(self, use_ml=True):
        """
        Initialize Fertilizer Recommendation System
        
        Args:
            use_ml (bool): Whether to use ML model or pure rule-based approach
        """
        self.use_ml = use_ml
        self.model = None
        self.is_trained = False
        
        if use_ml:
            self.model = DecisionTreeClassifier(
                max_depth=10,
                random_state=42,
                min_samples_split=5
            )
    
    def rule_based_recommendation(self, N, P, K, crop='default', soil_type='loamy'):
        """
        Rule-based fertilizer recommendation using NPK deficiency analysis
        
        Args:
            N (float): Current nitrogen level
            P (float): Current phosphorus level
            K (float): Current potassium level
            crop (str): Crop type
            soil_type (str): Soil type
            
        Returns:
            dict: Recommendation with fertilizer type and reasoning
        """
        crop = crop.lower()
        if crop not in self.CROP_REQUIREMENTS:
            crop = 'default'
        
        required = self.CROP_REQUIREMENTS[crop]
        
        # Calculate deficiencies
        N_deficit = max(0, required['N'] - N)
        P_deficit = max(0, required['P'] - P)
        K_deficit = max(0, required['K'] - K)
        
        # Determine primary deficiency
        deficiencies = {'N': N_deficit, 'P': P_deficit, 'K': K_deficit}
        max_deficit = max(deficiencies.values())
        
        # Recommendation logic
        recommendation = {}
        
        if max_deficit == 0:
            recommendation = {
                'fertilizer': 'No fertilizer needed',
                'reason': 'Soil nutrient levels are adequate for the crop',
                'deficiencies': deficiencies,
                'alternative': 'Consider organic manure for soil health'
            }
        elif N_deficit > P_deficit and N_deficit > K_deficit:
            # High nitrogen deficiency
            if N_deficit > 80:
                recommendation = {
                    'fertilizer': 'Urea',
                    'amount': f'{int(N_deficit * 2.17)} kg/ha',  # Conversion factor for urea
                    'reason': f'High nitrogen deficiency detected ({int(N_deficit)} kg/ha)',
                    'deficiencies': deficiencies,
                    'application': 'Apply in split doses - 50% at planting, 50% at growth stage'
                }
            else:
                recommendation = {
                    'fertilizer': 'NPK 20-10-10',
                    'amount': f'{int(N_deficit * 5)} kg/ha',
                    'reason': f'Moderate nitrogen deficiency with balanced nutrients',
                    'deficiencies': deficiencies,
                    'application': 'Apply during land preparation'
                }
        elif P_deficit > N_deficit and P_deficit > K_deficit:
            # High phosphorus deficiency
            if P_deficit > 40:
                recommendation = {
                    'fertilizer': 'DAP (Di-Ammonium Phosphate)',
                    'amount': f'{int(P_deficit * 2.22)} kg/ha',  # Conversion factor for DAP
                    'reason': f'High phosphorus deficiency detected ({int(P_deficit)} kg/ha)',
                    'deficiencies': deficiencies,
                    'application': 'Apply as basal dose during sowing'
                }
            else:
                recommendation = {
                    'fertilizer': 'SSP (Single Super Phosphate)',
                    'amount': f'{int(P_deficit * 6.25)} kg/ha',
                    'reason': f'Moderate phosphorus deficiency',
                    'deficiencies': deficiencies,
                    'application': 'Apply during land preparation'
                }
        elif K_deficit > N_deficit and K_deficit > P_deficit:
            # High potassium deficiency
            if K_deficit > 60:
                recommendation = {
                    'fertilizer': 'MOP (Muriate of Potash)',
                    'amount': f'{int(K_deficit * 1.67)} kg/ha',  # Conversion factor for MOP
                    'reason': f'High potassium deficiency detected ({int(K_deficit)} kg/ha)',
                    'deficiencies': deficiencies,
                    'application': 'Apply in split doses during growth stages'
                }
            else:
                recommendation = {
                    'fertilizer': 'NPK 10-10-20',
                    'amount': f'{int(K_deficit * 5)} kg/ha',
                    'reason': f'Moderate potassium deficiency',
                    'deficiencies': deficiencies,
                    'application': 'Apply during flowering/fruiting stage'
                }
        else:
            # Multiple deficiencies
            recommendation = {
                'fertilizer': 'NPK 10-26-26 or NPK 20-20-0-13',
                'amount': f'{int((N_deficit + P_deficit + K_deficit) / 3 * 3)} kg/ha',
                'reason': 'Multiple nutrient deficiencies detected',
                'deficiencies': deficiencies,
                'application': 'Apply as per crop growth stage requirements'
            }
        
        # Add soil-specific recommendations
        if soil_type.lower() == 'sandy':
            recommendation['note'] = 'Sandy soil: Apply in smaller, more frequent doses to prevent leaching'
        elif soil_type.lower() == 'clayey':
            recommendation['note'] = 'Clayey soil: Ensure good drainage before application'
        
        return recommendation
    
    def train_ml_model(self, X, y):
        """
        Train ML model for fertilizer recommendation
        
        Args:
            X (pd.DataFrame): Features (N, P, K, crop_encoded, soil_encoded)
            y (pd.Series): Target (fertilizer type)
            
        Returns:
            dict: Training metrics
        """
        if not self.use_ml:
            raise ValueError("ML mode is not enabled for this instance")
        
        print("=" * 60)
        print("Training Fertilizer Recommendation Model")
        print("=" * 60)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\nTraining samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")
        
        # Train model
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Predictions
        y_pred = self.model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n✓ Model Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        return {
            'accuracy': accuracy,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
    
    def predict(self, input_data):
        """
        Predict fertilizer recommendation
        
        Args:
            input_data (dict): {
                'N': 40,
                'P': 30,
                'K': 25,
                'crop': 'wheat',
                'soil_type': 'loamy'
            }
            
        Returns:
            dict: Fertilizer recommendation
        """
        N = input_data.get('N', 0)
        P = input_data.get('P', 0)
        K = input_data.get('K', 0)
        crop = input_data.get('crop', 'default')
        soil_type = input_data.get('soil_type', 'loamy')
        
        # Use rule-based recommendation
        recommendation = self.rule_based_recommendation(N, P, K, crop, soil_type)
        
        return recommendation
    
    def save_model(self, model_path='saved_models/fertilizer_model.pkl'):
        """Save trained ML model"""
        if self.use_ml and self.is_trained:
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            joblib.dump(self.model, model_path)
            print(f"✓ Model saved to: {model_path}")
        else:
            print("ℹ Rule-based model - no file to save")
    
    def load_model(self, model_path='saved_models/fertilizer_model.pkl'):
        """Load trained ML model"""
        if self.use_ml and os.path.exists(model_path):
            self.model = joblib.load(model_path)
            self.is_trained = True
            print(f"✓ Model loaded from: {model_path}")
        else:
            print("ℹ Using rule-based approach")
    
    def generate_nutrient_report(self, N, P, K, crop='default'):
        """
        Generate detailed nutrient analysis report
        
        Args:
            N, P, K: Current nutrient levels
            crop: Crop type
            
        Returns:
            dict: Detailed nutrient analysis
        """
        crop = crop.lower()
        if crop not in self.CROP_REQUIREMENTS:
            crop = 'default'
        
        required = self.CROP_REQUIREMENTS[crop]
        
        report = {
            'current_levels': {'N': N, 'P': P, 'K': K},
            'required_levels': required,
            'status': {
                'N': 'Adequate' if N >= required['N'] else 'Deficient',
                'P': 'Adequate' if P >= required['P'] else 'Deficient',
                'K': 'Adequate' if K >= required['K'] else 'Deficient'
            },
            'deficit': {
                'N': max(0, required['N'] - N),
                'P': max(0, required['P'] - P),
                'K': max(0, required['K'] - K)
            }
        }
        
        return report


# Example usage
if __name__ == "__main__":
    print("Fertilizer Recommendation System - Test Mode")
    print("=" * 60)
    
    # Initialize model
    fert_model = FertilizerRecommendationModel(use_ml=False)
    
    # Test cases
    test_cases = [
        {'N': 30, 'P': 40, 'K': 25, 'crop': 'wheat', 'soil_type': 'loamy'},
        {'N': 80, 'P': 20, 'K': 50, 'crop': 'rice', 'soil_type': 'clayey'},
        {'N': 120, 'P': 70, 'K': 45, 'crop': 'maize', 'soil_type': 'sandy'},
    ]
    
    print("\nTesting Fertilizer Recommendations:\n")
    for i, test in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"Input: N={test['N']}, P={test['P']}, K={test['K']}, Crop={test['crop']}")
        result = fert_model.predict(test)
        print(f"Recommendation: {result['fertilizer']}")
        print(f"Reason: {result['reason']}")
        print("-" * 60)
    
    print("\n✓ Module loaded successfully!")
