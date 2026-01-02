"""
Data Preprocessing Utilities

Common preprocessing functions for crop recommendation system.

Author: ML Agriculture Team
Date: December 2025
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns


def load_and_validate_dataset(file_path):
    """
    Load and validate dataset
    
    Args:
        file_path (str): Path to CSV file
        
    Returns:
        pd.DataFrame: Validated dataset
    """
    print(f"Loading dataset from: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        print(f"✓ Dataset loaded successfully")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        
        # Check for missing values
        missing = df.isnull().sum()
        if missing.any():
            print("\n⚠ Warning: Missing values detected:")
            print(missing[missing > 0])
        else:
            print("✓ No missing values")
        
        return df
    
    except FileNotFoundError:
        print(f"✗ Error: File not found at {file_path}")
        raise
    except Exception as e:
        print(f"✗ Error loading dataset: {str(e)}")
        raise


def check_data_quality(df):
    """
    Perform data quality checks
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        dict: Quality metrics
    """
    quality_report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'duplicate_rows': df.duplicated().sum(),
        'data_types': df.dtypes.to_dict()
    }
    
    print("\n" + "=" * 60)
    print("Data Quality Report")
    print("=" * 60)
    print(f"Total Rows: {quality_report['total_rows']}")
    print(f"Total Columns: {quality_report['total_columns']}")
    print(f"Missing Values: {quality_report['missing_values']}")
    print(f"Duplicate Rows: {quality_report['duplicate_rows']}")
    
    return quality_report


def detect_outliers(df, columns, method='iqr', threshold=1.5):
    """
    Detect outliers in specified columns
    
    Args:
        df (pd.DataFrame): Input dataset
        columns (list): Columns to check
        method (str): Method to use ('iqr' or 'zscore')
        threshold (float): Threshold for outlier detection
        
    Returns:
        dict: Outlier information
    """
    outliers = {}
    
    for col in columns:
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - threshold * IQR
            upper = Q3 + threshold * IQR
            outlier_mask = (df[col] < lower) | (df[col] > upper)
            outliers[col] = {
                'count': outlier_mask.sum(),
                'percentage': (outlier_mask.sum() / len(df)) * 100,
                'lower_bound': lower,
                'upper_bound': upper
            }
        elif method == 'zscore':
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            outlier_mask = z_scores > threshold
            outliers[col] = {
                'count': outlier_mask.sum(),
                'percentage': (outlier_mask.sum() / len(df)) * 100
            }
    
    print("\n" + "=" * 60)
    print("Outlier Detection Report")
    print("=" * 60)
    for col, info in outliers.items():
        print(f"\n{col}:")
        print(f"  Outliers: {info['count']} ({info['percentage']:.2f}%)")
        if 'lower_bound' in info:
            print(f"  Bounds: [{info['lower_bound']:.2f}, {info['upper_bound']:.2f}]")
    
    return outliers


def plot_feature_distributions(df, features, save_path=None):
    """
    Plot distributions of numerical features
    
    Args:
        df (pd.DataFrame): Input dataset
        features (list): List of features to plot
        save_path (str): Path to save the plot
    """
    n_features = len(features)
    n_cols = 3
    n_rows = (n_features + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 4))
    axes = axes.flatten() if n_rows > 1 else [axes]
    
    for idx, feature in enumerate(features):
        ax = axes[idx]
        ax.hist(df[feature], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
        ax.set_title(f'{feature} Distribution', fontweight='bold')
        ax.set_xlabel(feature)
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)
        
        # Add statistics
        mean = df[feature].mean()
        median = df[feature].median()
        ax.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean:.2f}')
        ax.axvline(median, color='green', linestyle='--', linewidth=2, label=f'Median: {median:.2f}')
        ax.legend()
    
    # Hide unused subplots
    for idx in range(len(features), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Distribution plot saved to: {save_path}")
    else:
        plt.show()


def plot_correlation_matrix(df, features, save_path=None):
    """
    Plot correlation matrix
    
    Args:
        df (pd.DataFrame): Input dataset
        features (list): List of features
        save_path (str): Path to save the plot
    """
    corr_matrix = df[features].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        fmt='.2f', 
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8}
    )
    plt.title('Feature Correlation Matrix', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Correlation matrix saved to: {save_path}")
    else:
        plt.show()


def normalize_features(X_train, X_test=None):
    """
    Normalize features using StandardScaler
    
    Args:
        X_train: Training features
        X_test: Test features (optional)
        
    Returns:
        tuple: (X_train_scaled, X_test_scaled, scaler)
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled, scaler
    
    return X_train_scaled, scaler


def encode_labels(y_train, y_test=None):
    """
    Encode categorical labels
    
    Args:
        y_train: Training labels
        y_test: Test labels (optional)
        
    Returns:
        tuple: (y_train_encoded, y_test_encoded, encoder) or (y_train_encoded, encoder)
    """
    encoder = LabelEncoder()
    y_train_encoded = encoder.fit_transform(y_train)
    
    if y_test is not None:
        y_test_encoded = encoder.transform(y_test)
        return y_train_encoded, y_test_encoded, encoder
    
    return y_train_encoded, encoder


def balance_dataset(X, y, method='oversample'):
    """
    Balance imbalanced dataset
    
    Args:
        X: Features
        y: Labels
        method: 'oversample', 'undersample', or 'smote'
        
    Returns:
        tuple: (X_balanced, y_balanced)
    """
    from collections import Counter
    
    print(f"\nOriginal class distribution:")
    print(Counter(y))
    
    if method == 'oversample':
        from imblearn.over_sampling import RandomOverSampler
        sampler = RandomOverSampler(random_state=42)
    elif method == 'undersample':
        from imblearn.under_sampling import RandomUnderSampler
        sampler = RandomUnderSampler(random_state=42)
    elif method == 'smote':
        from imblearn.over_sampling import SMOTE
        sampler = SMOTE(random_state=42)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    X_balanced, y_balanced = sampler.fit_resample(X, y)
    
    print(f"\nBalanced class distribution:")
    print(Counter(y_balanced))
    
    return X_balanced, y_balanced


def create_train_val_test_split(X, y, train_size=0.7, val_size=0.15, test_size=0.15, random_state=42):
    """
    Create train, validation, and test splits
    
    Args:
        X: Features
        y: Labels
        train_size: Proportion for training
        val_size: Proportion for validation
        test_size: Proportion for testing
        random_state: Random seed
        
    Returns:
        tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    from sklearn.model_selection import train_test_split
    
    # First split: separate test set
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Second split: separate train and validation
    val_size_adjusted = val_size / (train_size + val_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size_adjusted, random_state=random_state, stratify=y_temp
    )
    
    print("\nDataset Split:")
    print(f"  Training:   {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"  Validation: {len(X_val)} samples ({len(X_val)/len(X)*100:.1f}%)")
    print(f"  Testing:    {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


# Example usage
if __name__ == "__main__":
    print("Data Preprocessing Utilities Module")
    print("=" * 60)
    print("\nAvailable functions:")
    print("  - load_and_validate_dataset()")
    print("  - check_data_quality()")
    print("  - detect_outliers()")
    print("  - plot_feature_distributions()")
    print("  - plot_correlation_matrix()")
    print("  - normalize_features()")
    print("  - encode_labels()")
    print("  - balance_dataset()")
    print("  - create_train_val_test_split()")
    print("\n✓ Module loaded successfully!")
