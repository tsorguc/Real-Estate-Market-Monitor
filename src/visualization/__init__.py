"""
Visualization package for the Real Estate Market Monitor.
Re-exports all chart functions from static_charts and interactive_charts.
"""

from .static_charts import (
    plot_top_properties_by_price,
    plot_avg_price_over_time,
    plot_price_distribution,
    plot_area_vs_price,
    plot_property_type_counts,
    plot_price_by_type_boxplot,
    plot_correlation_heatmap,
    plot_dashboard_subplots
)

from .interactive_charts import (
    plot_interactive_price_scatter,
    plot_interactive_type_distribution,
    plot_interactive_price_by_type,
    plot_interactive_area_hist,
    plot_interactive_multi_layout
)

__all__ = [
    'plot_top_properties_by_price',
    'plot_avg_price_over_time',
    'plot_price_distribution',
    'plot_area_vs_price',
    'plot_property_type_counts',
    'plot_price_by_type_boxplot',
    'plot_correlation_heatmap',
    'plot_dashboard_subplots',
    'plot_interactive_price_scatter',
    'plot_interactive_type_distribution',
    'plot_interactive_price_by_type',
    'plot_interactive_area_hist',
    'plot_interactive_multi_layout'
]
