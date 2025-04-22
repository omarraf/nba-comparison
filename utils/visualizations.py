import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import numpy as np
import plotly.graph_objects as go

def add_court_shapes(fig):
    # Steph Curry's 3pt shots at (2, 254) => center 3pt arc at y=254
    court_shapes = [
        # Hoop (centered at (0, 0), diameter 15)
        dict(type="circle", xref="x", yref="y", x0=-7.5, y0=-7.5, x1=7.5, y1=7.5, line=dict(color="white", width=2)),
        # Backboard (from -30 to 30 at y=-7.5)
        dict(type="rect", xref="x", yref="y", x0=-30, y0=-10, x1=30, y1=-7.5, line=dict(color="white", width=2)),
        # Paint (the key)
        dict(type="rect", xref="x", yref="y", x0=-80, y0=-47.5, x1=80, y1=143.5, line=dict(color="white", width=2)),
        # Free throw circle (centered at y=143.5, radius 60)
        dict(type="circle", xref="x", yref="y", x0=-60, y0=83.5, x1=60, y1=203.5, line=dict(color="white", width=2)),
        # 3pt arc (top at y=254, from x=-220 to x=220)
        dict(type="path", path="M -220,0 Q 0,500 220,0", line=dict(color="white", width=2)),
        # Sidelines (full half court)
        dict(type="rect", xref="x", yref="y", x0=-250, y0=-47.5, x1=250, y1=422.5, line=dict(color="white", width=2)),
    ]
    fig.update_layout(shapes=court_shapes)
    return fig

def plot_made_shots_scatter(df, player_name, season):
    made_df = df[df['SHOT_MADE_FLAG'] == 1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=made_df['LOC_X'],
        y=made_df['LOC_Y'],
        mode='markers',
        marker=dict(color='red', size=7, opacity=0.7),
        name='Made Shot'
    ))
    fig = add_court_shapes(fig)
    fig.update_layout(
        title=f"{player_name} Made Shots ({season})",
        xaxis=dict(showgrid=False, zeroline=False, range=[-250, 250], color='white'),
        yaxis=dict(showgrid=False, zeroline=False, range=[-47.5, 422.5], scaleanchor="x", scaleratio=1, color='white'),
        plot_bgcolor='black',
        paper_bgcolor='black',
        height=600,
        width=600,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def create_stat_comparison(df, player1_name, player2_name):
    """Create a bar chart comparing basic stats between two players."""
    # Melt the dataframe for easier plotting
    melted_df = pd.melt(df, id_vars=['Stat'], var_name='Player', value_name='Value')
    
    # Create the bar chart
    fig = px.bar(
        melted_df, 
        x='Stat', 
        y='Value', 
        color='Player',
        barmode='group',
        title='Basic Statistics Comparison',
        color_discrete_map={
            player1_name: '#1D428A',
            player2_name: '#C8102E'
        }
    )
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title='Value',
        legend_title='Player',
        font=dict(size=14),
        height=500
    )
    
    return fig
def create_radar_chart(df, player1_name, player2_name):
    """Create a radar chart comparing advanced metrics between two players."""
    categories = df['Metric'].tolist()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=df[player1_name].tolist(),
        theta=categories,
        fill='toself',
        name=player1_name,
        line_color='#1D428A'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=df[player2_name].tolist(),
        theta=categories,
        fill='toself',
        name=player2_name,
        line_color='#C8102E'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
            ),
        ),
        showlegend=True,
        title='Advanced Metrics Comparison',
        height=500
    )
    
    return fig