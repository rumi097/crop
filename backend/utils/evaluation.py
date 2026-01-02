"""
Model Evaluation Utilities

Functions for evaluating ML model performance.

Author: ML Agriculture Team
Date: December 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc,
    precision_recall_curve, average_precision_score
)
from sklearn.preprocessing import label_binarize
import pandas as pd


def calculate_metrics(y_true, y_pred, average='weighted'):
    """
    Calculate comprehensive classification metrics
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        average: Averaging method for multi-class metrics
        
    Returns:
        dict: Dictionary of metrics
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average=average, zero_division=0),
        'recall': recall_score(y_true, y_pred, average=average, zero_division=0),
        'f1_score': f1_score(y_true, y_pred, average=average, zero_division=0)
    }
    
    return metrics


def print_evaluation_report(y_true, y_pred, class_names=None):
    """
    Print comprehensive evaluation report
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        class_names: List of class names
    """
    print("\n" + "=" * 60)
    print("MODEL EVALUATION REPORT")
    print("=" * 60)
    
    # Overall metrics
    metrics = calculate_metrics(y_true, y_pred)
    
    print("\n📊 Overall Metrics:")
    print(f"  Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  F1-Score:  {metrics['f1_score']:.4f}")
    
    # Classification report
    print("\n📋 Detailed Classification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names, zero_division=0))
    
    return metrics


def plot_confusion_matrix(y_true, y_pred, class_names=None, normalize=False, save_path=None):
    """
    Plot confusion matrix
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        class_names: List of class names
        normalize: Whether to normalize the matrix
        save_path: Path to save the plot
    """
    cm = confusion_matrix(y_true, y_pred)
    
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        fmt = '.2f'
        title = 'Normalized Confusion Matrix'
    else:
        fmt = 'd'
        title = 'Confusion Matrix'
    
    plt.figure(figsize=(max(10, len(class_names) if class_names else 10), 
                        max(8, len(class_names) if class_names else 8)))
    
    sns.heatmap(
        cm, 
        annot=True, 
        fmt=fmt, 
        cmap='Blues',
        xticklabels=class_names if class_names else 'auto',
        yticklabels=class_names if class_names else 'auto',
        cbar_kws={'label': 'Count' if not normalize else 'Proportion'}
    )
    
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    
    if class_names and len(class_names) > 10:
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Confusion matrix saved to: {save_path}")
    else:
        plt.show()
    
    return cm


def plot_roc_curves(y_true, y_pred_proba, class_names, save_path=None):
    """
    Plot ROC curves for multi-class classification
    
    Args:
        y_true: True labels (must be numeric)
        y_pred_proba: Predicted probabilities
        class_names: List of class names
        save_path: Path to save the plot
    """
    n_classes = len(class_names)
    
    # Binarize the labels
    y_true_bin = label_binarize(y_true, classes=range(n_classes))
    
    # Compute ROC curve and AUC for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_pred_proba[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    # Plot
    plt.figure(figsize=(12, 8))
    colors = plt.cm.get_cmap('tab10', n_classes)
    
    for i in range(min(n_classes, 10)):  # Plot max 10 classes
        plt.plot(
            fpr[i], tpr[i], 
            color=colors(i), 
            lw=2,
            label=f'{class_names[i]} (AUC = {roc_auc[i]:.2f})'
        )
    
    plt.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curves - Multi-class Classification', fontsize=16, fontweight='bold')
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ ROC curves saved to: {save_path}")
    else:
        plt.show()


def plot_precision_recall_curve(y_true, y_pred_proba, class_idx, class_name, save_path=None):
    """
    Plot precision-recall curve for a specific class
    
    Args:
        y_true: True labels (binary: 0 or 1)
        y_pred_proba: Predicted probabilities for the positive class
        class_idx: Index of the class
        class_name: Name of the class
        save_path: Path to save the plot
    """
    precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
    avg_precision = average_precision_score(y_true, y_pred_proba)
    
    plt.figure(figsize=(10, 6))
    plt.plot(recall, precision, lw=2, label=f'Precision-Recall curve (AP = {avg_precision:.2f})')
    plt.xlabel('Recall', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.title(f'Precision-Recall Curve - {class_name}', fontsize=16, fontweight='bold')
    plt.legend(loc="lower left", fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Precision-recall curve saved to: {save_path}")
    else:
        plt.show()


def plot_feature_importance(feature_names, importance_scores, top_n=10, save_path=None):
    """
    Plot feature importance
    
    Args:
        feature_names: List of feature names
        importance_scores: Importance scores
        top_n: Number of top features to display
        save_path: Path to save the plot
    """
    # Create DataFrame and sort
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance_scores
    }).sort_values('importance', ascending=False)
    
    # Select top N features
    top_features = importance_df.head(top_n)
    
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(top_features)), top_features['importance'], color='steelblue')
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Importance Score', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.title(f'Top {top_n} Feature Importance', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Feature importance plot saved to: {save_path}")
    else:
        plt.show()


def plot_learning_curves(train_scores, val_scores, metric_name='Accuracy', save_path=None):
    """
    Plot learning curves
    
    Args:
        train_scores: Training scores over epochs
        val_scores: Validation scores over epochs
        metric_name: Name of the metric
        save_path: Path to save the plot
    """
    epochs = range(1, len(train_scores) + 1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(epochs, train_scores, 'b-', label=f'Training {metric_name}', marker='o')
    plt.plot(epochs, val_scores, 'r-', label=f'Validation {metric_name}', marker='s')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel(metric_name, fontsize=12)
    plt.title(f'Learning Curves - {metric_name}', fontsize=16, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Learning curves saved to: {save_path}")
    else:
        plt.show()


def calculate_per_class_metrics(y_true, y_pred, class_names):
    """
    Calculate metrics for each class
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        class_names: List of class names
        
    Returns:
        pd.DataFrame: DataFrame with per-class metrics
    """
    precision = precision_score(y_true, y_pred, average=None, zero_division=0)
    recall = recall_score(y_true, y_pred, average=None, zero_division=0)
    f1 = f1_score(y_true, y_pred, average=None, zero_division=0)
    
    # Calculate support (number of samples per class)
    support = np.bincount(y_true, minlength=len(class_names))
    
    metrics_df = pd.DataFrame({
        'Class': class_names,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'Support': support
    })
    
    print("\n📊 Per-Class Metrics:")
    print(metrics_df.to_string(index=False))
    
    return metrics_df


def compare_models(models_results, metric='accuracy', save_path=None):
    """
    Compare multiple models
    
    Args:
        models_results: Dictionary {model_name: metrics_dict}
        metric: Metric to compare
        save_path: Path to save the plot
    """
    model_names = list(models_results.keys())
    metric_values = [results[metric] for results in models_results.values()]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(model_names, metric_values, color='steelblue', edgecolor='black')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2., height,
            f'{height:.4f}',
            ha='center', va='bottom', fontweight='bold'
        )
    
    plt.xlabel('Model', fontsize=12)
    plt.ylabel(metric.capitalize(), fontsize=12)
    plt.title(f'Model Comparison - {metric.capitalize()}', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Model comparison plot saved to: {save_path}")
    else:
        plt.show()


# Example usage
if __name__ == "__main__":
    print("Model Evaluation Utilities Module")
    print("=" * 60)
    print("\nAvailable functions:")
    print("  - calculate_metrics()")
    print("  - print_evaluation_report()")
    print("  - plot_confusion_matrix()")
    print("  - plot_roc_curves()")
    print("  - plot_precision_recall_curve()")
    print("  - plot_feature_importance()")
    print("  - plot_learning_curves()")
    print("  - calculate_per_class_metrics()")
    print("  - compare_models()")
    print("\n✓ Module loaded successfully!")
