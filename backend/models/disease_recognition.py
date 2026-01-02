"""
Plant Disease Recognition using CNN

This module implements a Convolutional Neural Network (CNN) for classifying
plant disease images across multiple crops.

Supports:
- Multi-crop disease detection (Cashew, Cassava, Maize, Tomato)
- 22 disease classes
- Both custom CNN and transfer learning approaches

Author: ML Agriculture Team
Date: December 2025
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import os
import cv2
from PIL import Image
import json


class PlantDiseaseRecognitionModel:
    """
    CNN-based Plant Disease Classification System
    
    Supports multi-crop disease detection:
    - Cashew: 5 disease classes
    - Cassava: 5 disease classes
    - Maize: 7 disease classes
    - Tomato: 5 disease classes
    
    Total: 22 disease classes across 4 crops
    """
    
    def __init__(self, img_size=(128, 128), num_classes=22, use_pretrained=False):
        """
        Initialize the CNN model
        
        Args:
            img_size (tuple): Input image size (height, width)
            num_classes (int): Number of classification categories (22 for plant diseases)
            use_pretrained (bool): Use transfer learning with MobileNetV2
        """
        self.img_size = img_size
        self.num_classes = num_classes
        self.use_pretrained = use_pretrained
        self.model = None
        self.class_names = []
        self.is_trained = False
        
    def build_model(self):
        """
        Build CNN architecture
        
        Two approaches:
        1. Transfer Learning with MobileNetV2 (recommended)
        2. Custom CNN from scratch
        """
        if self.use_pretrained:
            print("Building model with Transfer Learning (MobileNetV2)...")
            self.model = self._build_transfer_learning_model()
        else:
            print("Building custom CNN model...")
            self.model = self._build_custom_cnn()
        
        print("✓ Model built successfully!")
        return self.model
    
    def _build_transfer_learning_model(self):
        """
        Build model using transfer learning with MobileNetV2
        
        MobileNetV2 is lightweight and efficient, pre-trained on ImageNet
        """
        # Load pre-trained MobileNetV2 without top layers
        base_model = MobileNetV2(
            input_shape=(*self.img_size, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Build model
        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.3),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        return model
    
    def _build_custom_cnn(self):
        """
        Build custom CNN architecture from scratch
        
        Architecture:
        - 4 Convolutional blocks with increasing filters
        - MaxPooling for spatial reduction
        - Dropout for regularization
        - Dense layers for classification
        """
        model = models.Sequential([
            # Input layer
            layers.Input(shape=(*self.img_size, 3)),
            
            # Conv Block 1
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Conv Block 2
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Conv Block 3
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Conv Block 4
            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Flatten and Dense layers
            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.4),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        return model
    
    def create_data_generators(self, train_dir, val_dir=None, batch_size=32):
        """
        Create data generators with augmentation
        
        Args:
            train_dir (str): Path to training data directory
            val_dir (str): Path to validation data directory
            batch_size (int): Batch size for training
            
        Returns:
            tuple: (train_generator, val_generator)
        """
        # Training data augmentation
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=30,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            brightness_range=[0.8, 1.2],
            fill_mode='nearest',
            validation_split=0.2 if val_dir is None else 0.0
        )
        
        # Validation data (only rescaling)
        val_datagen = ImageDataGenerator(rescale=1./255)
        
        # Create generators
        if val_dir is None:
            # Use validation_split
            train_generator = train_datagen.flow_from_directory(
                train_dir,
                target_size=self.img_size,
                batch_size=batch_size,
                class_mode='categorical',
                subset='training'
            )
            
            val_generator = train_datagen.flow_from_directory(
                train_dir,
                target_size=self.img_size,
                batch_size=batch_size,
                class_mode='categorical',
                subset='validation'
            )
        else:
            train_generator = train_datagen.flow_from_directory(
                train_dir,
                target_size=self.img_size,
                batch_size=batch_size,
                class_mode='categorical'
            )
            
            val_generator = val_datagen.flow_from_directory(
                val_dir,
                target_size=self.img_size,
                batch_size=batch_size,
                class_mode='categorical'
            )
        
        # Store class names
        self.class_names = list(train_generator.class_indices.keys())
        
        return train_generator, val_generator
    
    def train(self, train_generator, val_generator, epochs=50, 
              model_save_path='saved_models/fertilizer_cnn_model.h5'):
        """
        Train the CNN model
        
        Args:
            train_generator: Training data generator
            val_generator: Validation data generator
            epochs (int): Number of training epochs
            model_save_path (str): Path to save best model
            
        Returns:
            dict: Training history and metrics
        """
        if self.model is None:
            self.build_model()
        
        print("=" * 60)
        print("Training Fertilizer Disease Recognition Model")
        print("=" * 60)
        print(f"Classes: {self.class_names}")
        print(f"Training samples: {train_generator.samples}")
        print(f"Validation samples: {val_generator.samples}")
        print(f"Batch size: {train_generator.batch_size}")
        print(f"Steps per epoch: {len(train_generator)}")
        
        # Create callbacks
        callbacks = [
            # Save best model
            ModelCheckpoint(
                model_save_path,
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            # Early stopping
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            # Reduce learning rate
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        # Train model
        print("\nStarting training...")
        history = self.model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        self.is_trained = True
        print("\n✓ Training completed!")
        
        # Evaluate on validation set
        val_loss, val_accuracy, val_precision, val_recall = self.model.evaluate(
            val_generator, verbose=0
        )
        
        print(f"\nFinal Validation Metrics:")
        print(f"  Accuracy:  {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")
        print(f"  Precision: {val_precision:.4f}")
        print(f"  Recall:    {val_recall:.4f}")
        print(f"  F1-Score:  {2 * (val_precision * val_recall) / (val_precision + val_recall):.4f}")
        
        return {
            'history': history.history,
            'val_accuracy': val_accuracy,
            'val_precision': val_precision,
            'val_recall': val_recall
        }
    
    def predict_image(self, image_path):
        """
        Predict plant disease from image
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            dict: Prediction results with disease name, crop, and confidence scores
        """
        if not self.is_trained and self.model is None:
            raise ValueError("Model is not trained or loaded. Please train or load model first.")
        
        # Load and preprocess image
        img = Image.open(image_path).convert('RGB')
        img = img.resize(self.img_size)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        predictions = self.model.predict(img_array, verbose=0)[0]
        
        # Get predicted class
        predicted_class_idx = np.argmax(predictions)
        predicted_class = self.class_names[predicted_class_idx] if self.class_names else f"Class_{predicted_class_idx}"
        confidence = float(predictions[predicted_class_idx])
        
        # Extract crop and disease from class name (format: "Crop/disease_name")
        crop = None
        disease = predicted_class
        if '/' in predicted_class:
            parts = predicted_class.split('/')
            if len(parts) >= 2:
                crop = parts[0]
                disease = parts[-1]
        
        # Get all predictions
        all_predictions = {
            (self.class_names[i] if self.class_names else f"Class_{i}"): float(predictions[i]) 
            for i in range(len(predictions))
        }
        
        # Sort by confidence
        sorted_predictions = sorted(
            all_predictions.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Format top 3 predictions
        top_3 = []
        for cls, conf in sorted_predictions[:3]:
            pred_crop = None
            pred_disease = cls
            if '/' in cls:
                parts = cls.split('/')
                if len(parts) >= 2:
                    pred_crop = parts[0]
                    pred_disease = parts[-1]
            
            top_3.append({
                'class': cls,
                'crop': pred_crop,
                'disease': pred_disease,
                'confidence': conf
            })
        
        result = {
            'prediction': predicted_class,
            'crop': crop,
            'disease': disease,
            'confidence': confidence,
            'all_predictions': all_predictions,
            'top_3_predictions': top_3
        }
        
        return result
    
    def predict_from_array(self, image_array):
        """
        Predict from numpy array
        
        Args:
            image_array (np.array): Image as numpy array
            
        Returns:
            dict: Prediction results
        """
        if not self.is_trained and self.model is None:
            raise ValueError("Model is not trained or loaded.")
        
        # Preprocess
        if image_array.shape[:2] != self.img_size:
            image_array = cv2.resize(image_array, self.img_size)
        
        if image_array.max() > 1.0:
            image_array = image_array / 255.0
        
        img_array = np.expand_dims(image_array, axis=0)
        
        # Predict
        predictions = self.model.predict(img_array, verbose=0)[0]
        predicted_class_idx = np.argmax(predictions)
        
        result = {
            'prediction': self.class_names[predicted_class_idx],
            'confidence': float(predictions[predicted_class_idx]),
            'all_predictions': {
                self.class_names[i]: float(predictions[i]) 
                for i in range(len(self.class_names))
            }
        }
        
        return result
    
    def save_model(self, model_path='saved_models/fertilizer_cnn_model.h5'):
        """Save trained model"""
        if self.model is None:
            raise ValueError("No model to save")
        
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        self.model.save(model_path)
        
        # Save class names
        import json
        class_names_path = model_path.replace('.h5', '_classes.json')
        with open(class_names_path, 'w') as f:
            json.dump(self.class_names, f)
        
        print(f"✓ Model saved to: {model_path}")
        print(f"✓ Class names saved to: {class_names_path}")
    
    def load_model(self, model_path='saved_models/plant_disease_model.keras', class_names_path='saved_models/plant_disease_classes.json'):
        """
        Load trained plant disease model
        
        Args:
            model_path (str): Path to saved model file
            class_names_path (str): Path to class names JSON file
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        print(f"Loading model from: {model_path}")
        self.model = keras.models.load_model(model_path)
        
        # Load class names
        if os.path.exists(class_names_path):
            with open(class_names_path, 'r') as f:
                self.class_names = json.load(f)
            print(f"✓ Loaded {len(self.class_names)} disease classes")
        else:
            print(f"⚠ Class names file not found: {class_names_path}")
            print("  Using default numbering for classes")
            self.class_names = [f"Class_{i}" for i in range(self.num_classes)]
        
        self.is_trained = True
        print(f"✓ Model loaded successfully")
        return self.model
    
    def plot_training_history(self, history, save_path=None):
        """Plot training history"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Accuracy
        axes[0, 0].plot(history['accuracy'], label='Train Accuracy')
        axes[0, 0].plot(history['val_accuracy'], label='Val Accuracy')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss
        axes[0, 1].plot(history['loss'], label='Train Loss')
        axes[0, 1].plot(history['val_loss'], label='Val Loss')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Precision
        axes[1, 0].plot(history['precision'], label='Train Precision')
        axes[1, 0].plot(history['val_precision'], label='Val Precision')
        axes[1, 0].set_title('Model Precision')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Precision')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Recall
        axes[1, 1].plot(history['recall'], label='Train Recall')
        axes[1, 1].plot(history['val_recall'], label='Val Recall')
        axes[1, 1].set_title('Model Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            print(f"✓ Training history plot saved to: {save_path}")
        else:
            plt.show()
    
    def get_model_summary(self):
        """Print model architecture summary"""
        if self.model is None:
            print("Model not built yet")
        else:
            self.model.summary()


# Example usage
if __name__ == "__main__":
    print("Fertilizer Disease Recognition Model - Test Mode")
    print("=" * 60)
    
    # Initialize model
    disease_model = FertilizerDiseaseRecognitionModel(
        img_size=(224, 224),
        num_classes=5,
        use_pretrained=True
    )
    
    # Build model
    disease_model.build_model()
    disease_model.get_model_summary()
    
    print("\n✓ Module loaded successfully!")
    print("Use this module in training scripts to train the CNN model.")
