import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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