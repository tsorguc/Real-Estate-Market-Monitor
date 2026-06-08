"""
Dashboard package for the Real Estate Market Monitor.
Includes layout, callbacks, and database access utilities.
"""

from src.dashboard.data_access import load_data
from src.dashboard.layout import get_layout
from src.dashboard.callbacks import register_callbacks
