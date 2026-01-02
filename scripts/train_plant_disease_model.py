"""
Training Script for Multi-Crop Plant Disease Detection Model

This script trains a CNN model on the CCMT Multi-Crop Plant Disease Detection Dataset.
Dataset: https://www.kaggle.com/datasets/shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset

Crops: Cashew, Cassava, Maize, Tomato
Total Disease Classes: 22
Total Images: 130,378 (Raw: 25,126 | Augmented: 105,252)

Author: ML Agriculture Team
Date: December 2025
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix, classification_report
import json

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))


class PlantDiseaseModel:
    """
    Multi-Crop Plant Disease Detection CNN Model
    
    Supports 22 disease classes across 4 crops:
    - Cashew (5 classes)
    - Cassava (5 classes)
    - Maize (7 classes)
    - Tomato (5 classes)
    """
    
    def __init__(self, img_size=(128, 128), num_classes=22):
        """
        Initialize the CNN model
        
        Args:
            img_size (tuple): Input image size (height, width)
            num_classes (int): Number of disease classes (22)
        """
        self.img_size = img_size
        self.num_classes = num_classes
        self.model = None
        self.history = None
        self.class_names = []
        
    def build_model(self):
        """
        Build custom CNN architecture optimized for plant disease detection
        
        Architecture:
        - 4 Convolutional blocks (32→64→128→256 filters)
        - Batch Normalization for stability
        - Dropout regularization (0.25-0.50)
        - Dense classification head (512→256→22)
        """
        print("\n" + "=" * 60)
        print("Building Custom CNN Model")
        print("=" * 60)
        
        model = models.Sequential([
            # Input layer
            layers.Input(shape=(self.img_size[0], self.img_size[1], 3)),
            
            # Block 1: 32 filters
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 2: 64 filters
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 3: 128 filters
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 4: 256 filters
            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Global pooling and dense layers
            layers.GlobalAveragePooling2D(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        
        print(f"\n✓ Model built successfully")
        print(f"  Input shape: {self.img_size[0]}x{self.img_size[1]}x3")
        print(f"  Output classes: {self.num_classes}")
        print(f"  Total parameters: {model.count_params():,}")
        
        return model
    
    def get_data_generators(self, data_dir, batch_size=128, validation_split=0.2):
        """
        Create data generators for training and validation
        
        Args:
            data_dir (str): Base directory containing dataset
            batch_size (int): Batch size for training
            validation_split (float): Validation split ratio
            
        Returns:
            tuple: (train_generator, val_generator, test_generator)
        """
        print("\n" + "=" * 60)
        print("Preparing Data Generators")
        print("=" * 60)
        
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest',
            validation_split=validation_split
        )
        
        # Only rescaling for validation/test
        test_datagen = ImageDataGenerator(
            rescale=1./255
        )
        
        # Check if data directories exist
        augmented_path = Path(data_dir) / 'Augmented Data'
        raw_path = Path(data_dir) / 'Raw Data'
        
        if not augmented_path.exists() or not raw_path.exists():
            print(f"\n⚠ ERROR: Dataset not found!")
            print(f"  Expected paths:")
            print(f"    - {augmented_path}")
            print(f"    - {raw_path}")
            print(f"\n  Please download the CCMT dataset from:")
            print(f"  https://www.kaggle.com/datasets/shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset")
            return None, None, None
        
        # Training generator (Augmented Data)
        print("\n📊 Loading Augmented Data for Training...")
        train_generator = train_datagen.flow_from_directory(
            augmented_path,
            target_size=self.img_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        # Validation generator (from Augmented Data)
        print("📊 Loading Augmented Data for Validation...")
        val_generator = train_datagen.flow_from_directory(
            augmented_path,
            target_size=self.img_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        # Test generator (Raw Data - unseen data)
        print("📊 Loading Raw Data for Testing...")
        test_generator = test_datagen.flow_from_directory(
            raw_path,
            target_size=self.img_size,
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
        # Store class names
        self.class_names = list(train_generator.class_indices.keys())
        
        print(f"\n✓ Data generators created successfully")
        print(f"  Training samples: {train_generator.samples:,}")
        print(f"  Validation samples: {val_generator.samples:,}")
        print(f"  Test samples: {test_generator.samples:,}")
        print(f"  Number of classes: {len(self.class_names)}")
        print(f"  Batch size: {batch_size}")
        
        return train_generator, val_generator, test_generator
    
    def train(self, train_gen, val_gen, epochs=50, model_save_path='../backend/saved_models'):
        """
        Train the model
        
        Args:
            train_gen: Training data generator
            val_gen: Validation data generator
            epochs (int): Number of training epochs
            model_save_path (str): Directory to save model
        """
        print("\n" + "=" * 60)
        print("Training Plant Disease Detection Model")
        print("=" * 60)
        
        # Create save directory
        os.makedirs(model_save_path, exist_ok=True)
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            ModelCheckpoint(
                os.path.join(model_save_path, 'plant_disease_best.keras'),
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        # Train model
        print(f"\n🚀 Starting training for {epochs} epochs...")
        print(f"   Using GPU: {len(tf.config.list_physical_devices('GPU')) > 0}")
        
        self.history = self.model.fit(
            train_gen,
            epochs=epochs,
            validation_data=val_gen,
            callbacks=callbacks,
            verbose=1
        )
        
        print("\n✓ Training completed!")
        
        # Save final model
        final_model_path = os.path.join(model_save_path, 'plant_disease_model.keras')
        self.model.save(final_model_path)
        print(f"✓ Model saved to: {final_model_path}")
        
        # Save class names
        class_names_path = os.path.join(model_save_path, 'plant_disease_classes.json')
        with open(class_names_path, 'w') as f:
            json.dump(self.class_names, f, indent=2)
        print(f"✓ Class names saved to: {class_names_path}")
        
        return self.history
    
    def evaluate(self, test_gen):
        """
        Evaluate model on test set
        
        Args:
            test_gen: Test data generator
            
        Returns:
            dict: Evaluation metrics
        """
        print("\n" + "=" * 60)
        print("Model Evaluation")
        print("=" * 60)
        
        # Get predictions
        print("\n📊 Generating predictions...")
        y_pred = self.model.predict(test_gen, verbose=1)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true = test_gen.classes
        
        # Calculate metrics
        test_loss, test_acc = self.model.evaluate(test_gen, verbose=0)
        
        print(f"\n📈 Test Results:")
        print(f"   Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
        print(f"   Test Loss: {test_loss:.4f}")
        
        # Classification report
        print("\n📋 Classification Report:")
        report = classification_report(
            y_true, 
            y_pred_classes, 
            target_names=self.class_names,
            digits=4
        )
        print(report)
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred_classes)
        
        return {
            'test_accuracy': test_acc,
            'test_loss': test_loss,
            'y_true': y_true,
            'y_pred': y_pred_classes,
            'confusion_matrix': cm,
            'classification_report': report
        }
    
    def plot_training_history(self, save_path='../backend/saved_models/training_history.png'):
        """Plot training history"""
        if self.history is None:
            print("⚠ No training history available")
            return
        
        print("\n📊 Plotting training history...")
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Accuracy plot
        axes[0].plot(self.history.history['accuracy'], label='Train Accuracy', linewidth=2)
        axes[0].plot(self.history.history['val_accuracy'], label='Val Accuracy', linewidth=2)
        axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Accuracy')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Loss plot
        axes[1].plot(self.history.history['loss'], label='Train Loss', linewidth=2)
        axes[1].plot(self.history.history['val_loss'], label='Val Loss', linewidth=2)
        axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Training history plot saved to: {save_path}")
        plt.close()
    
    def plot_confusion_matrix(self, cm, save_path='../backend/saved_models/confusion_matrix.png'):
        """Plot confusion matrix"""
        print("\n📊 Plotting confusion matrix...")
        
        plt.figure(figsize=(20, 16))
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=self.class_names,
            yticklabels=self.class_names,
            cbar_kws={'label': 'Count'}
        )
        plt.title('Confusion Matrix - Plant Disease Classification', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.ylabel('True Label', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Confusion matrix saved to: {save_path}")
        plt.close()


def main():
    """Main training pipeline"""
    print("\n" + "=" * 60)
    print("MULTI-CROP PLANT DISEASE DETECTION - MODEL TRAINING")
    print("=" * 60)
    print("\nDataset: CCMT Multi-Crop Plant Disease Detection Dataset")
    print("Source: https://www.kaggle.com/datasets/shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset")
    print("\nCrops: Cashew, Cassava, Maize, Tomato")
    print("Classes: 22 disease types")
    print("Total Images: 130,378")
    
    # Configuration
    IMG_SIZE = (128, 128)
    NUM_CLASSES = 22
    BATCH_SIZE = 128
    EPOCHS = 50
    DATA_DIR = '../data/plant_diseases'
    
    print(f"\nConfiguration:")
    print(f"  Image Size: {IMG_SIZE[0]}x{IMG_SIZE[1]}")
    print(f"  Batch Size: {BATCH_SIZE}")
    print(f"  Epochs: {EPOCHS}")
    print(f"  Data Directory: {DATA_DIR}")
    
    # Check if dataset exists
    if not os.path.exists(DATA_DIR):
        print(f"\n⚠ WARNING: Dataset directory not found: {DATA_DIR}")
        print(f"\n📥 Please download the CCMT dataset:")
        print(f"   1. Visit: https://www.kaggle.com/datasets/shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset")
        print(f"   2. Download the dataset")
        print(f"   3. Extract to: {os.path.abspath(DATA_DIR)}")
        print(f"\n   Expected structure:")
        print(f"   {DATA_DIR}/")
        print(f"   ├── Augmented Data/")
        print(f"   │   ├── Cashew/")
        print(f"   │   ├── Cassava/")
        print(f"   │   ├── Maize/")
        print(f"   │   └── Tomato/")
        print(f"   └── Raw Data/")
        print(f"       ├── Cashew/")
        print(f"       ├── Cassava/")
        print(f"       ├── Maize/")
        print(f"       └── Tomato/")
        return
    
    # Initialize model
    model = PlantDiseaseModel(img_size=IMG_SIZE, num_classes=NUM_CLASSES)
    
    # Build model
    model.build_model()
    
    # Display model summary
    print("\n" + "=" * 60)
    print("Model Architecture Summary")
    print("=" * 60)
    model.model.summary()
    
    # Prepare data
    train_gen, val_gen, test_gen = model.get_data_generators(
        DATA_DIR, 
        batch_size=BATCH_SIZE
    )
    
    if train_gen is None:
        return
    
    # Train model
    history = model.train(train_gen, val_gen, epochs=EPOCHS)
    
    # Plot training history
    model.plot_training_history()
    
    # Evaluate model
    results = model.evaluate(test_gen)
    
    # Plot confusion matrix
    model.plot_confusion_matrix(results['confusion_matrix'])
    
    print("\n" + "=" * 60)
    print("✓ TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n📊 Final Results:")
    print(f"   Test Accuracy: {results['test_accuracy']:.4f} ({results['test_accuracy']*100:.2f}%)")
    print(f"   Test Loss: {results['test_loss']:.4f}")
    
    print(f"\n📁 Saved Files:")
    print(f"   - Model: ../backend/saved_models/plant_disease_model.keras")
    print(f"   - Best Model: ../backend/saved_models/plant_disease_best.keras")
    print(f"   - Class Names: ../backend/saved_models/plant_disease_classes.json")
    print(f"   - Training History: ../backend/saved_models/training_history.png")
    print(f"   - Confusion Matrix: ../backend/saved_models/confusion_matrix.png")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
