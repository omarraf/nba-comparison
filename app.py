import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_fetcher import get_all_players, get_player_stats, get_player_image, get_shotchart_df
from utils.visualizations import create_stat_comparison, create_radar_chart, plot_made_shots_scatter
from utils.bedrock_client import BedrockClient

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
    .ai-insights-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        color: white;
        margin-top: 1rem;
    }
    .ai-insights-card h3 {
        color: white;
        margin-bottom: 1rem;
    }
    .ai-insights-card p {
        color: white;
        line-height: 1.8;
        font-size: 1.05rem;
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

# Player selection
player1_name = st.sidebar.selectbox(
    "Select Player 1:",
    options=["Select a player"] + st.session_state.players_list['full_name'].tolist(),
    key="player1"
)

player2_name = st.sidebar.selectbox(
    "Select Player 2:",
    options=["Select a player"] + st.session_state.players_list['full_name'].tolist(),
    key="player2"
)

# Only proceed if both players are selected
if player1_name == "Select a player" or player2_name == "Select a player":
    st.info("Please select both players to see the comparison")
    st.stop()


player1_id = st.session_state.players_list[st.session_state.players_list['full_name'] == player1_name]['id'].iloc[0]
player2_id = st.session_state.players_list[st.session_state.players_list['full_name'] == player2_name]['id'].iloc[0]

# Get player career stats with error handling
try:
    with st.spinner(f"Loading {player1_name}'s career data..."):
        player1_stats = get_player_stats(player1_id)
    with st.spinner(f"Loading {player2_name}'s career data..."):
        player2_stats = get_player_stats(player2_id)
except Exception as e:
    st.error("⚠️ NBA API is currently unavailable or slow. Please try again in a few moments.")
    st.info("💡 Tip: The NBA API can be slow during peak times. Try refreshing the page or selecting different players.")
    st.stop()

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

col1_label = f"{player1_name} ({season1})"
col2_label = f"{player2_name} ({season2})"

# Create comparison dataframe
comparison_df = pd.DataFrame({
    'Stat': ['PPG', 'RPG', 'APG', 'SPG', 'BPG', 'FG%', '3P%', 'FT%'],
    col1_label: [
        player1_season_stats['PTS'] / 100, 
        player1_season_stats['REB'] / 100, 
        player1_season_stats['AST'] / 100, 
        player1_season_stats['STL'] / 100, 
        player1_season_stats['BLK'] / 100, 
        player1_season_stats['FG_PCT'] * 100, 
        player1_season_stats['FG3_PCT'] * 100, 
        player1_season_stats['FT_PCT'] * 100
    ],
    col2_label: [
        player2_season_stats['PTS'] / 100, 
        player2_season_stats['REB'] / 100, 
        player2_season_stats['AST'] / 100, 
        player2_season_stats['STL'] / 100, 
        player2_season_stats['BLK'] / 100, 
        player2_season_stats['FG_PCT'] * 100, 
        player2_season_stats['FG3_PCT'] * 100, 
        player2_season_stats['FT_PCT'] * 100
    ]
})

# Display basic stats bar chart
stats = comparison_df['Stat'].tolist()
players = [col for col in comparison_df.columns if col != 'Stat']

fig = make_subplots(rows=1, cols=len(stats), subplot_titles=stats)

for i, stat in enumerate(stats):
    values = comparison_df[comparison_df['Stat'] == stat][players].values[0]
    fig.add_trace(
    go.Bar(
        x=players,
        y=values,
        text=[f"{v:.2f}" for v in values],
        textposition='inside', 
        marker_color=['#1D428A', '#C8102E'],
        showlegend=False,
        cliponaxis=False  # Prevents text from being clipped or overlaid
    ),
    row=1, col=i+1
)

    fig.update_xaxes(title_text="", row=1, col=i+1)
    fig.update_yaxes(title_text="", row=1, col=i+1)

fig.update_layout(
    height=400,  # or higher

    width=250*len(stats),
    title_text="Player Comparison: Stat by Stat",
    showlegend=False,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Get shot data for each player/season
with st.spinner("Loading shot chart data..."):
    df1 = get_shotchart_df(player1_id, season1)
    df2 = get_shotchart_df(player2_id, season2)

# Only show shot charts if we have data
if not df1.empty and not df2.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### {col1_label} Made Shots")
        st.plotly_chart(plot_made_shots_scatter(df1, player1_name, season1), use_container_width=True)
    with col2:
        st.markdown(f"### {col2_label} Made Shots")
        st.plotly_chart(plot_made_shots_scatter(df2, player2_name, season2), use_container_width=True)
else:
    st.warning("⚠️ Shot chart data is temporarily unavailable. The basic stats comparison above is still accurate!")

# AI-Powered Comparison Insights
st.markdown("---")
st.markdown("## AI-Powered Comparison Insights")

# Add a button to generate insights
if st.button("🔮 Generate AI Analysis", type="primary", use_container_width=True):
    with st.spinner("🏀 Analyzing players with AI..."):
        try:
            # Initialize Bedrock client
            bedrock = BedrockClient(region_name="us-east-1")

            # Generate comparison
            insights = bedrock.generate_player_comparison(
                player1_name=player1_name,
                player2_name=player2_name,
                season1=season1,
                season2=season2,
                player1_stats=player1_season_stats,
                player2_stats=player2_season_stats
            )

            # Convert markdown-style formatting to HTML
            insights_html = insights.replace('\n\n', '</p><p>').replace('\n', '<br>')

            # Display insights in a nice container
            st.markdown(
                f"""
                <div class='ai-insights-card'>
                    <h3>📊 Expert Analysis</h3>
                    <p>{insights_html}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"❌ Failed to generate AI insights: {str(e)}")
            st.info("💡 Make sure AWS Bedrock is configured and model access is enabled.")

# Footer
st.markdown("---")
st.markdown("Made by Omar Rafiq. Data provided by NBA API.")