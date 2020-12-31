import urllib.request as request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re
import requests
import json
from unidecode import unidecode
from variables import *
from cookies import *

'''
To-Dos:

1. Automate weighting for projected/real stats - DONE
2. Automate pulling URLs for players - DONE
3. Access ESPN lineup to pull players without having to manually enter them (not sure if this is doable) - DONE
4. Same for scoring settings - DONE
5. Same for waivers?
'''

team_object_dict = {}
player_object_dict = {}
scoring_settings = {}

class Player():
    '''
    Class representing a player, containing information that will be used to
    tabulate a score for the player for the given week (stored in the object)
    which will then be compared to set the lineup.
    '''
    def __init__(self, player_name):
        self.player_name = player_name
        self.player_positions = []
        self.player_bbref_url = ""
        self.has_projection = True

    def getPlayerName(self):
        return self.player_name
    
    def setPlayerTeam(self, team):
        self.team = team

    def getPlayerTeam(self):
        return self.team

    def addPlayerPosition(self, position):
        self.player_positions.append(position)


    def getPlayerPositions(self):
        return self.player_positions

    def setBBRefUrl(self, url):
        self.player_bbref_url = url

    def getBBRefUrl(self):
        return self.player_bbref_url

    def setPlayerHasProjection(self, player_has_projection):
        self.has_projection = player_has_projection
    
    def getPlayerHasProjection(self):
        return self.has_projection

    def setPlayerMinutesPerGame(self, minutes_per_game):
        self.minutes_per_game = minutes_per_game

    def getPlayerMinutesPerGame(self):
        return self.minutes_per_game
    
    def setPlayerProjectionDict(self, projection_dict):
        self.projection_dict = projection_dict

    def getPlayerProjectionDict(self):
        return self.projection_dict
    
    def setPlayerCurrentSeasonStatsDict(self, current_season_stats_dict):
        self.current_season_stats_dict = current_season_stats_dict

    def getPlayerCurrentSeasonStatsDict(self):
        return self.current_season_stats_dict

    def tabulatePlayerESPNPointsPerGame(self):
        '''
        Return the current value of a player's ESPN points per game, using the
        projected season stats and the current season stats, with more weight
        given to the current season stats as the season progresses.
        '''
        points_based_on_projection = 0
        points_based_on_season = 0

        if self.has_projection:
            for stat, value in self.projection_dict.items():
                if stat in scoring_settings.keys():
                    points_based_on_projection += value * scoring_settings[stat]

        for stat, value in self.current_season_stats_dict.items():
            if stat in scoring_settings.keys():
                points_based_on_season += value * scoring_settings[stat]

        points_based_on_projection = points_based_on_projection * (self.minutes_per_game / 36.0) # Adjust projections for actual minutes the player plays

        current_season_stats_weight, projected_stats_weight = calculateStatWeighting(self.team)

        if self.has_projection:
            weighted_points_based_on_projection = points_based_on_projection * projected_stats_weight
            weighted_points_based_on_season = points_based_on_season * current_season_stats_weight

            return weighted_points_based_on_projection + weighted_points_based_on_season
        else:
            return points_based_on_season

    def setPlayerScore(self, score):
        self.player_score = score
    
    def getPlayerScore(self):
        return self.player_score

class Team():
    '''
    Class representing a team, containing information the opponents the team
    will face for the given week and the team's opponent statistics by position.
    '''
    def __init__(self, team_name):
        self.team_name = team_name
        self.opponents_list = []
        self.opponent_stats_dict = {}
    
    def getTeamName(self):
        return self.team_name

    def setOpponentsList(self, opponents_list):
        self.opponents_list = opponents_list
    
    def getOpponentsList(self):
        return self.opponents_list
    
    def setOpponentStatsDict(self, opponent_stats_dict):
        self.opponent_stats_dict = opponent_stats_dict

    def getOpponentStatsDict(self,):
        return self.opponent_stats_dict

    def tabulateTeamPositionalESPNPoints(self, position):
        '''
        For the given position, determine the number of fantasy points that position
        scores against this team.
        '''
        points = 0

        for stat, value in self.opponent_stats_dict[position].items():
            if stat in scoring_settings.keys():
                points += value * scoring_settings[stat]
        
        return points

def calculateStatWeighting(team):
    '''
    Get the weight for the current season stats and projected stats. This is
    based on the given team's number of games played, such that more weight will
    be given to the current season stats as the season progresses. Once the team
    has played half of its games for the season, the projected stats will no
    longer have any bearing.
    '''
    record_pattern = re.compile(r' (\d+)\-(\d+),')
    html = request.urlopen(team_page_url.format(team, current_year))
    soup = BeautifulSoup(html, features="lxml")
    record = re.findall(record_pattern, soup.findAll('p')[2].text)
    games_played = int(record[0][0]) + int(record[0][1])

    current_season_stats_weight = float(games_played / total_games_in_season) * 2.0
    projected_stats_weight = max(1.0 - current_season_stats_weight, 0)

    return current_season_stats_weight, projected_stats_weight

def get_scoring_settings_from_espn():
    '''
    Retrieve the league's scoring settings from ESPN.
    '''
    r = requests.get(espn_league_base_url, params = {'view' : 'mSettings'}, cookies = {'swid' : SWID, 'espn_s2' : ESPN_S2})
    json_request = json.loads(r.content)

    scoring_items = json_request['settings']['scoringSettings']['scoringItems']

    for scoring_item in scoring_items:
        scoring_settings[espn_stat_ids_dict[scoring_item['statId']]] = scoring_item['points']

def get_players_from_espn():
    '''
    Retrieve the team's players from ESPN.
    '''
    r = requests.get(espn_league_base_url, params = {'view' : 'mRoster'}, cookies = {'swid' : SWID, 'espn_s2' : ESPN_S2})
    json_request = json.loads(r.content)

    roster = json_request['teams'][team_id - 1]['roster']['entries']

    for player_index in range(len(roster)):
        player_json = roster[player_index]['playerPoolEntry']['player']
        player_object = Player(player_json['fullName'])
        for position_index in range(len(player_json['eligibleSlots'])):
            position_id = player_json['eligibleSlots'][position_index]
            if position_id <= 4:
                player_object.addPlayerPosition(fantasy_team_position_list[position_id])
        player_last_name = player_json['lastName'].replace('.','')
        player_first_name = player_json['firstName'].replace('.', '')
        scrape_bbref_player(player_object, player_json['fullName'], player_last_name, player_first_name)
        player_object_dict[player_json['fullName']] = player_object

def get_bbref_url(player_object, player_full_name, player_last_name, player_first_name):
    '''
    Get the URL for this player's basketball-reference.com page.
    '''
    for attempts in range(1,10):
        bbref_url = bbref_base_url.format(player_last_name[0], player_last_name[0:5], player_first_name[0:2], attempts).lower()
        html = request.urlopen(bbref_url)
        soup = BeautifulSoup(html, features="lxml")

        try:
            soup.findAll('table', attrs={'id':'projection'})[0]
        except IndexError:
            try:
                soup.findAll('tr',attrs={'id':f'per_game.20{current_year}'})[0]
            except IndexError:
                continue

        if player_full_name != unidecode(soup.find('h1', attrs={'itemprop' : 'name' }).text.replace('\n','')):
            continue

        return bbref_url

    raise Exception(f"Can't find the basketball reference page for payer {player_full_name}")


def scrape_bbref_player(player_object, player_full_name, player_last_name, player_first_name):
    '''
    Scrape the Basketball Reference page for the given player and return a player
    object containing the player's name, team, minutes per game, projection dict,
    and current season stats dict.

    The index errors in this function are there to catch instances where a player
    has not yet played this season, and therefore has not accrued any stats.
    '''

    bbref_url = get_bbref_url(player_object, player_full_name, player_last_name, player_first_name)

    html = request.urlopen(bbref_url)
    soup = BeautifulSoup(html, features="lxml")

    # Grab projections, which are per 36 mins
    projection_dict = {}
    try:
        projection = soup.findAll('table', attrs={'id':'projection'})
        for stat in projection_headers_dict.keys():
            projection_dict[projection_headers_dict[stat]] = float(projection[0].findAll('td', attrs={'data-stat':stat})[0].text)
    except IndexError:
        # If we've gotten this far and still have an IndexError, then this is probably a rookie who just has no projection
        player_object.setPlayerHasProjection(False)

    player_object.setPlayerProjectionDict(projection_dict)

    # Grab current season stats, which are per game
    current_season_stats_dict = {}
    current_season_stats = soup.findAll('tr',attrs={'id':f'per_game.20{current_year}'})

    try:
        for stat in current_season_stats_headers_dict.keys():
            current_season_stats_dict[current_season_stats_headers_dict[stat]] = float(current_season_stats[0].findAll('td', attrs={'data-stat':stat})[0].text)
    except IndexError:
        for stat in current_season_stats_headers_dict.keys():
            current_season_stats_dict[current_season_stats_headers_dict[stat]] = 0.0

    player_object.setPlayerCurrentSeasonStatsDict(current_season_stats_dict)

    # Grab the player's team
    try:
        player_team = current_season_stats[0].findAll('td', attrs={'data-stat':'team_id'})[0].text
    except IndexError:
        player_team = soup.findAll('tr',attrs={'id':f'per_game.20{current_year - 1}'})[0].findAll('td', attrs={'data-stat':'team_id'})[0].text
    player_object.setPlayerTeam(player_team)

    # Grab the player's minutes per game
    try:
        player_minutes_per_game = float(current_season_stats[0].findAll('td', attrs={'data-stat':'mp_per_g'})[0].text)
    except IndexError:
        player_minutes_per_game = 0.0
    player_object.setPlayerMinutesPerGame(player_minutes_per_game)

def get_team_opponents_for_week(start_date):
    '''
    Scrape the Basketball Reference page for the given team and start date to
    determine what opponents the team will be playing that week. Store in a global
    dictionary.
    '''
    for team_name in team_abbreviation_to_name_dict.keys():
        opponent_list = []
        html = request.urlopen(schedule_url.format(team_name, current_year))
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

        team_object_dict[team_name].setOpponentsList(opponent_list)

def get_team_opponent_stats_by_position():
    '''
    Scrape www.hoopsstats.com for the opponent statistics by position data for
    each team.
    '''
    made_pattern = re.compile(r'([0-9]+\.[0-9]+)-')
    attempted_pattern = re.compile(r'-([0-9]+\.[0-9]+)')

    for position in opponent_position_statistics_urls.keys():
        html = request.urlopen(opponent_position_statistics_urls[position])
        soup = BeautifulSoup(html, features="lxml")

        for team_abbrev, team_name in team_abbreviation_to_name_dict.items():
            team_opponent_position_stats = {}
            # This website's HTML layout is horrifying so we have to do some bad things here...
            raw_stat_table_row = soup.find('a',text=team_name).find_parent('tr').findAll('td')
            team_opponent_position_stats["MP"] = float(raw_stat_table_row[3].text)
            team_opponent_position_stats["PTS"] = float(raw_stat_table_row[4].text)
            team_opponent_position_stats["REB"] = float(raw_stat_table_row[5].text)
            team_opponent_position_stats["AST"] = float(raw_stat_table_row[6].text)
            team_opponent_position_stats["STL"] = float(raw_stat_table_row[7].text)
            team_opponent_position_stats["BLK"] = float(raw_stat_table_row[8].text)
            team_opponent_position_stats["TOV"] = float(raw_stat_table_row[9].text)
            team_opponent_position_stats["PF"] = float(raw_stat_table_row[10].text)
            team_opponent_position_stats["DRB"] = float(raw_stat_table_row[11].text)
            team_opponent_position_stats["ORB"] = float(raw_stat_table_row[12].text)
            team_opponent_position_stats["FGM"] = float(re.findall(made_pattern, raw_stat_table_row[13].text)[0])
            team_opponent_position_stats["FGA"] = float(re.findall(attempted_pattern, raw_stat_table_row[13].text)[0])
            team_opponent_position_stats["3PM"] = float(re.findall(made_pattern, raw_stat_table_row[15].text)[0])
            team_opponent_position_stats["3PA"] = float(re.findall(attempted_pattern, raw_stat_table_row[15].text)[0])
            team_opponent_position_stats["FTM"] = float(re.findall(made_pattern, raw_stat_table_row[17].text)[0])
            team_opponent_position_stats["FTA"] = float(re.findall(attempted_pattern, raw_stat_table_row[17].text)[0])

            team_object_dict[team_abbrev].getOpponentStatsDict()[position] = team_opponent_position_stats

def generate_player_score(player):
    '''
    First, get the number of fantasy points we can project for this player on a
    per-game basis. Then, get the number of fantasy points this player's position
    scores against his opponents for this week. Take the average of this number
    per-game, and find the mean between this number and the player's fantasy
    points. Finally, multiply this by the number of games the player will
    play this week, with a small adjustment to consider the fact that a 4 game
    slate may end up with a rest day for the player.
    '''
    espn_points_for_player = player.tabulatePlayerESPNPointsPerGame()
    espn_points_for_position_for_opponents = 0
    team_opponents_list = team_object_dict[player.team].opponents_list

    for team in team_opponents_list:
        espn_points_for_position_for_opponents += team_object_dict[team].tabulateTeamPositionalESPNPoints(player.getPlayerPositions()[0])

    number_of_games = len(team_opponents_list)
    average_espn_points_for_position_for_opponents = espn_points_for_position_for_opponents / number_of_games

    raw_score = (espn_points_for_player + average_espn_points_for_position_for_opponents) / 2

    adjusted_score = raw_score * number_of_games
    if number_of_games == 4:
        adjusted_score = adjusted_score * 0.90

    player.setPlayerScore(adjusted_score)

def recurse_lineup(fantasy_position_to_player_dict, current_lineup_players, position_index, current_score, high_score, best_lineup, tested_permutations):
    '''
    Recursively check the given position and dict's permutations until we get to a full lineup. Once we get to a full
    lineup, check the score and see if it higher.
    '''
    for player in fantasy_position_to_player_dict[fantasy_team_position_list[position_index]]:
        if player not in current_lineup_players:
            current_score += player_object_dict[player].getPlayerScore()
            current_lineup_players.append(player)
            if position_index == (len(fantasy_position_to_player_dict.keys()) - 1):
                tested_permutations += 1
                if current_score > high_score:
                    high_score = current_score
                    best_lineup = [player for player in current_lineup_players]
            else:
                high_score, best_lineup, tested_permutations = recurse_lineup(fantasy_position_to_player_dict, current_lineup_players, position_index + 1, current_score, high_score, best_lineup, tested_permutations)
            current_score -= player_object_dict[player].getPlayerScore()
            current_lineup_players.remove(player)
    return high_score, best_lineup, tested_permutations

def generate_optimal_lineup():
    '''
    Iterate through every possible lineup and generate scores for each to
    determine the best lineup.
    '''
    fantasy_position_to_player_dict = {"PG" : [], "SG" : [], "SF" : [], "PF" : [], "C" : [], "G" : [], "F" : [], "UTIL1" : [], "UTIL2" : [], "UTIL3" : []}

    for position_group in fantasy_team_position_dict.keys():
        for position in fantasy_team_position_dict[position_group]:
            for player_name, player in player_object_dict.items():
                if position in player.getPlayerPositions():
                    fantasy_position_to_player_dict[position_group].append(player_name)
    
    high_score, best_lineup, tested_permutations = recurse_lineup(fantasy_position_to_player_dict, [], 0, 0, 0, [], 0)

    print_optimal_lineup(best_lineup, high_score, tested_permutations)

def print_optimal_lineup(best_lineup, high_score, tested_permutations):
    start_date = datetime.datetime.today() + datetime.timedelta(days = 7 - datetime.datetime.today().weekday())

    print("Optimal lineup for the week beginning {:04}-{:02}-{:02}\n".format(start_date.year, start_date.month, start_date.day))

    for index in range(len(best_lineup)):
        print(f"{fantasy_team_position_list[index]}: {best_lineup[index]} - Projected Score: {player_object_dict[best_lineup[index]].getPlayerScore()}")

    print(f"\nTotal Projected Score: {high_score}\nNumber of Tested Permutations: {tested_permutations}")                                     

if __name__ == "__main__":
    # Get league scoring settings
    get_scoring_settings_from_espn()

    # Create objects for each team
    for team_name in team_abbreviation_to_name_dict.keys():
        team_object_dict[team_name] = Team(team_name)

    # Collect the opponents for each team for the following week    
    get_team_opponents_for_week(datetime.datetime.today())

    # Collect the opponent stats by position for each team
    get_team_opponent_stats_by_position()

    # Collect the projections and stats for each player on the team, and generate
    # scores
    get_players_from_espn()
    for player_name, player in player_object_dict.items():
        generate_player_score(player)

    generate_optimal_lineup()