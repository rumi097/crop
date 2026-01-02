"""
Training Script for CNN-based Fertilizer Disease Recognition Model

This script trains a Convolutional Neural Network for classifying fertilizer
images into categories: Healthy, Contaminated, Expired, Fake, Damaged.

Author: ML Agriculture Team
Date: December 2025
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
from sklearn.metrics import classification_report, confusion_matrix

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models.disease_recognition import FertilizerDiseaseRecognitionModel


def create_sample_dataset(base_dir='../data/fertilizer_images'):
    """
    Create sample image dataset structure for demonstration
    
    In production, you should:
    1. Collect real fertilizer images for each category
    2. Use data augmentation to increase dataset size
    3. Ensure balanced classes
    
    Dataset structure:
    fertilizer_images/
    ├── train/
    │   ├── Healthy/
    │   ├── Contaminated/
    │   ├── Expired/
    │   ├── Fake/
    │   └── Damaged/
    └── val/
        ├── Healthy/
        ├── Contaminated/
        ├── Expired/
        ├── Fake/
        └── Damaged/
    """
    print("=" * 60)
    print("Setting Up Image Dataset Structure")
    print("=" * 60)
    
    categories = ['Healthy', 'Contaminated', 'Expired', 'Fake', 'Damaged']
    
    # Create directories
    for split in ['train', 'val']:
        for category in categories:
            dir_path = os.path.join(base_dir, split, category)
            os.makedirs(dir_path, exist_ok=True)
    
    print(f"\n✓ Dataset directory structure created at: {base_dir}")
    print("\n📁 Directory structure:")
    print(f"{base_dir}/")
    print("├── train/")
    for cat in categories:
        print(f"│   ├── {cat}/")
    print("└── val/")
    for cat in categories:
        print(f"    ├── {cat}/")
    
    # Check if images exist
    train_dir = os.path.join(base_dir, 'train')
    total_images = sum([len(files) for _, _, files in os.walk(train_dir)])
    
    if total_images == 0:
        print("\n⚠ WARNING: No images found in dataset directories!")
        print("\nTo train the model, please:")
        print("1. Collect fertilizer images for each category")
        print("2. Place images in respective folders:")
        for cat in categories:
            print(f"   - {cat}: Images of {cat.lower()} fertilizer")
        print("\nRecommended dataset sources:")
        print("- Kaggle agricultural image datasets")
        print("- PlantVillage dataset (can be adapted)")
        print("- Custom collected images from fertilizer samples")
        print("\nMinimum recommended images per category:")
        print("- Training: 500+ images per class")
        print("- Validation: 100+ images per class")
        
        return False
    
    print(f"\n✓ Found {total_images} images in training directory")
    return True


def plot_sample_images(data_generator, save_path):
    """Plot sample images from dataset"""
    print("\nGenerating sample images visualization...")
    
    # Get a batch of images
    images, labels = next(data_generator)
    
    # Plot first 9 images
    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    fig.suptitle('Sample Training Images', fontsize=16, fontweight='bold')
    
    class_names = list(data_generator.class_indices.keys())
    
    for idx in range(9):
        if idx >= len(images):
            break
        
        ax = axes[idx // 3, idx % 3]
        ax.imshow(images[idx])
        
        # Get class label
        label_idx = np.argmax(labels[idx])
        class_name = class_names[label_idx]
        
        ax.set_title(f'Class: {class_name}')
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Sample images saved to: {save_path}")


def plot_class_distribution(train_dir, save_path):
    """Plot class distribution"""
    print("\nAnalyzing class distribution...")
    
    categories = ['Healthy', 'Contaminated', 'Expired', 'Fake', 'Damaged']
    counts = []
    
    for category in categories:
        cat_dir = os.path.join(train_dir, category)
        if os.path.exists(cat_dir):
            count = len([f for f in os.listdir(cat_dir) 
                        if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            counts.append(count)
        else:
            counts.append(0)
    
    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, counts, color=['green', 'orange', 'red', 'purple', 'brown'])
    plt.title('Class Distribution in Training Dataset', fontsize=14, fontweight='bold')
    plt.xlabel('Fertilizer Condition')
    plt.ylabel('Number of Images')
    plt.xticks(rotation=45)
    
    # Add count labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Class distribution plot saved to: {save_path}")
    
    return dict(zip(categories, counts))


def plot_training_results(history, save_path):
    """Plot training history"""
    history_dict = history['history']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Training Results', fontsize=16, fontweight='bold')
    
    # Accuracy
    axes[0, 0].plot(history_dict['accuracy'], label='Train', marker='o')
    axes[0, 0].plot(history_dict['val_accuracy'], label='Validation', marker='s')
    axes[0, 0].set_title('Model Accuracy')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Loss
    axes[0, 1].plot(history_dict['loss'], label='Train', marker='o')
    axes[0, 1].plot(history_dict['val_loss'], label='Validation', marker='s')
    axes[0, 1].set_title('Model Loss')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Loss')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Precision
    axes[1, 0].plot(history_dict['precision'], label='Train', marker='o')
    axes[1, 0].plot(history_dict['val_precision'], label='Validation', marker='s')
    axes[1, 0].set_title('Model Precision')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Precision')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Recall
    axes[1, 1].plot(history_dict['recall'], label='Train', marker='o')
    axes[1, 1].plot(history_dict['val_recall'], label='Validation', marker='s')
    axes[1, 1].set_title('Model Recall')
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Recall')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Training results plot saved to: {save_path}")


def main():
    """Main training pipeline"""
    print("\n" + "=" * 60)
    print("FERTILIZER DISEASE RECOGNITION MODEL TRAINING")
    print("=" * 60)
    
    # Configuration
    IMG_SIZE = (224, 224)
    BATCH_SIZE = 32
    EPOCHS = 50
    NUM_CLASSES = 5
    
    # Step 1: Setup dataset
    base_dir = '../data/fertilizer_images'
    dataset_ready = create_sample_dataset(base_dir)
    
    if not dataset_ready:
        print("\n" + "=" * 60)
        print("⚠ Dataset not ready. Please add images and try again.")
        print("=" * 60)
        
        # Create a demo model for structure
        print("\nCreating model architecture for reference...")
        model = FertilizerDiseaseRecognitionModel(
            img_size=IMG_SIZE,
            num_classes=NUM_CLASSES,
            use_pretrained=True
        )
        model.build_model()
        model.get_model_summary()
        
        # Save model architecture diagram
        try:
            tf.keras.utils.plot_model(
                model.model,
                to_file='../backend/saved_models/cnn_architecture.png',
                show_shapes=True,
                show_layer_names=True,
                rankdir='TB',
                expand_nested=True
            )
            print("✓ Model architecture diagram saved")
        except:
            print("ℹ Could not save model architecture diagram (graphviz not installed)")
        
        return
    
    # Step 2: Analyze dataset
    train_dir = os.path.join(base_dir, 'train')
    val_dir = os.path.join(base_dir, 'val')
    
    class_distribution = plot_class_distribution(
        train_dir,
        '../backend/saved_models/fertilizer_class_distribution.png'
    )
    
    print("\nClass Distribution:")
    for cls, count in class_distribution.items():
        print(f"  {cls:15s}: {count} images")
    
    # Step 3: Initialize model
    print("\n" + "=" * 60)
    print("Initializing Model")
    print("=" * 60)
    
    model = FertilizerDiseaseRecognitionModel(
        img_size=IMG_SIZE,
        num_classes=NUM_CLASSES,
        use_pretrained=True  # Use transfer learning
    )
    
    model.build_model()
    model.get_model_summary()
    
    # Step 4: Create data generators
    print("\n" + "=" * 60)
    print("Creating Data Generators")
    print("=" * 60)
    
    train_generator, val_generator = model.create_data_generators(
        train_dir=train_dir,
        val_dir=val_dir,
        batch_size=BATCH_SIZE
    )
    
    print(f"\n✓ Training generator: {train_generator.samples} samples")
    print(f"✓ Validation generator: {val_generator.samples} samples")
    print(f"✓ Batch size: {BATCH_SIZE}")
    print(f"✓ Classes: {model.class_names}")
    
    # Plot sample images
    plot_sample_images(
        train_generator,
        '../backend/saved_models/fertilizer_sample_images.png'
    )
    
    # Step 5: Train model
    print("\n" + "=" * 60)
    print("Training Model")
    print("=" * 60)
    
    results = model.train(
        train_generator=train_generator,
        val_generator=val_generator,
        epochs=EPOCHS,
        model_save_path='../backend/saved_models/fertilizer_cnn_model.h5'
    )
    
    # Step 6: Plot training results
    plot_training_results(
        results,
        '../backend/saved_models/fertilizer_training_results.png'
    )
    
    # Step 7: Save model
    print("\n" + "=" * 60)
    print("Saving Model")
    print("=" * 60)
    model.save_model('../backend/saved_models/fertilizer_cnn_model.h5')
    
    # Step 8: Summary
    print("\n" + "=" * 60)
    print("✓ TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nModel Performance:")
    print(f"  Validation Accuracy:  {results['val_accuracy']:.4f} ({results['val_accuracy']*100:.2f}%)")
    print(f"  Validation Precision: {results['val_precision']:.4f}")
    print(f"  Validation Recall:    {results['val_recall']:.4f}")
    
    f1_score = 2 * (results['val_precision'] * results['val_recall']) / \
               (results['val_precision'] + results['val_recall'])
    print(f"  F1-Score:            {f1_score:.4f}")
    
    print("\nModel files saved in: ../backend/saved_models/")
    print("  - fertilizer_cnn_model.h5")
    print("  - fertilizer_cnn_model_classes.json")
    
    print("\nVisualization files:")
    print("  - fertilizer_class_distribution.png")
    print("  - fertilizer_sample_images.png")
    print("  - fertilizer_training_results.png")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Set random seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)
    
    main()
