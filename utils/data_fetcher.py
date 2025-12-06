import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import requests
from io import BytesIO
from nba_api.stats.endpoints import shotchartdetail
import time
import streamlit as st
from nba_api.stats.library.http import NBAStatsHTTP

# Configure NBA API headers to work on Streamlit Cloud
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.nba.com/',
    'Origin': 'https://www.nba.com',
    'Connection': 'keep-alive',
}

# Set custom headers for all NBA API requests
NBAStatsHTTP().headers = headers

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_shotchart_df(player_id, season):
    """Get shot chart data with retry logic."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                time.sleep(1)  # Small delay between retries

            shotchart = shotchartdetail.ShotChartDetail(
                team_id=0,  # 0 means all teams (useful for players who switched teams)
                player_id=player_id,
                season_type_all_star='Regular Season',
                season_nullable=season,
                timeout=30
            )
            df = shotchart.get_data_frames()[0]
            return df
        except Exception as e:
            if attempt < max_retries - 1:
                continue
            else:
                # Return empty dataframe if all retries fail
                return pd.DataFrame()

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_all_players():
    """Get a list of all NBA players."""
    all_players = players.get_players()
    return pd.DataFrame(all_players)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_player_stats(player_id):
    """Get career stats for a specific player with retry logic."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                time.sleep(1)  # Small delay between retries

            career_stats = playercareerstats.PlayerCareerStats(
                player_id=player_id,
                timeout=30
            )
            return career_stats.get_data_frames()[0]
        except Exception as e:
            if attempt < max_retries - 1:
                continue
            else:
                raise Exception(f"NBA API unavailable. Please try again in a moment or select different players.")

def get_player_image(player_id):
    """Get player headshot image."""
    url = f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            # Return a placeholder image if player image not found
            return "https://cdn.nba.com/logos/nba/fallback-headshot.png"
    except:
        return "https://cdn.nba.com/logos/nba/fallback-headshot.png"