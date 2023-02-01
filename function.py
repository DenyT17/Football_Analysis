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

def table_in_season(games_data,competitions_data,league,year):
    league_name=competitions_data['competition_id'].loc[(competitions_data['competition_code']==league)|
                                      (competitions_data['name']==league)].reset_index(drop=True).iloc[0]

    all_matches=games_data.loc[(games_data['competition_id']==league_name)&
                                (games_data['season']==year)&
                                (games_data['competition_type']=='domestic_league')].reset_index(drop=True)
    clubs=all_matches['club_home_name'].unique()
    table=pd.DataFrame(columns=clubs,index=['Wins','Draws','Loses','Points'])
    wins=0
    draws=0
    loses=0
    for club in clubs:
        matches=all_matches.loc[(all_matches['club_home_name']==club)|(all_matches['club_away_name']==club)]
        for index,row in matches.iterrows():
            if row['club_home_name']==club:
                if row['home_club_goals']>row['away_club_goals']:
                    wins+=1
                elif row['home_club_goals'] < row['away_club_goals']:
                    loses += 1
                else:
                    draws+=1
            elif row['club_away_name'] == club:
                if row['home_club_goals'] < row['away_club_goals']:
                    wins += 1
                elif row['home_club_goals'] > row['away_club_goals']:
                    loses += 1
                else:
                    draws += 1
        table.at['Wins',club]=wins
        table.at['Loses',club]=loses
        table.at['Draws',club]=draws
        table.at['Points',club]=wins*3+draws
        wins = 0
        draws = 0
        loses = 0
    table=table.T.sort_values(by=['Points'],ascending=False)
    table=table.reset_index().rename(columns={'index':'Team'})
    return table

def best_scorers(competitions_data,league,year,games_data,appearances):
    league_name=competitions_data['competition_id'].loc[(competitions_data['competition_code']==league)|
                                      (competitions_data['name']==league)].reset_index(drop=True).iloc[0]
    all_matches = games_data['game_id'].loc[(games_data['competition_id'] == league_name) &
                                 (games_data['season'] == year) &
                                 (games_data['competition_type'] == 'domestic_league')].reset_index(drop=True)
    all_appearances=appearances[['game_id','player_club_id',
                                 'player_name','assists','goals']].merge(all_matches,on='game_id')
    players=all_appearances['player_name'].unique()
    goals=0
    scorers=pd.DataFrame()
    for player in players:
        appearance = all_appearances.loc[(all_appearances['player_name'] == player)]
        goals=appearance['goals'].sum()
        new_row=pd.DataFrame([{'Player Name':player,'Goals':goals}])
        scorers=pd.concat([scorers,new_row])
    scorers=scorers.sort_values(by=['Goals'],ascending=False).reset_index(drop=True)
    scorers.index=scorers.index+1
    return scorers

