import streamlit as st
from nba_api.stats.static import players
import pandas as pd



st.title("NBA Player Comparison Dashboard")

player_list = players.get_players()
df = pd.DataFrame(player_list)
st.write("first 10 nba players in the database:")
st.table(df[['full_name']].head(10))

player_names = df['full_name'].tolist()
selected_player = st.selectbox("Select an NBA player:", player_names)
player_id = df[df['full_name'] == selected_player]['id'].values[0]
st.write("selected player: {selected_player} (ID: {player_id})")

