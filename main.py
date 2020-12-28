from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re
from variables import *

team_opponents_dict = {}
team_opponent_position_stats_dict = {}
player_object_dict = {}

class Player():
    '''
    Class representing a player, containing information that will be used to
    tabulate a score for the player for the given week (stored in the object)
    which will then be compared to set the lineup.
    '''
    def __init__(self, player_name, team, minutes_per_game, projection_dict, current_season_stats_dict):
        self.player_name = player_name
        self.team = team
        self.minutes_per_game = minutes_per_game
        self.projection_dict = projection_dict # Per 36 minutes
        self.current_season_stats_dict = current_season_stats_dict # Per game

    def getPlayerName(self):
        return self.player_name
    
    def getPlayerTeam(self):
        return self.team
    
    def getPlayerMinutesPerGame(self):
        return self.minutes_per_game
    
    def getPlayerProjectionDict(self):
        return self.projection_dict
    
    def getPlayerCurrentSeasonStatsDict(self):
        return self.current_season_stats_dict

    def setPlayerScore(self, score):
        self.player_score = score
    
    def getPlayerScore(self):
        return self.player_score

def scrape_bbref_player(player_name):
    '''
    Scrape the Basketball Reference page for the given player and return a player
    object containing the player's name, team, minutes per game, projection dict,
    and current season stats dict.
    '''
    html = urlopen(player_urls[player_name])
    soup = BeautifulSoup(html, features="lxml")

    # Grab projections, which are per 36 mins
    projection_dict = {}
    projection = soup.findAll('table', attrs={'id':'projection'})
    for stat in projection_headers_dict.keys():
        projection_dict[projection_headers_dict[stat]] = float(projection[0].findAll('td', attrs={'data-stat':stat})[0].text)

    # Grab current season stats, which are per game
    current_season_stats_dict = {}
    current_season_stats = soup.findAll('tr',attrs={'id':f'per_game.20{current_year}'})
    
    for stat in current_season_stats_headers_dict.keys():
        current_season_stats_dict[current_season_stats_headers_dict[stat]] = float(current_season_stats[0].findAll('td', attrs={'data-stat':stat})[0].text)

    # Grab the player's team
    player_team = current_season_stats[0].findAll('td', attrs={'data-stat':'team_id'})[0].text

    # Grab the player's minutes per game
    player_minutes_per_game = current_season_stats[0].findAll('td', attrs={'data-stat':'mp_per_g'})[0].text

    return Player(player_name, player_team, player_minutes_per_game, projection_dict, current_season_stats_dict)

def get_team_opponents_for_week(start_date):
    '''
    Scrape the Basketball Reference page for the given team and start date to
    determine what opponents the team will be playing that week. Store in a global
    dictionary.
    '''
    for team_name in team_abbreviation_to_name_dict.keys():
        opponent_list = []
        html = urlopen(schedule_url.format(team_name))
        soup = BeautifulSoup(html, features="lxml")
        games_table = soup.findAll('table',attrs={'id':'games'})[0]

        # We want to start from the following Monday from the day the program is run,
        # since that is the ESPN week for which we will be setting the lineup
        monday_date = start_date + datetime.timedelta(days = 7 - start_date.weekday())

        for day_delta in range(0, 6):
            date = monday_date + datetime.timedelta(days = day_delta)
            date_lookup_string = "{:04}-{:02}-{:02}".format(date.year, date.month, date.day)
            try:
                games_row = games_table.findChild('td',attrs={'csk':date_lookup_string}).find_parent('tr')
            except AttributeError:
                # No game is going to be played on this day
                continue
            opponent_name = games_row.findChild('td',attrs={'data-stat':'opp_name'}).text
            opponent_list.append(opponent_full_name_dict[opponent_name])

        team_opponents_dict[team_name] = opponent_list

def get_team_opponent_stats_by_position():
    '''
    Scrape www.hoopsstats.com for the opponent statistics by position data for
    each team.
    '''
    made_pattern = re.compile(r'([0-9]+\.[0-9]+)-')
    attempted_pattern = re.compile(r'-([0-9]+\.[0-9]+)')

    for position in opponent_position_statistics_urls.keys():
        html = urlopen(opponent_position_statistics_urls[position])
        soup = BeautifulSoup(html, features="lxml")

        for team_abbrev, team_name in team_abbreviation_to_name_dict.items():
            team_opponent_position_stats = {}
            # This website's HTML layout is horrifying so we have to do some bad things here...
            raw_stat_table_row = soup.find('a',text=team_name).find_parent('tr').findAll('td')
            team_opponent_position_stats["MP"] = float(raw_stat_table_row[3].text)
            team_opponent_position_stats["PTS"] = float(raw_stat_table_row[4].text)
            team_opponent_position_stats["TRB"] = float(raw_stat_table_row[5].text)
            team_opponent_position_stats["AST"] = float(raw_stat_table_row[6].text)
            team_opponent_position_stats["STL"] = float(raw_stat_table_row[7].text)
            team_opponent_position_stats["BLK"] = float(raw_stat_table_row[8].text)
            team_opponent_position_stats["TOV"] = float(raw_stat_table_row[9].text)
            team_opponent_position_stats["PF"] = float(raw_stat_table_row[10].text)
            team_opponent_position_stats["DRB"] = float(raw_stat_table_row[11].text)
            team_opponent_position_stats["ORB"] = float(raw_stat_table_row[12].text)
            team_opponent_position_stats["FG"] = float(re.findall(made_pattern, raw_stat_table_row[13].text)[0])
            team_opponent_position_stats["FGA"] = float(re.findall(attempted_pattern, raw_stat_table_row[13].text)[0])
            team_opponent_position_stats["3P"] = float(re.findall(made_pattern, raw_stat_table_row[15].text)[0])
            team_opponent_position_stats["3PA"] = float(re.findall(attempted_pattern, raw_stat_table_row[15].text)[0])
            team_opponent_position_stats["FT"] = float(re.findall(made_pattern, raw_stat_table_row[17].text)[0])
            team_opponent_position_stats["FTA"] = float(re.findall(attempted_pattern, raw_stat_table_row[17].text)[0])

            if team_abbrev not in team_opponent_position_stats_dict.keys():
                team_opponent_position_stats_dict[team_abbrev] = {position : team_opponent_position_stats}
            else:
                team_opponent_position_stats_dict[team_abbrev][position] = team_opponent_position_stats

    print(team_opponent_position_stats_dict)

if __name__ == "__main__":
    # Collect the projections and stats for each player on the team
    for player_name in player_list:
        player_object_dict[player_name] = scrape_bbref_player(player_name)

    # Collect the opponents for each team for the following week    
    get_team_opponents_for_week(datetime.datetime.today())

    # Collect the opponent stats by position for each team
    get_team_opponent_stats_by_position()