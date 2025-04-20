import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_fetcher import get_all_players, get_player_stats, get_player_image
from utils.visualizations import create_stat_comparison


# Page configuration
st.set_page_config(
    page_title="NBA Player Comparison Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1D428A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #C8102E;
        margin-top: 1rem;
    }
    .stat-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<div class="main-header">NBA Player Comparison Dashboard</div>', unsafe_allow_html=True)
st.markdown("Compare statistics between NBA players across different seasons.")

# Initialize session state for caching
if 'players_list' not in st.session_state:
    st.session_state.players_list = get_all_players()

# Sidebar for player selection
st.sidebar.markdown("## Player Selection")

# Player 1 selection
player1_name = st.sidebar.selectbox(
    "Select Player 1:",
    options=st.session_state.players_list['full_name'].tolist(),
    key="player1"
)
player1_id = st.session_state.players_list[st.session_state.players_list['full_name'] == player1_name]['id'].iloc[0]

# Player 2 selection
player2_name = st.sidebar.selectbox(
    "Select Player 2:",
    options=st.session_state.players_list['full_name'].tolist(),
    key="player2"
)
player2_id = st.session_state.players_list[st.session_state.players_list['full_name'] == player2_name]['id'].iloc[0]

# Get player career stats
player1_stats = get_player_stats(player1_id)
player2_stats = get_player_stats(player2_id)

# Get available seasons for both players
player1_seasons = sorted(player1_stats['SEASON_ID'].unique(), reverse=True)
player2_seasons = sorted(player2_stats['SEASON_ID'].unique(), reverse=True)

# Season selection
st.sidebar.markdown("## Season Selection")
season1 = st.sidebar.selectbox("Select Season for Player 1:", options=player1_seasons, key="season1")
season2 = st.sidebar.selectbox("Select Season for Player 2:", options=player2_seasons, key="season2")

# Filter stats for selected seasons
player1_season_stats = player1_stats[player1_stats['SEASON_ID'] == season1].iloc[0]
player2_season_stats = player2_stats[player2_stats['SEASON_ID'] == season2].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"<div class='sub-header'>{player1_name} ({season1})</div>", unsafe_allow_html=True)
    player1_img = get_player_image(player1_id)
    st.image(player1_img, width=200)

with col2:
    st.markdown(f"<div class='sub-header'>{player2_name} ({season2})</div>", unsafe_allow_html=True)
    player2_img = get_player_image(player2_id)
    st.image(player2_img, width=200)

# Basic stats comparison
st.markdown("## Basic Statistics Comparison")

# Create comparison dataframe
comparison_df = pd.DataFrame({
    'Stat': ['PPG', 'RPG', 'APG', 'SPG', 'BPG', 'FG%', '3P%', 'FT%'],
    player1_name: [
        player1_season_stats['PTS'], 
        player1_season_stats['REB'], 
        player1_season_stats['AST'], 
        player1_season_stats['STL'], 
        player1_season_stats['BLK'], 
        player1_season_stats['FG_PCT'] * 100, 
        player1_season_stats['FG3_PCT'] * 100, 
        player1_season_stats['FT_PCT'] * 100
    ],
    player2_name: [
        player2_season_stats['PTS'], 
        player2_season_stats['REB'], 
        player2_season_stats['AST'], 
        player2_season_stats['STL'], 
        player2_season_stats['BLK'], 
        player2_season_stats['FG_PCT'] * 100, 
        player2_season_stats['FG3_PCT'] * 100, 
        player2_season_stats['FT_PCT'] * 100
    ]
})

# Display basic stats bar chart
st.plotly_chart(create_stat_comparison(comparison_df, player1_name, player2_name), use_container_width=True)
