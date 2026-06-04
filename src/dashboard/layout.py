from dash import dcc, html
import dash_bootstrap_components as dbc
from src.dashboard.data_access import get_available_genres, get_year_range

def create_kpi_card(title, value, color_class):
    """Helper function to build a styled glassmorphic KPI card."""
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.H6(title, className="text-muted text-uppercase font-weight-bold mb-2", style={"fontSize": "0.75rem", "letterSpacing": "1px"}),
                html.H3(value, className=f"text-{color_class} font-weight-bold mb-0", style={"fontSize": "1.8rem", "fontFamily": "Outfit, sans-serif"})
            ])
        ]),
        style={
            "background": "rgba(25, 25, 35, 0.65)",
            "border": "1px solid rgba(255, 255, 255, 0.1)",
            "borderRadius": "12px",
            "boxShadow": "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
            "backdropFilter": "blur(8px)",
            "WebkitBackdropFilter": "blur(8px)"
        },
        className="mb-4"
    )

def get_layout(df):
    """Defines the full Dash page layout."""
    property_types = get_available_genres(df)
    min_yr, max_yr = get_year_range(df)
    
    # In case there's only one year or min_yr == max_yr, adjust so slider works
    if min_yr == max_yr:
        slider_min = min_yr - 5
        slider_max = max_yr
        slider_marks = {y: str(y) for y in range(slider_min, slider_max + 1)}
    else:
        slider_min = min_yr
        slider_max = max_yr
        slider_marks = {y: str(y) for y in range(min_yr, max_yr + 1)}
        
    layout = dbc.Container([
        # Header with Gradient Background
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("REAL ESTATE MARKET MONITOR", 
                            style={
                                "color": "#00f2fe", 
                                "fontFamily": "Outfit, sans-serif", 
                                "fontWeight": "800",
                                "letterSpacing": "2px",
                                "textAlign": "center",
                                "marginTop": "20px",
                                "textShadow": "0 0 10px rgba(0, 242, 254, 0.5)"
                            }),
                    html.P("Interactive Analytics & Live Streaming Pipeline Dashboard", 
                           style={
                               "color": "#a2a2a2", 
                               "textAlign": "center",
                               "fontSize": "1.1rem",
                               "marginBottom": "30px"
                           })
                ])
            ], width=12)
        ]),
        
        # KPI Row
        dbc.Row([
            dbc.Col(id="kpi-total-listings", width=3),
            dbc.Col(id="kpi-avg-price", width=3),
            dbc.Col(id="kpi-avg-area", width=3),
            dbc.Col(id="kpi-avg-price-sqft", width=3),
        ], className="mb-2"),
        
        # Filters Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Search & Filter Controls", style={"borderBottom": "1px solid rgba(255,255,255,0.1)", "color": "#00f2fe", "fontWeight": "bold"}),
                    dbc.CardBody([
                        dbc.Row([
                            # Property Type Dropdown
                            dbc.Col([
                                html.Label("Property Type:", className="text-muted mb-2"),
                                dcc.Dropdown(
                                    id="filter-property-type",
                                    options=[{"label": t, "value": t} for t in property_types],
                                    value=property_types, # Select all by default
                                    multi=True,
                                    placeholder="Select property types...",
                                    style={"color": "#000"}
                                )
                            ], md=4, xs=12),
                            
                            # Year Range Slider
                            dbc.Col([
                                html.Label("Collection Year Range:", className="text-muted mb-2"),
                                dcc.RangeSlider(
                                    id="filter-year-range",
                                    min=slider_min,
                                    max=slider_max,
                                    step=1,
                                    value=[min_yr, max_yr],
                                    marks=slider_marks,
                                    tooltip={"always_visible": False, "placement": "bottom"}
                                )
                            ], md=4, xs=12),
                            
                            # Text Search Input
                            dbc.Col([
                                html.Label("Search Listings (Title/Desc):", className="text-muted mb-2"),
                                dbc.Input(
                                    id="filter-search",
                                    type="text",
                                    placeholder="Enter keyword (e.g. Office, Retail, etc.)...",
                                    className="bg-dark text-white border-secondary"
                                )
                            ], md=4, xs=12)
                        ])
                    ])
                ], style={
                    "background": "rgba(25, 25, 35, 0.8)",
                    "border": "1px solid rgba(255,255,255,0.1)",
                    "borderRadius": "12px"
                }, className="mb-4")
            ], width=12)
        ]),
        
        # Main Charts Grid
        dbc.Row([
            # 1. Price Bar Chart
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Top Listings by Price", style={"color": "#00f2fe"}),
                    dbc.CardBody([
                        dcc.Graph(id="chart-price-bar")
                    ])
                ], style={"background": "rgba(25, 25, 35, 0.8)", "border": "1px solid rgba(255,255,255,0.1)", "borderRadius": "12px"}, className="mb-4")
            ], md=6, xs=12),
            
            # 2. Composition Pie Chart
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Market Composition by Property Type", style={"color": "#00f2fe"}),
                    dbc.CardBody([
                        dcc.Graph(id="chart-type-pie")
                    ])
                ], style={"background": "rgba(25, 25, 35, 0.8)", "border": "1px solid rgba(255,255,255,0.1)", "borderRadius": "12px"}, className="mb-4")
            ], md=6, xs=12)
        ]),
        
        dbc.Row([
            # 3. Price Distribution Violin
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Price Distribution by Property Type", style={"color": "#00f2fe"}),
                    dbc.CardBody([
                        dcc.Graph(id="chart-price-violin")
                    ])
                ], style={"background": "rgba(25, 25, 35, 0.8)", "border": "1px solid rgba(255,255,255,0.1)", "borderRadius": "12px"}, className="mb-4")
            ], md=6, xs=12),
            
            # 4. Area Distribution Histogram
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Property Area (sqft) Distribution", style={"color": "#00f2fe"}),
                    dbc.CardBody([
                        dcc.Graph(id="chart-area-hist")
                    ])
                ], style={"background": "rgba(25, 25, 35, 0.8)", "border": "1px solid rgba(255,255,255,0.1)", "borderRadius": "12px"}, className="mb-4")
            ], md=6, xs=12)
        ]),
        
        # 5. Live Streaming Ticker Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("🔴 Live Real-Time Property Price Stream", style={"color": "#ff007f", "fontWeight": "bold"}),
                        html.Span(" (Updates every 3 seconds)", className="text-muted", style={"fontSize": "0.85rem"})
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="chart-live-ticker"),
                        dcc.Interval(
                            id="live-ticker-interval",
                            interval=3000,  # in milliseconds
                            n_intervals=0
                        )
                    ])
                ], style={"background": "rgba(25, 25, 35, 0.8)", "border": "1px solid rgba(255,255,255,0.1)", "borderRadius": "12px"}, className="mb-4")
            ], width=12)
        ]),
        
        # Footer
        dbc.Row([
            dbc.Col([
                html.Hr(style={"borderColor": "rgba(255,255,255,0.1)"}),
                html.P("© 2026 Real Estate Market Monitor. Built with Dash & Plotly.", 
                       className="text-muted text-center mb-4", style={"fontSize": "0.9rem"})
            ], width=12)
        ])
    ], fluid=True, style={"background": "#0b0c10", "minHeight": "100vh"})
    
    return layout
