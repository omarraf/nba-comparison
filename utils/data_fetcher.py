import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import requests
from io import BytesIO
from nba_api.stats.endpoints import shotchartdetail
import time
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_shotchart_df(player_id, season):
    """Get shot chart data with retry logic."""
    max_retries = 5  # Increased retries
    for attempt in range(max_retries):
        try:
            if attempt > 0:  # Only sleep on retries
                time.sleep(2 ** attempt)  # Exponential backoff

            shotchart = shotchartdetail.ShotChartDetail(
                team_id=0,  # 0 means all teams (useful for players who switched teams)
                player_id=player_id,
                season_type_all_star='Regular Season',
                season_nullable=season,
                timeout=60  # Increase timeout to 60 seconds
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
    max_retries = 5  # Increased retries
    for attempt in range(max_retries):
        try:
            if attempt > 0:  # Only sleep on retries
                time.sleep(2 ** attempt)  # Exponential backoff: 2s, 4s, 8s, 16s

            career_stats = playercareerstats.PlayerCareerStats(
                player_id=player_id,
                timeout=60  # Increase timeout to 60 seconds
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