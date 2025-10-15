"""
Data processing utilities for data science workflows.

Security Features:
- Role-based access control (RBAC)
- Authentication decorators
- Session management
- Audit logging for sensitive operations
- CWE-285 Authorization Bypass prevention
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Callable
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from functools import wraps
from datetime import datetime
import os
import logging
from pathlib import Path

# Configure audit logging
AUDIT_LOG_DIR = Path(__file__).parent.parent / "outputs" / "audit_logs"
AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)

audit_logger = logging.getLogger('data_processing_audit')
audit_logger.setLevel(logging.INFO)
audit_handler = logging.FileHandler(AUDIT_LOG_DIR / 'data_processing_audit.log')
audit_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
audit_logger.addHandler(audit_handler)

# Role definitions
ROLES = {
    'admin': ['read', 'write', 'delete', 'scale', 'encode', 'split', 'process'],
    'data_scientist': ['read', 'write', 'scale', 'encode', 'split', 'process'],
    'data_analyst': ['read', 'scale', 'encode', 'process'],
    'viewer': ['read']
}

# Session storage (in production, use Redis or database)
_active_sessions: Dict[str, Dict[str, Any]] = {}


class AuthorizationError(Exception):
    """Raised when authorization check fails."""
    pass


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


def create_session(user_id: str, role: str) -> str:
    """
    Create a new authenticated session.
    
    Args:
        user_id: Unique user identifier
        role: User role (admin, data_scientist, data_analyst, viewer)
        
    Returns:
        Session token
        
    Raises:
        ValueError: If role is invalid
    """
    if role not in ROLES:
        raise ValueError(f"Invalid role. Must be one of: {', '.join(ROLES.keys())}")
    
    session_token = f"session_{user_id}_{datetime.now().timestamp()}"
    _active_sessions[session_token] = {
        'user_id': user_id,
        'role': role,
        'created_at': datetime.now(),
        'permissions': ROLES[role]
    }
    
    audit_logger.info(f"Session created: user={user_id}, role={role}, token={session_token}")
    return session_token


def get_session(session_token: str) -> Optional[Dict[str, Any]]:
    """
    Get session information.
    
    Args:
        session_token: Session token
        
    Returns:
        Session data or None if not found
    """
    return _active_sessions.get(session_token)


def revoke_session(session_token: str) -> bool:
    """
    Revoke an active session.
    
    Args:
        session_token: Session token to revoke
        
    Returns:
        True if revoked, False if not found
    """
    if session_token in _active_sessions:
        user_id = _active_sessions[session_token]['user_id']
        del _active_sessions[session_token]
        audit_logger.info(f"Session revoked: user={user_id}, token={session_token}")
        return True
    return False


def require_permission(permission: str):
    """
    Decorator to require specific permission for function execution.
    
    Args:
        permission: Required permission (read, write, delete, scale, encode, split, process)
        
    Usage:
        @require_permission('write')
        def process_data(df, session_token=None):
            # Function code here
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract session_token from kwargs
            session_token = kwargs.get('session_token')
            
            if not session_token:
                error_msg = f"Authentication required for {func.__name__}"
                audit_logger.warning(f"{error_msg} - No session token provided")
                raise AuthenticationError(error_msg)
            
            # Validate session
            session = get_session(session_token)
            if not session:
                error_msg = f"Invalid or expired session for {func.__name__}"
                audit_logger.warning(f"{error_msg} - Token: {session_token}")
                raise AuthenticationError(error_msg)
            
            # Check permission
            user_permissions = session['permissions']
            if permission not in user_permissions:
                error_msg = f"Permission denied: '{permission}' required for {func.__name__}"
                audit_logger.warning(
                    f"{error_msg} - User: {session['user_id']}, Role: {session['role']}"
                )
                raise AuthorizationError(error_msg)
            
            # Log successful authorization
            audit_logger.info(
                f"Authorized: user={session['user_id']}, role={session['role']}, "
                f"function={func.__name__}, permission={permission}"
            )
            
            # Remove session_token from kwargs before calling function
            kwargs_cleaned = {k: v for k, v in kwargs.items() if k != 'session_token'}
            
            return func(*args, **kwargs_cleaned)
        
        return wrapper
    return decorator


def require_role(required_role: str):
    """
    Decorator to require specific role for function execution.
    
    Args:
        required_role: Required role (admin, data_scientist, data_analyst, viewer)
        
    Usage:
        @require_role('admin')
        def delete_data(df, session_token=None):
            # Function code here
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract session_token from kwargs
            session_token = kwargs.get('session_token')
            
            if not session_token:
                error_msg = f"Authentication required for {func.__name__}"
                audit_logger.warning(f"{error_msg} - No session token provided")
                raise AuthenticationError(error_msg)
            
            # Validate session
            session = get_session(session_token)
            if not session:
                error_msg = f"Invalid or expired session for {func.__name__}"
                audit_logger.warning(f"{error_msg} - Token: {session_token}")
                raise AuthenticationError(error_msg)
            
            # Check role
            user_role = session['role']
            if user_role != required_role:
                error_msg = f"Role '{required_role}' required for {func.__name__}, got '{user_role}'"
                audit_logger.warning(
                    f"{error_msg} - User: {session['user_id']}"
                )
                raise AuthorizationError(error_msg)
            
            # Log successful authorization
            audit_logger.info(
                f"Authorized: user={session['user_id']}, role={user_role}, "
                f"function={func.__name__}, required_role={required_role}"
            )
            
            # Remove session_token from kwargs before calling function
            kwargs_cleaned = {k: v for k, v in kwargs.items() if k != 'session_token'}
            
            return func(*args, **kwargs_cleaned)
        
        return wrapper
    return decorator

@require_permission('read')
def clean_column_names(df: pd.DataFrame, session_token: Optional[str] = None) -> pd.DataFrame:
    """
    Clean column names by removing spaces, special characters, and converting to lowercase.
    
    Args:
        df: Input DataFrame
        session_token: Authentication session token (required)
        
    Returns:
        DataFrame with cleaned column names
        
    Raises:
        AuthenticationError: If session_token is invalid or missing
        AuthorizationError: If user lacks 'read' permission
    """
    df_cleaned = df.copy()
    
    # Clean column names
    df_cleaned.columns = (df_cleaned.columns
                         .str.strip()
                         .str.lower()
                         .str.replace(r'[^\w\s]', '', regex=True)
                         .str.replace(r'\s+', '_', regex=True))
    
    return df_cleaned

@require_permission('process')
def handle_missing_values(df: pd.DataFrame, 
                         strategy: str = "drop",
                         columns: Optional[List[str]] = None,
                         fill_value: Any = None,
                         session_token: Optional[str] = None) -> pd.DataFrame:
    """
    Handle missing values in DataFrame.
    
    Args:
        df: Input DataFrame
        strategy: Strategy for handling missing values (drop, mean, median, mode, forward_fill, back_fill, custom)
        columns: Specific columns to process (if None, process all)
        fill_value: Custom fill value when strategy is 'custom'
        session_token: Authentication session token (required)
        
    Returns:
        DataFrame with missing values handled
        
    Raises:
        AuthenticationError: If session_token is invalid or missing
        AuthorizationError: If user lacks 'process' permission
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

@require_permission('encode')
def encode_categorical_variables(df: pd.DataFrame, 
                               columns: Optional[List[str]] = None,
                               method: str = "label",
                               session_token: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Encode categorical variables.
    
    Args:
        df: Input DataFrame
        columns: Columns to encode (if None, auto-detect categorical columns)
        method: Encoding method ('label', 'onehot')
        session_token: Authentication session token (required)
        
    Returns:
        Tuple of (encoded DataFrame, encoders dictionary)
        
    Raises:
        AuthenticationError: If session_token is invalid or missing
        AuthorizationError: If user lacks 'encode' permission
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

@require_permission('scale')
def scale_features(df: pd.DataFrame, 
                  columns: Optional[List[str]] = None,
                  method: str = "standard",
                  session_token: Optional[str] = None) -> Tuple[pd.DataFrame, Any]:
    """
    Scale numerical features.
    
    Args:
        df: Input DataFrame
        columns: Columns to scale (if None, auto-detect numerical columns)
        method: Scaling method ('standard', 'minmax')
        session_token: Authentication session token (required)
        
    Returns:
        Tuple of (scaled DataFrame, scaler object)
        
    Raises:
        AuthenticationError: If session_token is invalid or missing
        AuthorizationError: If user lacks 'scale' permission
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

@require_permission('read')
def detect_outliers(df: pd.DataFrame, 
                   columns: Optional[List[str]] = None,
                   method: str = "iqr",
                   session_token: Optional[str] = None) -> pd.DataFrame:
    """
    Detect outliers in numerical columns.
    
    Args:
        df: Input DataFrame
        columns: Columns to check (if None, check all numerical columns)
        method: Method for outlier detection ('iqr', 'zscore')
        session_token: Authentication session token (required)
        
    Returns:
        DataFrame with outlier indicators
        
    Raises:
        AuthenticationError: If session_token is invalid or missing
        AuthorizationError: If user lacks 'read' permission
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

@require_permission('split')
def split_data(df: pd.DataFrame, 
               target_column: str,
               test_size: float = 0.2,
               validation_size: float = 0.1,
               random_state: int = 42,
               session_token: Optional[str] = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    """
    Split data into train, validation, and test sets.
    
    Args:
        df: Input DataFrame
        target_column: Name of target column
        test_size: Proportion of test set
        validation_size: Proportion of validation set
        random_state: Random state for reproducibility
        session_token: Authentication session token (required)
        
    Returns:
        Tuple of (X_train, X_val, X_test, y_train, y_val, y_test)
        
    Raises:
        AuthenticationError: If session_token is invalid or missing
        AuthorizationError: If user lacks 'split' permission
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

@require_permission('read')
def create_feature_summary(df: pd.DataFrame, session_token: Optional[str] = None) -> pd.DataFrame:
    """
    Create a summary of features in the DataFrame.
    
    Args:
        df: Input DataFrame
        session_token: Authentication session token (required)
        
    Returns:
        Summary DataFrame with feature statistics
        
    Raises:
        AuthenticationError: If session_token is invalid or missing
        AuthorizationError: If user lacks 'read' permission
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