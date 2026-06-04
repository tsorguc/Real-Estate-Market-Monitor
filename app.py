import os
import sys
import dash
import dash_bootstrap_components as dbc

# Ensure the root/src directories are in path for module resolution
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.dashboard.data_access import load_data
from src.dashboard.layout import get_layout
from src.dashboard.callbacks import register_callbacks

# Initialize Dash application with Cyborg dark bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="Real Estate Market Monitor Dashboard"
)

# Expose flask server for WSGI/Gunicorn production environments
server = app.server

# Load data once to initialize layout options
df = load_data()

# Apply the page layout
app.layout = get_layout(df)

# Register all callbacks
register_callbacks(app)

if __name__ == "__main__":
    # Run server locally on default port 8050
    # Enable debug=True for local development auto-reloading
    print("Starting Real Estate Market Monitor Dashboard at http://localhost:8050 ...")
    app.run(debug=True, host="0.0.0.0", port=8050)
