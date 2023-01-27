import pandas as pd

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



