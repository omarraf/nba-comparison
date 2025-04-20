import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import requests
from io import BytesIO

def get_all_players():
    """Get a list of all NBA players."""
    all_players = players.get_players()
    return pd.DataFrame(all_players)

def get_player_stats(player_id):
    """Get career stats for a specific player."""
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    return career_stats.get_data_frames()[0]

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