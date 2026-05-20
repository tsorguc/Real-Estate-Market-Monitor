import os
import sys
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Detect interactive Jupyter/IPython environment safely
_in_notebook = False
try:
    from IPython import get_ipython
    if get_ipython() is not None:
        _in_notebook = True
except Exception:
    pass

if not _in_notebook and 'ipykernel' in sys.modules:
    _in_notebook = True

def _save_html(fig, output_dir, filename):
    """Internal helper to save figures as HTML."""
    os.makedirs(output_dir, exist_ok=True)
    html_path = os.path.join(output_dir, f"{filename}.html")
    fig.write_html(html_path)

def plot_interactive_price_scatter(df, output_dir):
    """Interactive scatter plot: Area vs. Price with tooltips."""
    fig = px.scatter(
        df, x='area', y='price', color='type',
        hover_data=['listing_id', 'source', 'title'],
        title='Interactive Price vs. Area Explorer',
        labels={'area': 'Area (sqft)', 'price': 'Price (USD)'},
        template='plotly_white'
    )
    _save_html(fig, output_dir, "interactive_price_scatter")
    if _in_notebook:
        fig.show()

def plot_interactive_type_distribution(df, output_dir):
    """Interactive pie chart for property types."""
    fig = px.pie(
        df, names='type', 
        title='Market Composition by Property Type',
        template='plotly_white',
        hole=0.3
    )
    fig.update_traces(textinfo='percent+label')
    _save_html(fig, output_dir, "interactive_type_pie")
    if _in_notebook:
        fig.show()

def plot_interactive_price_by_type(df, output_dir):
    """Interactive violin plot for price distributions."""
    fig = px.violin(
        df, x='type', y='price', color='type',
        box=True, points='all',
        hover_data=['listing_id', 'area'],
        title='Price Distribution by Property Type (Interactive)',
        labels={'price': 'Price (USD)', 'type': 'Property Type'},
        template='plotly_white'
    )
    _save_html(fig, output_dir, "interactive_price_violin")
    if _in_notebook:
        fig.show()

def plot_interactive_area_hist(df, output_dir):
    """Interactive histogram for property area."""
    fig = px.histogram(
        df, x='area', color='type',
        marginal='box',
        hover_data=['listing_id', 'price'],
        title='Property Area Distribution',
        labels={'area': 'Area (sqft)'},
        template='plotly_white'
    )
    _save_html(fig, output_dir, "interactive_area_histogram")
    if _in_notebook:
        fig.show()

def plot_interactive_multi_layout(df, output_dir):
    """Interactive 2x2 dashboard using Graph Objects."""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Price vs Area", "Type Distribution", 
            "Price Boxplot", "Area Distribution"
        ),
        specs=[[{"type": "xy"}, {"type": "domain"}],
               [{"type": "xy"}, {"type": "xy"}]]
    )
    
    # Trace 1: Scatter (Price vs Area)
    for t in df['type'].unique():
        sub_df = df[df['type'] == t]
        fig.add_trace(
            go.Scatter(
                x=sub_df['area'], y=sub_df['price'], mode='markers',
                name=t, text=sub_df['listing_id'],
                hovertemplate="Area: %{x}<br>Price: %{y}<br>ID: %{text}"
            ),
            row=1, col=1
        )
    
    # Trace 2: Pie (Type Dist)
    counts = df['type'].value_counts()
    fig.add_trace(
        go.Pie(labels=counts.index, values=counts.values, name="Types"),
        row=1, col=2
    )
    
    # Trace 3: Box (Price by Type)
    for t in df['type'].unique():
        sub_df = df[df['type'] == t]
        fig.add_trace(
            go.Box(y=sub_df['price'], name=t, boxpoints='all'),
            row=2, col=1
        )
        
    # Trace 4: Histogram (Area)
    fig.add_trace(
        go.Histogram(x=df['area'], name="Area Distribution", marker_color='green'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800, width=1000, 
        title_text="Interactive Real Estate Market Dashboard",
        template='plotly_white',
        showlegend=True
    )
    
    _save_html(fig, output_dir, "interactive_multi_layout")
    if _in_notebook:
        fig.show()
