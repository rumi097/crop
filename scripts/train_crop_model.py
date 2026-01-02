"""
Training Script for Crop Recommendation Model

This script trains a Random Forest Classifier for crop recommendation using
soil and climate parameters from Kaggle dataset.

Dataset: https://www.kaggle.com/atharvaingle/crop-recommendation-dataset

Author: ML Agriculture Team
Date: December 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models.crop_recommendation import CropRecommendationModel
from sklearn.metrics import confusion_matrix


def load_dataset(file_path='../data/crop_recommendation.csv'):
    """
    Load crop recommendation dataset
    
    Dataset columns:
    - N: Nitrogen content ratio in soil
    - P: Phosphorus content ratio in soil
    - K: Potassium content ratio in soil
    - temperature: Temperature in Celsius
    - humidity: Relative humidity in %
    - ph: pH value of soil
    - rainfall: Rainfall in mm
    - label: Crop name (target variable)
    """
    print("=" * 60)
    print("Loading Crop Recommendation Dataset")
    print("=" * 60)
    
    try:
        df = pd.read_csv(file_path)
        print(f"✓ Dataset loaded successfully")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        
        return df
    
    except FileNotFoundError:
        print(f"⚠ Dataset not found at: {file_path}")
        print("\nCreating sample dataset for demonstration...")
        
        # Create sample dataset if file doesn't exist
        df = create_sample_dataset()
        
        # Save sample dataset
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        print(f"✓ Sample dataset saved to: {file_path}")
        
        return df


def create_sample_dataset():
    """
    Create a sample dataset for demonstration purposes
    
    In production, download the actual dataset from Kaggle:
    https://www.kaggle.com/atharvaingle/crop-recommendation-dataset
    """
    np.random.seed(42)
    
    crops = ['rice', 'wheat', 'maize', 'cotton', 'sugarcane', 'groundnut', 
             'pulses', 'coffee', 'apple', 'orange', 'banana', 'grapes',
             'watermelon', 'mango', 'pomegranate', 'papaya', 'coconut',
             'jute', 'chickpea', 'kidneybeans', 'pigeonpeas', 'mothbeans']
    
    samples_per_crop = 100
    data = []
    
    # Define typical ranges for each crop (simplified)
    crop_params = {
        'rice': {'N': (80, 100), 'P': (40, 50), 'K': (35, 45), 
                 'temp': (20, 27), 'hum': (80, 85), 'ph': (5.5, 7.0), 'rain': (200, 250)},
        'wheat': {'N': (100, 120), 'P': (50, 70), 'K': (40, 50),
                  'temp': (15, 25), 'hum': (50, 70), 'ph': (6.0, 7.5), 'rain': (50, 100)},
        'maize': {'N': (70, 90), 'P': (45, 60), 'K': (35, 50),
                  'temp': (18, 27), 'hum': (60, 75), 'ph': (5.5, 7.0), 'rain': (60, 110)},
        'cotton': {'N': (110, 130), 'P': (40, 60), 'K': (45, 55),
                   'temp': (21, 30), 'hum': (55, 75), 'ph': (6.0, 8.0), 'rain': (50, 100)},
        'sugarcane': {'N': (75, 100), 'P': (50, 80), 'K': (50, 70),
                      'temp': (21, 27), 'hum': (75, 87), 'ph': (6.0, 7.5), 'rain': (75, 150)},
    }
    
    # Generate data for each crop
    for crop in crops:
        params = crop_params.get(crop, {
            'N': (50, 150), 'P': (30, 80), 'K': (30, 80),
            'temp': (15, 35), 'hum': (40, 90), 'ph': (5.0, 8.0), 'rain': (50, 300)
        })
        
        for _ in range(samples_per_crop):
            data.append({
                'N': np.random.uniform(*params['N']),
                'P': np.random.uniform(*params['P']),
                'K': np.random.uniform(*params['K']),
                'temperature': np.random.uniform(*params['temp']),
                'humidity': np.random.uniform(*params['hum']),
                'ph': np.random.uniform(*params['ph']),
                'rainfall': np.random.uniform(*params['rain']),
                'label': crop
            })
    
    df = pd.DataFrame(data)
    return df


def perform_eda(df):
    """Perform Exploratory Data Analysis"""
    print("\n" + "=" * 60)
    print("Exploratory Data Analysis")
    print("=" * 60)
    
    # Basic statistics
    print("\nDataset Info:")
    print(df.info())
    
    print("\nStatistical Summary:")
    print(df.describe())
    
    print("\nCrop Distribution:")
    print(df['label'].value_counts())
    
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    # Visualizations
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    fig.suptitle('Feature Distributions', fontsize=16, fontweight='bold')
    
    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    for idx, feature in enumerate(features):
        row = idx // 3
        col = idx % 3
        axes[row, col].hist(df[feature], bins=30, edgecolor='black', alpha=0.7)
        axes[row, col].set_title(f'{feature} Distribution')
        axes[row, col].set_xlabel(feature)
        axes[row, col].set_ylabel('Frequency')
        axes[row, col].grid(True, alpha=0.3)
    
    # Crop distribution
    crop_counts = df['label'].value_counts()
    axes[2, 1].barh(crop_counts.index[:10], crop_counts.values[:10])
    axes[2, 1].set_title('Top 10 Crops Distribution')
    axes[2, 1].set_xlabel('Count')
    
    # Correlation heatmap
    axes[2, 2].remove()
    ax_corr = fig.add_subplot(3, 3, 9)
    corr_matrix = df[features].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                square=True, ax=ax_corr, cbar_kws={'shrink': 0.8})
    ax_corr.set_title('Feature Correlation')
    
    plt.tight_layout()
    plt.savefig('../backend/saved_models/crop_eda.png', dpi=300, bbox_inches='tight')
    print("\n✓ EDA visualizations saved to: ../backend/saved_models/crop_eda.png")


def plot_confusion_matrix(y_true, y_pred, classes, save_path):
    """Plot confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(20, 18))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=classes, yticklabels=classes,
                cbar_kws={'label': 'Count'})
    plt.title('Confusion Matrix - Crop Recommendation', fontsize=16, fontweight='bold')
    plt.xlabel('Predicted Crop', fontsize=12)
    plt.ylabel('Actual Crop', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Confusion matrix saved to: {save_path}")


def main():
    """Main training pipeline"""
    print("\n" + "=" * 60)
    print("CROP RECOMMENDATION MODEL TRAINING")
    print("=" * 60)
    
    # Step 1: Load dataset
    df = load_dataset('../data/crop_recommendation.csv')
    
    # Step 2: Perform EDA
    perform_eda(df)
    
    # Step 3: Prepare data
    print("\n" + "=" * 60)
    print("Preparing Data")
    print("=" * 60)
    
    # Note: Dataset uses 'ph' not 'pH'
    feature_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    X = df[feature_columns]
    y = df['label']
    
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    print(f"Number of classes: {len(y.unique())}")
    
    # Step 4: Initialize and train model
    model = CropRecommendationModel(n_estimators=100, max_depth=10, random_state=42)
    
    # Train model
    metrics = model.train(X, y, test_size=0.2, validate=True)
    
    # Step 5: Plot confusion matrix
    # For plotting, we need to make predictions on test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    X_test_scaled = model.scaler.transform(X_test)
    y_pred = model.model.predict(X_test_scaled)
    
    plot_confusion_matrix(
        y_test, y_pred, 
        sorted(y.unique()),
        '../backend/saved_models/crop_confusion_matrix.png'
    )
    
    # Step 6: Save model
    print("\n" + "=" * 60)
    print("Saving Model")
    print("=" * 60)
    model.save_model(
        model_path='../backend/saved_models/crop_model.pkl',
        scaler_path='../backend/saved_models/crop_scaler.pkl'
    )
    
    # Step 7: Test predictions
    print("\n" + "=" * 60)
    print("Testing Model Predictions")
    print("=" * 60)
    
    test_cases = [
        {'N': 90, 'P': 42, 'K': 43, 'temperature': 20.87, 
         'humidity': 82.0, 'pH': 6.5, 'rainfall': 202.9},
        {'N': 110, 'P': 55, 'K': 45, 'temperature': 23.5,
         'humidity': 65.0, 'pH': 7.0, 'rainfall': 75.0},
        {'N': 85, 'P': 58, 'K': 41, 'temperature': 21.0,
         'humidity': 80.0, 'pH': 7.0, 'rainfall': 140.0}
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Input: N={test_input['N']}, P={test_input['P']}, K={test_input['K']}")
        print(f"       Temp={test_input['temperature']}°C, Humidity={test_input['humidity']}%")
        print(f"       pH={test_input['pH']}, Rainfall={test_input['rainfall']}mm")
        
        result = model.predict(test_input)
        print(f"Predicted Crop: {result['crop']}")
        print(f"Confidence: {result['confidence']*100:.2f}%")
        print(f"Top 3 Predictions:")
        for pred in result['top_3_predictions']:
            print(f"  - {pred['crop']}: {pred['confidence']*100:.2f}%")
    
    print("\n" + "=" * 60)
    print("✓ TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nModel files saved in: ../backend/saved_models/")
    print("  - crop_model.pkl")
    print("  - crop_scaler.pkl")
    print("  - crop_model_labels.pkl")
    print("\nVisualization files:")
    print("  - crop_eda.png")
    print("  - crop_confusion_matrix.png")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
