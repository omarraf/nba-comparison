import streamlit as st
from nba_api.stats.static import players
import pandas as pd



st.title("NBA Player Comparison Dashboard")

player_list = players.get_players()
df = pd.DataFrame(player_list)
st.write("first 10 nba players in the database:")
st.table(df[['full_name']].head(10))