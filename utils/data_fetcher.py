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
