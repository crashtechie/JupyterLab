"""
Data processing utilities for data science workflows.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names by removing spaces, special characters, and converting to lowercase.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with cleaned column names
    """
    df_cleaned = df.copy()
    
    # Clean column names
    df_cleaned.columns = (df_cleaned.columns
                         .str.strip()
                         .str.lower()
                         .str.replace(r'[^\w\s]', '', regex=True)
                         .str.replace(r'\s+', '_', regex=True))
    
    return df_cleaned

def handle_missing_values(df: pd.DataFrame, 
                         strategy: str = "drop",
                         columns: Optional[List[str]] = None,
                         fill_value: Any = None) -> pd.DataFrame:
    """
    Handle missing values in DataFrame.
    
    Args:
        df: Input DataFrame
        strategy: Strategy for handling missing values (drop, mean, median, mode, forward_fill, back_fill, custom)
        columns: Specific columns to process (if None, process all)
        fill_value: Custom fill value when strategy is 'custom'
        
    Returns:
        DataFrame with missing values handled
    """
    df_processed = df.copy()
    
    if columns is None:
        columns = df_processed.columns
    
    if strategy == "drop":
        df_processed = df_processed.dropna(subset=columns)
    elif strategy == "mean":
        for col in columns:
            if df_processed[col].dtype in ['int64', 'float64']:
                df_processed[col] = df_processed[col].fillna(df_processed[col].mean())
    elif strategy == "median":
        for col in columns:
            if df_processed[col].dtype in ['int64', 'float64']:
                df_processed[col] = df_processed[col].fillna(df_processed[col].median())
    elif strategy == "mode":
        for col in columns:
            mode_value = df_processed[col].mode()
            if len(mode_value) > 0:
                df_processed[col] = df_processed[col].fillna(mode_value[0])
    elif strategy == "forward_fill":
        df_processed[columns] = df_processed[columns].fillna(method='ffill')
    elif strategy == "back_fill":
        df_processed[columns] = df_processed[columns].fillna(method='bfill')
    elif strategy == "custom":
        df_processed[columns] = df_processed[columns].fillna(fill_value)
    
    return df_processed

def encode_categorical_variables(df: pd.DataFrame, 
                               columns: Optional[List[str]] = None,
                               method: str = "label") -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Encode categorical variables.
    
    Args:
        df: Input DataFrame
        columns: Columns to encode (if None, auto-detect categorical columns)
        method: Encoding method ('label', 'onehot')
        
    Returns:
        Tuple of (encoded DataFrame, encoders dictionary)
    """
    df_encoded = df.copy()
    encoders = {}
    
    if columns is None:
        columns = df_encoded.select_dtypes(include=['object', 'category']).columns
    
    if method == "label":
        for col in columns:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            encoders[col] = le
    elif method == "onehot":
        df_encoded = pd.get_dummies(df_encoded, columns=columns, prefix=columns)
        encoders['columns'] = columns
        encoders['method'] = 'onehot'
    
    return df_encoded, encoders

def scale_features(df: pd.DataFrame, 
                  columns: Optional[List[str]] = None,
                  method: str = "standard") -> Tuple[pd.DataFrame, Any]:
    """
    Scale numerical features.
    
    Args:
        df: Input DataFrame
        columns: Columns to scale (if None, auto-detect numerical columns)
        method: Scaling method ('standard', 'minmax')
        
    Returns:
        Tuple of (scaled DataFrame, scaler object)
    """
    df_scaled = df.copy()
    
    if columns is None:
        columns = df_scaled.select_dtypes(include=[np.number]).columns
    
    if method == "standard":
        scaler = StandardScaler()
    elif method == "minmax":
        scaler = MinMaxScaler()
    else:
        raise ValueError("Method must be 'standard' or 'minmax'")
    
    df_scaled[columns] = scaler.fit_transform(df_scaled[columns])
    
    return df_scaled, scaler

def detect_outliers(df: pd.DataFrame, 
                   columns: Optional[List[str]] = None,
                   method: str = "iqr") -> pd.DataFrame:
    """
    Detect outliers in numerical columns.
    
    Args:
        df: Input DataFrame
        columns: Columns to check (if None, check all numerical columns)
        method: Method for outlier detection ('iqr', 'zscore')
        
    Returns:
        DataFrame with outlier indicators
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns
    
    outlier_df = pd.DataFrame(index=df.index)
    
    for col in columns:
        if method == "iqr":
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outlier_df[f"{col}_outlier"] = (df[col] < lower_bound) | (df[col] > upper_bound)
        elif method == "zscore":
            from scipy import stats
            z_scores = np.abs(stats.zscore(df[col]))
            outlier_df[f"{col}_outlier"] = z_scores > 3
    
    return outlier_df

def split_data(df: pd.DataFrame, 
               target_column: str,
               test_size: float = 0.2,
               validation_size: float = 0.1,
               random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    """
    Split data into train, validation, and test sets.
    
    Args:
        df: Input DataFrame
        target_column: Name of target column
        test_size: Proportion of test set
        validation_size: Proportion of validation set
        random_state: Random state for reproducibility
        
    Returns:
        Tuple of (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # First split: separate test set
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y if y.dtype == 'object' else None
    )
    
    # Second split: separate train and validation from remaining data
    val_size_adjusted = validation_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size_adjusted, random_state=random_state,
        stratify=y_temp if y_temp.dtype == 'object' else None
    )
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def create_feature_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a summary of features in the DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Summary DataFrame with feature statistics
    """
    summary_data = []
    
    for col in df.columns:
        col_info = {
            'column': col,
            'dtype': str(df[col].dtype),
            'null_count': df[col].isnull().sum(),
            'null_percentage': round((df[col].isnull().sum() / len(df)) * 100, 2),
            'unique_count': df[col].nunique(),
            'unique_percentage': round((df[col].nunique() / len(df)) * 100, 2)
        }
        
        if df[col].dtype in ['int64', 'float64']:
            col_info.update({
                'mean': round(df[col].mean(), 4),
                'std': round(df[col].std(), 4),
                'min': df[col].min(),
                'max': df[col].max()
            })
        else:
            most_common = df[col].value_counts().index[0] if len(df[col].value_counts()) > 0 else None
            col_info.update({
                'most_common': most_common,
                'most_common_freq': df[col].value_counts().iloc[0] if len(df[col].value_counts()) > 0 else 0
            })
        
        summary_data.append(col_info)
    
    return pd.DataFrame(summary_data)