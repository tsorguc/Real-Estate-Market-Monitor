from dash import Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from src.dashboard.data_access import load_data, filter_data
from src.dashboard.layout import create_kpi_card

# Load initial dataset
df_all = load_data()

# Global transaction history for live ticker
live_ticker_history = {
    'timestamps': [datetime.now() - timedelta(seconds=(20-i)*3) for i in range(20)],
    'prices': [random.randint(250000, 1500000) for _ in range(20)]
}

def get_empty_chart(message):
    """Generates an empty graph figure showing a placeholder message."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color="#a2a2a2")
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    return fig

def register_callbacks(app):
    """Registers all dashboard callbacks with the Dash application."""
    
    # 1. Update KPI cards based on filter selections
    @app.callback(
        [Output("kpi-total-listings", "children"),
         Output("kpi-avg-price", "children"),
         Output("kpi-avg-area", "children"),
         Output("kpi-avg-price-sqft", "children")],
        [Input("filter-property-type", "value"),
         Input("filter-year-range", "value"),
         Input("filter-search", "value")]
    )
    def update_kpi_cards(selected_types, year_range, search_text):
        filtered_df = filter_data(df_all, selected_types, year_range, search_text)
        total_listings = len(filtered_df)
        
        if total_listings > 0:
            avg_price = filtered_df['price'].mean()
            avg_area = filtered_df['area'].mean()
            # Calculate price per sqft element-wise then mean
            if 'price' in filtered_df.columns and 'area' in filtered_df.columns:
                valid_sqft = filtered_df[(filtered_df['area'] > 0) & (filtered_df['price'] > 0)]
                if not valid_sqft.empty:
                    avg_price_sqft = (valid_sqft['price'] / valid_sqft['area']).mean()
                else:
                    avg_price_sqft = 0
            else:
                avg_price_sqft = 0
        else:
            avg_price = 0
            avg_area = 0
            avg_price_sqft = 0
            
        return (
            create_kpi_card("Total Listings", f"{total_listings:,}", "info"),
            create_kpi_card("Average Price", f"${avg_price:,.0f}" if avg_price > 0 else "$0", "primary"),
            create_kpi_card("Average Area", f"{avg_area:,.0f} sqft" if avg_area > 0 else "0 sqft", "success"),
            create_kpi_card("Avg Price / Sqft", f"${avg_price_sqft:,.2f}/sqft" if avg_price_sqft > 0 else "$0/sqft", "warning")
        )

    # 2. Update Top Listings by Price Bar Chart (Horizontal Bar Chart)
    @app.callback(
        Output("chart-price-bar", "figure"),
        [Input("filter-property-type", "value"),
         Input("filter-year-range", "value"),
         Input("filter-search", "value")]
    )
    def update_price_bar_chart(selected_types, year_range, search_text):
        filtered_df = filter_data(df_all, selected_types, year_range, search_text)
        
        if filtered_df.empty:
            return get_empty_chart("No matching property listings found.")
            
        top_10 = filtered_df.nlargest(10, 'price').copy()
        top_10['label'] = top_10['title'].fillna('Property ' + top_10['listing_id'].astype(str))
        top_10 = top_10.sort_values(by='price', ascending=True)
        
        fig = px.bar(
            top_10,
            x='price',
            y='label',
            orientation='h',
            color='type',
            hover_data=['area', 'listing_id'],
            color_discrete_map={
                'Multi-Family': '#00f2fe',
                'Retail': '#ff007f',
                'Office': '#39ff14',
                'Industrial': '#ffaa00'
            },
            template='plotly_dark'
        )
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=150, r=20, t=10, b=40),
            xaxis=dict(title="Price (USD)", gridcolor="rgba(255,255,255,0.05)", tickformat="$,.0f"),
            yaxis=dict(title=""),
            legend=dict(title="Type", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        return fig

    # 3. Update Market Composition Pie Chart
    @app.callback(
        Output("chart-type-pie", "figure"),
        [Input("filter-property-type", "value"),
         Input("filter-year-range", "value"),
         Input("filter-search", "value")]
    )
    def update_type_pie_chart(selected_types, year_range, search_text):
        filtered_df = filter_data(df_all, selected_types, year_range, search_text)
        
        if filtered_df.empty:
            return get_empty_chart("No matching property listings found.")
            
        counts = filtered_df['type'].value_counts().reset_index()
        counts.columns = ['type', 'count']
        
        fig = px.pie(
            counts,
            names='type',
            values='count',
            hole=0.4,
            color='type',
            color_discrete_map={
                'Multi-Family': '#00f2fe',
                'Retail': '#ff007f',
                'Office': '#39ff14',
                'Industrial': '#ffaa00'
            },
            template='plotly_dark'
        )
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=10, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        fig.update_traces(textinfo='percent+label', pull=[0.05]*len(counts))
        return fig

    # 4. Update Price Distribution Violin Plot
    @app.callback(
        Output("chart-price-violin", "figure"),
        [Input("filter-property-type", "value"),
         Input("filter-year-range", "value"),
         Input("filter-search", "value")]
    )
    def update_price_violin_plot(selected_types, year_range, search_text):
        filtered_df = filter_data(df_all, selected_types, year_range, search_text)
        
        if filtered_df.empty:
            return get_empty_chart("No matching property listings found.")
            
        fig = px.violin(
            filtered_df,
            x='type',
            y='price',
            color='type',
            box=True,
            points='all',
            hover_data=['listing_id', 'area'],
            color_discrete_map={
                'Multi-Family': '#00f2fe',
                'Retail': '#ff007f',
                'Office': '#39ff14',
                'Industrial': '#ffaa00'
            },
            template='plotly_dark'
        )
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=20, t=10, b=40),
            xaxis=dict(title="Property Type"),
            yaxis=dict(title="Price (USD)", gridcolor="rgba(255,255,255,0.05)", tickformat="$,.0f"),
            showlegend=False
        )
        return fig

    # 5. Update Property Area Distribution Histogram
    @app.callback(
        Output("chart-area-hist", "figure"),
        [Input("filter-property-type", "value"),
         Input("filter-year-range", "value"),
         Input("filter-search", "value")]
    )
    def update_area_histogram(selected_types, year_range, search_text):
        filtered_df = filter_data(df_all, selected_types, year_range, search_text)
        
        if filtered_df.empty:
            return get_empty_chart("No matching property listings found.")
            
        fig = px.histogram(
            filtered_df,
            x='area',
            color='type',
            marginal='box',
            hover_data=['listing_id', 'price'],
            color_discrete_map={
                'Multi-Family': '#00f2fe',
                'Retail': '#ff007f',
                'Office': '#39ff14',
                'Industrial': '#ffaa00'
            },
            template='plotly_dark'
        )
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=20, t=10, b=40),
            xaxis=dict(title="Area (sqft)", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title="Count", gridcolor="rgba(255,255,255,0.05)"),
            legend=dict(title="Type", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        return fig

    # 6. Live Streaming Ticker Update
    @app.callback(
        Output("chart-live-ticker", "figure"),
        [Input("live-ticker-interval", "n_intervals")]
    )
    def update_live_stream(n):
        new_time = datetime.now()
        last_price = live_ticker_history['prices'][-1]
        
        # Simulating a random walk for transaction prices
        change = random.randint(-40000, 45000)
        new_price = max(100000, last_price + change)
        
        live_ticker_history['timestamps'].append(new_time)
        live_ticker_history['prices'].append(new_price)
        
        # Keep sliding window of last 20 readings
        if len(live_ticker_history['timestamps']) > 20:
            live_ticker_history['timestamps'].pop(0)
            live_ticker_history['prices'].pop(0)
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=live_ticker_history['timestamps'],
            y=live_ticker_history['prices'],
            mode='lines+markers',
            line=dict(color='#ff007f', width=2),
            marker=dict(size=8, color='#ff007f'),
            name="Live Transaction Price"
        ))
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=20, t=10, b=40),
            xaxis=dict(
                gridcolor="rgba(255,255,255,0.05)",
                tickformat="%H:%M:%S"
            ),
            yaxis=dict(
                title="Transaction Price (USD)",
                gridcolor="rgba(255,255,255,0.05)",
                tickformat="$,.0f"
            ),
            height=300
        )
        return fig
