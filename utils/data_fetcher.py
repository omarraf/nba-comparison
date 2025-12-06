import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import requests
from io import BytesIO
from nba_api.stats.endpoints import shotchartdetail
import time

def get_shotchart_df(player_id, season):
    """Get shot chart data with retry logic."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            time.sleep(0.6)  # NBA API rate limit prevention
            shotchart = shotchartdetail.ShotChartDetail(
                team_id=0,  # 0 means all teams (useful for players who switched teams)
                player_id=player_id,
                season_type_all_star='Regular Season',
                season_nullable=season,
                timeout=30  # Increase timeout to 30 seconds
            )
            df = shotchart.get_data_frames()[0]
            return df
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                # Return empty dataframe if all retries fail
                return pd.DataFrame()

def get_all_players():
    """Get a list of all NBA players."""
    all_players = players.get_players()
    return pd.DataFrame(all_players)

def get_player_stats(player_id):
    """Get career stats for a specific player with retry logic."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            time.sleep(0.6)  # NBA API rate limit prevention
            career_stats = playercareerstats.PlayerCareerStats(
                player_id=player_id,
                timeout=30  # Increase timeout to 30 seconds
            )
            return career_stats.get_data_frames()[0]
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                continue
            else:
                raise Exception(f"Failed to fetch player stats after {max_retries} attempts: {str(e)}")

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