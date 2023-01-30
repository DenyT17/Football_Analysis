import pandas as pd
from datetime import date
import numpy as np

def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year -((today.month, today.day) <(birthDate.month, birthDate.day))
    return age

def club_squad(club_name,players_data):
    players_columns=['player_id','first_name','last_name','country_of_citizenship',
                     'date_of_birth','position','sub_position','market_value_in_eur']
    return(players_data[players_columns].loc[(players_data['current_club_name'] == club_name)&
                            (players_data['last_season'] == 2022)])

def player_price_history(player_name,players_data,player_valuations):
    player=players_data[['player_id','first_name','last_name']].loc[(players_data['last_name'] == player_name)|
                           (players_data['first_name'] == player_name)]
    player_id=player.reset_index(drop=True)
    player_id=player_id['player_id'].iloc[0]
    price_history=player_valuations[['market_value_in_eur',
                                     'player_id','datetime']].loc[(player_valuations['player_id']==player_id)]
    return player.merge(price_history,how='left',on='player_id').sort_values(by='datetime')

def players_age(club_name,players_data):
    players_data['date_of_birth'] = pd.to_datetime(players_data['date_of_birth'], format='%Y-%m-%d')
    players_data['year'] = players_data['date_of_birth'].dt.year
    players_data['month'] = players_data['date_of_birth'].dt.month
    players_data['day'] = players_data['date_of_birth'].dt.day
    birthday=(players_data[['last_name','date_of_birth',
                            'current_club_name']].loc[(players_data['current_club_name'] == club_name)&
                            (players_data['last_season'] == 2022)]).reset_index(drop=True)
    today=date.today()
    birthday['age']=birthday.apply(lambda birthday : calculateAge(birthday['date_of_birth']),axis=1)
    return birthday
def player_year_stats(player_name,season,apperance_data,players_data):
    player=players_data[['player_id','name','last_name','last_name']].loc[(players_data['name'].str.contains(player_name))]
    player_id=player.reset_index(drop=True)
    player_id=player_id['player_id'].iloc[0]
    stats = apperance_data.loc[(apperance_data['player_id'] == player_id)].reset_index(drop=True)
    stats['date'] = pd.to_datetime(stats['date'], format='%Y-%m-%d')
    stats['year'] = stats['date'].dt.year
    stats['month'] = stats['date'].dt.month
    stats['day'] = stats['date'].dt.day
    year_stats=stats.loc[(stats['date'].dt.year==season)]
    player_stats=year_stats[['minutes_played','goals','yellow_cards','red_cards','assists']].sum()
    player_stats['matches'] = len(year_stats)
    return pd.DataFrame(player_stats.reindex(index=['matches'
                                       ,'goals','assists',
                                       'yellow_cards','red_cards'])).rename(columns={0:player_name})

