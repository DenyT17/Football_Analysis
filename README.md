# Football Analisis ⚽📈 
## Technologies 💡
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
## Description 
In this project, I analyze the typical information related to football like:

-players price 💵

-history of players price 📆

-players age 👶

I will regularly upload new version of project with new functionality. 

## Dataset📁
Dataset used in this project you can find below this [link](https://data.world/dcereijo/player-scores).
Dataset consists of several csv files,the dependencies between the files are shown in the diagram below
![diagram](https://user-images.githubusercontent.com/122997699/215274664-a33d94e5-323c-491c-b39f-843cb240632c.svg)
(the diagram is from the same source as the Dataset)

## Created functions 
At the beginning i needed only players which play in the same club. That's why i created the function club_squad function. This function return DataFrame with basic information about players in one team. To return only the current squad, I added a condition that checks whether the player played for a given club in the last season.
```python
def club_squad(club_name,players_data):
    players_columns=['player_id','first_name','last_name','country_of_citizenship',
                     'date_of_birth','position','sub_position','market_value_in_eur']
    return(players_data[players_columns].loc[(players_data['current_club_name'] == club_name)&
                            (players_data['last_season'] == 2022)])
```
In players_valuations.csv file we can find not only actual price of player. Thanks to this, we can check how the price of a given player has changed over time. First, I'm looking for a player's ID based on their first or last name. In player_price_history function I'm looking for data only of one player using his ID. 
This function returns a DataFrame with the player's name and price along with the date.
```python
def player_price_history(player_name,players_data,player_valuations):
    player=players_data[['player_id','first_name','last_name']].loc[(players_data['last_name'] == player_name)|
                           (players_data['first_name'] == player_name)]
    player_id=player.reset_index(drop=True)
    player_id=player_id['player_id'].iloc[0]
    price_history=player_valuations[['market_value_in_eur',
                                     'player_id','datetime']].loc[(player_valuations['player_id']==player_id)]
    return player.merge(price_history,how='left',on='player_id').sort_values(by='datetime')
```
In player.csv file we can find birthday date of all players. I created calculate Age function thanks to which i can calculate actual age giving birthday date.  
```python
def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year -((today.month, today.day) <(birthDate.month, birthDate.day))
    return age
```

To calculate age of each player in any team i use calculateAge function and apply() method. 
```python
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
 ```
Player statistics are very important in football. The player_year_statisticis function allows you to obtain statistics of the selected player from the selected calendar year.
```python
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
 ```
## Visualisation of results 📊 

In this moment project have functionality to display chart like as: 
#### Price of players from the selected club on the chart ( Real Madrit squad price)
![Real Madrid Actual Price](https://user-images.githubusercontent.com/122997699/215055253-56597eb2-d314-4fe6-8ad9-607d8a2a767a.png)
#### History of the player price ( Luka Modric price history )
![Modric_price_history](https://user-images.githubusercontent.com/122997699/215276595-5cbd063b-5b55-4546-9b37-bcada7f414ea.png)
#### Age of all players in the selected team
![Real_madrid_players_age](https://user-images.githubusercontent.com/122997699/215271448-13fbdfb4-e95b-46e5-8f93-7ec8d12b9284.png)
#### Player stats in one season
