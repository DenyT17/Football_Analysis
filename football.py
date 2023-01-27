import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from function import *
appearances_data=pd.read_csv('appearances.csv')
club_games_data=pd.read_csv('club_games.csv')
clubs_data=pd.read_csv('clubs.csv')
competitions_data=pd.read_csv('competitions.csv')
game_events_data=pd.read_csv('game_events.csv')
games_data=pd.read_csv('games.csv')
player_valuations_data=pd.read_csv('player_valuations.csv')
players_data=pd.read_csv('players.csv')
pd.set_option('display.max_columns', None)

# Real Madrid Players Actual Price
Real_Madrid_players=club_squad("Real Madrid",players_data)
fig,ax=plt.subplots(figsize=(15,10))
sns.barplot(Real_Madrid_players,x=Real_Madrid_players['last_name'],y=Real_Madrid_players['market_value_in_eur']/10**6)
plt.title('Real Madrid players actual price')
plt.xticks(rotation=45)
plt.ylabel("Price in milon of euro")
ax.bar_label(ax.containers[0])

# History of player price
fig, ax = plt.subplots(figsize=(12, 7))
player=player_price_history('Modric',players_data,player_valuations_data)
name=player['last_name'].iloc[0]
plot=sns.lineplot(player,x=player['datetime'],y=player['market_value_in_eur']/10**6,linewidth=5,
                  marker='p',markersize=7)
plt.title('History of {0} price'.format(name))
plt.xticks(rotation=45)
plt.ylabel("Price in milon of euro")
plt.grid()
new_ticks = [i.get_text() for i in plot.get_xticklabels()]
plt.xticks(range(0, len(new_ticks), 5), new_ticks[::5])


# Age of players
players_age=players_age('Real Madrid',players_data)
club=players_age['current_club_name'].iloc[0]
fig,ax=plt.subplots(figsize=(15,10))
sns.barplot(data=players_age,x='last_name',y='age')
plt.title('{0} players age'.format(club))
plt.xticks(rotation=45)
plt.ylabel("age")
ax.bar_label(ax.containers[0])
plt.show()