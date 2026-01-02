"""
Crop Recommendation Model using Random Forest Classifier

This module implements a machine learning model to recommend the most suitable crop
based on soil parameters (N, P, K, pH) and climate parameters (temperature, humidity, rainfall).

Author: ML Agriculture Team
Date: December 2025
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import os


class CropRecommendationModel:
    """
    Random Forest-based Crop Recommendation System
    
    Features:
    - N (Nitrogen content in soil)
    - P (Phosphorus content in soil)
    - K (Potassium content in soil)
    - temperature (Temperature in Celsius)
    - humidity (Relative humidity in %)
    - pH (pH value of soil)
    - rainfall (Rainfall in mm)
    """
    
    def __init__(self, n_estimators=100, max_depth=10, random_state=42):
        """
        Initialize the Crop Recommendation Model
        
        Args:
            n_estimators (int): Number of trees in the forest
            max_depth (int): Maximum depth of the trees
            random_state (int): Random state for reproducibility
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1  # Use all CPU cores
        )
        self.scaler = StandardScaler()
        self.feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'pH', 'rainfall']
        self.crop_labels = None
        self.is_trained = False
        
    def preprocess_data(self, X):
        """
        Preprocess input features using standardization
        
        Args:
            X (array-like): Input features
            
        Returns:
            array: Scaled features
        """
        return self.scaler.transform(X)
    
    def train(self, X, y, test_size=0.2, validate=True):
        """
        Train the Random Forest model
        
        Args:
            X (pd.DataFrame or array): Feature matrix
            y (pd.Series or array): Target labels
            test_size (float): Proportion of dataset for testing
            validate (bool): Whether to perform validation
            
        Returns:
            dict: Training metrics
        """
        print("=" * 60)
        print("Training Crop Recommendation Model")
        print("=" * 60)
        
        # Convert to numpy arrays if DataFrame/Series
        if isinstance(X, pd.DataFrame):
            X = X.values
        if isinstance(y, pd.Series):
            y = y.values
            
        # Store unique crop labels
        self.crop_labels = np.unique(y)
        print(f"Number of crops: {len(self.crop_labels)}")
        print(f"Crops: {', '.join(self.crop_labels)}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"\nDataset Split:")
        print(f"Training samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")
        
        # Fit scaler on training data
        self.scaler.fit(X_train)
        
        # Transform data
        X_train_scaled = self.scaler.transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        print("\nTraining Random Forest Classifier...")
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        print("✓ Training completed!")
        
        # Predictions
        y_train_pred = self.model.predict(X_train_scaled)
        y_test_pred = self.model.predict(X_test_scaled)
        
        # Calculate metrics
        metrics = {
            'train_accuracy': accuracy_score(y_train, y_train_pred),
            'test_accuracy': accuracy_score(y_test, y_test_pred),
            'precision': precision_score(y_test, y_test_pred, average='weighted'),
            'recall': recall_score(y_test, y_test_pred, average='weighted'),
            'f1_score': f1_score(y_test, y_test_pred, average='weighted'),
            'confusion_matrix': confusion_matrix(y_test, y_test_pred)
        }
        
        # Cross-validation
        if validate:
            print("\nPerforming 5-fold Cross-Validation...")
            cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5)
            metrics['cv_scores'] = cv_scores
            metrics['cv_mean'] = cv_scores.mean()
            metrics['cv_std'] = cv_scores.std()
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        metrics['feature_importance'] = feature_importance
        
        # Print results
        self._print_metrics(metrics)
        
        return metrics
    
    def predict(self, input_data):
        """
        Predict the most suitable crop for given parameters
        
        Args:
            input_data (dict or array): Input features
                If dict: {'N': 90, 'P': 42, 'K': 43, 'temperature': 20.87, 
                         'humidity': 82.0, 'pH': 6.5, 'rainfall': 202.9}
                         
        Returns:
            dict: Prediction results with crop name and confidence
        """
        if not self.is_trained:
            raise ValueError("Model is not trained yet. Please train the model first.")
        
        # Convert dict to array if needed
        if isinstance(input_data, dict):
            X = np.array([[
                input_data['N'],
                input_data['P'],
                input_data['K'],
                input_data['temperature'],
                input_data['humidity'],
                input_data['pH'],
                input_data['rainfall']
            ]])
        else:
            X = np.array(input_data).reshape(1, -1)
        
        # Preprocess
        X_scaled = self.preprocess_data(X)
        
        # Predict
        prediction = self.model.predict(X_scaled)[0]
        
        # Get probability scores
        probabilities = self.model.predict_proba(X_scaled)[0]
        confidence = np.max(probabilities)
        
        # Get top 3 predictions
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        top_3_crops = [(self.model.classes_[i], probabilities[i]) for i in top_3_indices]
        
        result = {
            'crop': prediction,
            'confidence': float(confidence),
            'top_3_predictions': [
                {'crop': crop, 'confidence': float(conf)} 
                for crop, conf in top_3_crops
            ]
        }
        
        return result
    
    def save_model(self, model_path='saved_models/crop_model.pkl', 
                   scaler_path='saved_models/crop_scaler.pkl'):
        """
        Save trained model and scaler to disk
        
        Args:
            model_path (str): Path to save the model
            scaler_path (str): Path to save the scaler
        """
        if not self.is_trained:
            raise ValueError("Model is not trained yet. Cannot save untrained model.")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save model and scaler
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        
        # Save crop labels
        labels_path = model_path.replace('.pkl', '_labels.pkl')
        joblib.dump(self.crop_labels, labels_path)
        
        print(f"✓ Model saved to: {model_path}")
        print(f"✓ Scaler saved to: {scaler_path}")
        print(f"✓ Labels saved to: {labels_path}")
    
    def load_model(self, model_path='saved_models/crop_model.pkl',
                   scaler_path='saved_models/crop_scaler.pkl'):
        """
        Load trained model and scaler from disk
        
        Args:
            model_path (str): Path to load the model
            scaler_path (str): Path to load the scaler
        """
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        
        # Load crop labels
        labels_path = model_path.replace('.pkl', '_labels.pkl')
        self.crop_labels = joblib.load(labels_path)
        
        self.is_trained = True
        print(f"✓ Model loaded from: {model_path}")
        print(f"✓ Scaler loaded from: {scaler_path}")
        print(f"✓ Labels loaded from: {labels_path}")
    
    def _print_metrics(self, metrics):
        """Print training metrics in a formatted way"""
        print("\n" + "=" * 60)
        print("MODEL EVALUATION METRICS")
        print("=" * 60)
        
        print(f"\n📊 Accuracy Metrics:")
        print(f"   Training Accuracy:   {metrics['train_accuracy']:.4f} ({metrics['train_accuracy']*100:.2f}%)")
        print(f"   Testing Accuracy:    {metrics['test_accuracy']:.4f} ({metrics['test_accuracy']*100:.2f}%)")
        
        if 'cv_mean' in metrics:
            print(f"\n🔄 Cross-Validation (5-fold):")
            print(f"   Mean CV Score:       {metrics['cv_mean']:.4f} ± {metrics['cv_std']:.4f}")
            print(f"   Individual Scores:   {[f'{score:.4f}' for score in metrics['cv_scores']]}")
        
        print(f"\n📈 Classification Metrics:")
        print(f"   Precision (weighted): {metrics['precision']:.4f}")
        print(f"   Recall (weighted):    {metrics['recall']:.4f}")
        print(f"   F1-Score (weighted):  {metrics['f1_score']:.4f}")
        
        print(f"\n🔍 Feature Importance:")
        for _, row in metrics['feature_importance'].iterrows():
            print(f"   {row['feature']:15s}: {row['importance']:.4f}")
        
        print("\n" + "=" * 60)


# Example usage and testing
if __name__ == "__main__":
    print("Crop Recommendation Model - Test Mode")
    print("=" * 60)
    
    # This would normally load from a CSV file
    # For demonstration, here's how to use the model:
    
    """
    # Example: Load dataset
    df = pd.read_csv('../../data/crop_recommendation.csv')
    
    # Separate features and target
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    # Initialize and train model
    crop_model = CropRecommendationModel()
    metrics = crop_model.train(X, y)
    
    # Save model
    crop_model.save_model()
    
    # Make prediction
    test_input = {
        'N': 90,
        'P': 42,
        'K': 43,
        'temperature': 20.87,
        'humidity': 82.0,
        'pH': 6.5,
        'rainfall': 202.9
    }
    
    result = crop_model.predict(test_input)
    print(f"\nRecommended Crop: {result['crop']}")
    print(f"Confidence: {result['confidence']*100:.2f}%")
    """
    
    print("\n✓ Module loaded successfully!")
    print("Import this module in your training script to use the model.")
