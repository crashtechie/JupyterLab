"""
Utility functions for data science workflows.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import pandas as pd
import numpy as np

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=log_file
    )
    return logging.getLogger(__name__)

def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path to project root
    """
    return Path(__file__).parent.parent

def get_data_path(filename: str, data_type: str = "raw") -> Path:
    """
    Get path to data file.
    
    Args:
        filename: Name of the data file
        data_type: Type of data (raw, processed, external)
        
    Returns:
        Path to data file
    """
    return get_project_root() / "data" / data_type / filename

def get_output_path(filename: str, output_type: str = "figures") -> Path:
    """
    Get path to output file.
    
    Args:
        filename: Name of the output file
        output_type: Type of output (figures, models, reports)
        
    Returns:
        Path to output file
    """
    output_dir = get_project_root() / "outputs" / output_type
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / filename

def load_config(config_file: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from JSON file.
    
    Args:
        config_file: Name of configuration file
        
    Returns:
        Configuration dictionary
    """
    import json
    config_path = get_project_root() / config_file
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

def save_dataframe(df: pd.DataFrame, filename: str, data_type: str = "processed", **kwargs) -> None:
    """
    Save DataFrame to file with automatic format detection.
    
    Args:
        df: DataFrame to save
        filename: Output filename
        data_type: Type of data directory
        **kwargs: Additional arguments for pandas save methods
    """
    file_path = get_data_path(filename, data_type)
    
    # Create directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Determine file format from extension
    suffix = file_path.suffix.lower()
    
    if suffix == '.csv':
        df.to_csv(file_path, index=False, **kwargs)
    elif suffix == '.parquet':
        df.to_parquet(file_path, index=False, **kwargs)
    elif suffix in ['.xlsx', '.xls']:
        df.to_excel(file_path, index=False, **kwargs)
    elif suffix == '.json':
        df.to_json(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

def load_dataframe(filename: str, data_type: str = "raw", **kwargs) -> pd.DataFrame:
    """
    Load DataFrame from file with automatic format detection.
    
    Args:
        filename: Input filename
        data_type: Type of data directory
        **kwargs: Additional arguments for pandas load methods
        
    Returns:
        Loaded DataFrame
    """
    file_path = get_data_path(filename, data_type)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    # Determine file format from extension
    suffix = file_path.suffix.lower()
    
    if suffix == '.csv':
        return pd.read_csv(file_path, **kwargs)
    elif suffix == '.parquet':
        return pd.read_parquet(file_path, **kwargs)
    elif suffix in ['.xlsx', '.xls']:
        return pd.read_excel(file_path, **kwargs)
    elif suffix == '.json':
        return pd.read_json(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

def memory_usage(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get memory usage information for a DataFrame.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with memory usage statistics
    """
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    return {
        'total_memory_mb': round(memory_mb, 2),
        'shape': df.shape,
        'dtypes': df.dtypes.value_counts().to_dict(),
        'null_counts': df.isnull().sum().sum(),
        'duplicate_rows': df.duplicated().sum()
    }

def print_dataframe_info(df: pd.DataFrame, name: str = "DataFrame") -> None:
    """
    Print comprehensive information about a DataFrame.
    
    Args:
        df: DataFrame to analyze
        name: Name of the DataFrame for display
    """
    print(f"\n=== {name} Information ===")
    print(f"Shape: {df.shape}")
    print(f"Memory Usage: {memory_usage(df)['total_memory_mb']} MB")
    print(f"Null Values: {df.isnull().sum().sum()}")
    print(f"Duplicate Rows: {df.duplicated().sum()}")
    
    print(f"\nData Types:")
    print(df.dtypes.value_counts())
    
    print(f"\nFirst few rows:")
    print(df.head())
    
    print(f"\nBasic Statistics:")
    print(df.describe())