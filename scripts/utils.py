"""
Utility functions for data science workflows.
"""

import os
import sys
import logging
import subprocess
import shlex
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
    Get path to data file with path traversal protection.
    
    Args:
        filename: Name of the data file
        data_type: Type of data (raw, processed, external)
        
    Returns:
        Path to data file
        
    Raises:
        ValueError: If path traversal attempt is detected
    """
    # Validate data_type is in allowed list
    allowed_data_types = ["raw", "processed", "external"]
    if data_type not in allowed_data_types:
        raise ValueError(f"Invalid data_type. Must be one of: {allowed_data_types}")
    
    # Build base directory
    base_dir = get_project_root() / "data" / data_type
    base_dir_resolved = base_dir.resolve()
    
    # Resolve target path and ensure it's within base directory
    target_path = (base_dir / filename).resolve()
    
    # Check for path traversal
    try:
        target_path.relative_to(base_dir_resolved)
    except ValueError:
        raise ValueError(f"Path traversal attempt detected: {filename}")
    
    return target_path

def get_output_path(filename: str, output_type: str = "figures") -> Path:
    """
    Get path to output file with path traversal protection.
    
    Args:
        filename: Name of the output file
        output_type: Type of output (figures, models, reports)
        
    Returns:
        Path to output file
        
    Raises:
        ValueError: If path traversal attempt is detected
    """
    # Validate output_type is in allowed list
    allowed_output_types = ["figures", "models", "reports"]
    if output_type not in allowed_output_types:
        raise ValueError(f"Invalid output_type. Must be one of: {allowed_output_types}")
    
    # Build base directory
    output_dir = get_project_root() / "outputs" / output_type
    output_dir_resolved = output_dir.resolve()
    
    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Resolve target path and ensure it's within base directory
    target_path = (output_dir / filename).resolve()
    
    # Check for path traversal
    try:
        target_path.relative_to(output_dir_resolved)
    except ValueError:
        raise ValueError(f"Path traversal attempt detected: {filename}")
    
    return target_path

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

# Security utilities for command execution

def clear_terminal() -> None:
    """
    Safely clear the terminal screen without command injection risk.
    
    Uses subprocess with argument list instead of os.system to prevent
    command injection vulnerabilities (CWE-77, CWE-78, CWE-88).
    """
    if os.name == 'nt':  # Windows
        subprocess.run(['cmd', '/c', 'cls'], check=False)
    else:  # Unix/Linux/MacOS
        subprocess.run(['clear'], check=False)

def safe_subprocess_run(
    command: List[str],
    capture_output: bool = True,
    text: bool = True,
    check: bool = True,
    timeout: Optional[int] = 30,
    **kwargs
) -> subprocess.CompletedProcess:
    """
    Execute a subprocess command safely without shell injection risk.
    
    This function enforces secure subprocess execution by:
    - Using argument lists instead of shell strings
    - Never using shell=True
    - Implementing timeout protection
    - Validating command structure
    
    Args:
        command: List of command and arguments (e.g., ['ls', '-la', '/tmp'])
        capture_output: Whether to capture stdout and stderr
        text: Return output as text (string) instead of bytes
        check: Raise CalledProcessError if command returns non-zero exit code
        timeout: Maximum seconds to wait for command completion
        **kwargs: Additional arguments passed to subprocess.run
        
    Returns:
        CompletedProcess instance with returncode, stdout, stderr
        
    Raises:
        ValueError: If command is not a list or is empty
        subprocess.CalledProcessError: If check=True and command fails
        subprocess.TimeoutExpired: If command exceeds timeout
        
    Security:
        - Prevents CWE-77: Command Injection
        - Prevents CWE-78: OS Command Injection
        - Prevents CWE-88: Argument Injection
        
    Example:
        >>> result = safe_subprocess_run(['echo', 'Hello World'])
        >>> print(result.stdout)
        Hello World
    """
    # Validate command is a list
    if not isinstance(command, list):
        raise ValueError("Command must be a list of arguments, not a string")
    
    if len(command) == 0:
        raise ValueError("Command list cannot be empty")
    
    # Validate all arguments are strings
    if not all(isinstance(arg, str) for arg in command):
        raise ValueError("All command arguments must be strings")
    
    # Execute safely without shell
    return subprocess.run(
        command,
        capture_output=capture_output,
        text=text,
        check=check,
        timeout=timeout,
        shell=False,  # Critical: Never use shell=True
        **kwargs
    )

def validate_command_argument(arg: str, allowed_chars: str = "a-zA-Z0-9._/-") -> bool:
    """
    Validate that a command argument contains only allowed characters.
    
    Args:
        arg: Argument to validate
        allowed_chars: Regex character class of allowed characters
        
    Returns:
        True if valid, False otherwise
        
    Example:
        >>> validate_command_argument("safe_file.txt")
        True
        >>> validate_command_argument("dangerous; rm -rf /")
        False
    """
    import re
    # Escape special regex characters in allowed_chars
    pattern = f"^[{allowed_chars}]+$"
    return bool(re.match(pattern, arg))

def sanitize_for_shell(value: str) -> str:
    """
    Sanitize a string for safe use in shell commands using shlex.quote().
    
    This should only be used when shell=True is absolutely necessary.
    Prefer using safe_subprocess_run() with argument lists instead.
    
    Args:
        value: String to sanitize
        
    Returns:
        Safely quoted string for shell use
        
    Example:
        >>> sanitize_for_shell("file with spaces.txt")
        "'file with spaces.txt'"
    """
    return shlex.quote(value)