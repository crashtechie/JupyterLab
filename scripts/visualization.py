"""
Visualization utilities for data science workflows.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Optional, Tuple, Any
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set default style
plt.style.use('default')
sns.set_palette("husl")

def setup_matplotlib_style(style: str = "seaborn-v0_8", figsize: Tuple[int, int] = (12, 8)) -> None:
    """
    Set up matplotlib and seaborn style.
    
    Args:
        style: Matplotlib style to use
        figsize: Default figure size
    """
    plt.style.use(style)
    plt.rcParams['figure.figsize'] = figsize
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10

def plot_distribution(df: pd.DataFrame, 
                     columns: Optional[List[str]] = None,
                     bins: int = 30,
                     figsize: Tuple[int, int] = (15, 10)) -> None:
    """
    Plot distribution of numerical columns.
    
    Args:
        df: Input DataFrame
        columns: Columns to plot (if None, plot all numerical columns)
        bins: Number of bins for histograms
        figsize: Figure size
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    n_cols = min(3, len(columns))
    n_rows = (len(columns) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows == 1:
        axes = [axes] if n_cols == 1 else axes
    else:
        axes = axes.flatten()
    
    for i, col in enumerate(columns):
        ax = axes[i] if len(columns) > 1 else axes
        
        # Histogram
        ax.hist(df[col].dropna(), bins=bins, alpha=0.7, edgecolor='black')
        ax.set_title(f'Distribution of {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        
        # Add statistics
        mean_val = df[col].mean()
        median_val = df[col].median()
        ax.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='orange', linestyle='--', label=f'Median: {median_val:.2f}')
        ax.legend()
    
    # Hide unused subplots
    for i in range(len(columns), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()

def plot_correlation_matrix(df: pd.DataFrame, 
                           columns: Optional[List[str]] = None,
                           method: str = "pearson",
                           figsize: Tuple[int, int] = (12, 10)) -> None:
    """
    Plot correlation matrix heatmap.
    
    Args:
        df: Input DataFrame
        columns: Columns to include (if None, use all numerical columns)
        method: Correlation method ('pearson', 'spearman', 'kendall')
        figsize: Figure size
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    correlation_matrix = df[columns].corr(method=method)
    
    plt.figure(figsize=figsize)
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    
    sns.heatmap(correlation_matrix, 
                mask=mask,
                annot=True, 
                cmap='coolwarm', 
                center=0,
                square=True,
                fmt='.2f',
                cbar_kws={"shrink": .8})
    
    plt.title(f'{method.capitalize()} Correlation Matrix')
    plt.tight_layout()
    plt.show()

def plot_categorical_distribution(df: pd.DataFrame, 
                                 columns: Optional[List[str]] = None,
                                 max_categories: int = 20,
                                 figsize: Tuple[int, int] = (15, 10)) -> None:
    """
    Plot distribution of categorical columns.
    
    Args:
        df: Input DataFrame
        columns: Columns to plot (if None, plot all categorical columns)
        max_categories: Maximum number of categories to display
        figsize: Figure size
    """
    if columns is None:
        columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    n_cols = min(2, len(columns))
    n_rows = (len(columns) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows == 1:
        axes = [axes] if n_cols == 1 else axes
    else:
        axes = axes.flatten()
    
    for i, col in enumerate(columns):
        ax = axes[i] if len(columns) > 1 else axes
        
        # Get value counts and limit to max_categories
        value_counts = df[col].value_counts().head(max_categories)
        
        # Bar plot
        value_counts.plot(kind='bar', ax=ax, rot=45)
        ax.set_title(f'Distribution of {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Count')
        
        # Add value labels on bars
        for j, v in enumerate(value_counts.values):
            ax.text(j, v + 0.01 * ax.get_ylim()[1], str(v), ha='center', va='bottom')
    
    # Hide unused subplots
    for i in range(len(columns), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()

def plot_boxplot(df: pd.DataFrame, 
                columns: Optional[List[str]] = None,
                figsize: Tuple[int, int] = (15, 8)) -> None:
    """
    Plot boxplots for numerical columns.
    
    Args:
        df: Input DataFrame
        columns: Columns to plot (if None, plot all numerical columns)
        figsize: Figure size
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    plt.figure(figsize=figsize)
    df[columns].boxplot()
    plt.title('Boxplots of Numerical Features')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_scatter_matrix(df: pd.DataFrame, 
                       columns: Optional[List[str]] = None,
                       hue: Optional[str] = None,
                       figsize: Tuple[int, int] = (12, 12)) -> None:
    """
    Plot scatter matrix for numerical columns.
    
    Args:
        df: Input DataFrame
        columns: Columns to plot (if None, use all numerical columns)
        hue: Column for color coding
        figsize: Figure size
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Limit to maximum 5 columns for readability
    columns = columns[:5]
    
    sns.pairplot(df[columns + ([hue] if hue else [])], 
                hue=hue, 
                height=figsize[0]//len(columns))
    plt.suptitle('Scatter Matrix', y=1.02)
    plt.show()

def plot_time_series(df: pd.DataFrame, 
                    date_column: str,
                    value_columns: List[str],
                    title: str = "Time Series Plot",
                    figsize: Tuple[int, int] = (15, 8)) -> None:
    """
    Plot time series data.
    
    Args:
        df: Input DataFrame
        date_column: Name of date column
        value_columns: List of value columns to plot
        title: Plot title
        figsize: Figure size
    """
    plt.figure(figsize=figsize)
    
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])
    
    for col in value_columns:
        plt.plot(df[date_column], df[col], label=col, linewidth=2)
    
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def create_interactive_plot(df: pd.DataFrame, 
                          x: str, 
                          y: str,
                          color: Optional[str] = None,
                          plot_type: str = "scatter",
                          title: Optional[str] = None) -> go.Figure:
    """
    Create interactive plotly plot.
    
    Args:
        df: Input DataFrame
        x: X-axis column
        y: Y-axis column
        color: Column for color coding
        plot_type: Type of plot ('scatter', 'line', 'bar')
        title: Plot title
        
    Returns:
        Plotly figure object
    """
    if plot_type == "scatter":
        fig = px.scatter(df, x=x, y=y, color=color, title=title, 
                        hover_data=df.columns)
    elif plot_type == "line":
        fig = px.line(df, x=x, y=y, color=color, title=title)
    elif plot_type == "bar":
        fig = px.bar(df, x=x, y=y, color=color, title=title)
    else:
        raise ValueError("plot_type must be 'scatter', 'line', or 'bar'")
    
    fig.update_layout(
        height=600,
        showlegend=True,
        template="plotly_white"
    )
    
    return fig

def save_plot(filename: str, dpi: int = 300, bbox_inches: str = 'tight') -> None:
    """
    Save current matplotlib plot.
    
    Args:
        filename: Output filename
        dpi: Resolution in DPI
        bbox_inches: Bounding box inches
    """
    from scripts.utils import get_output_path
    
    filepath = get_output_path(filename, "figures")
    plt.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
    print(f"Plot saved to: {filepath}")