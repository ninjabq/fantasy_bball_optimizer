current_year = 21
espn_league_id = 984966540
team_id = 4

total_games_in_season = 72

espn_league_base_url = f'https://fantasy.espn.com/apis/v3/games/fba/seasons/20{current_year}/segments/0/leagues/{espn_league_id}'

opponent_position_statistics_urls = \
{
    "SF" : f"http://www.hoopsstats.com/basketball/fantasy/nba/opponentstats/{current_year}/8/eff/1-1",
    "PF" : f"http://www.hoopsstats.com/basketball/fantasy/nba/opponentstats/{current_year}/9/eff/1-1",
    "C" : f"http://www.hoopsstats.com/basketball/fantasy/nba/opponentstats/{current_year}/10/eff/1-1",
    "SG" : f"http://www.hoopsstats.com/basketball/fantasy/nba/opponentstats/{current_year}/11/eff/1-1",
    "PG" : f"http://www.hoopsstats.com/basketball/fantasy/nba/opponentstats/{current_year}/12/eff/1-1",
}

schedule_url = "https://www.basketball-reference.com/teams/{}/20{}_games.html"
team_page_url = "https://www.basketball-reference.com/teams/{}/20{}.html"
bbref_base_url = "https://www.basketball-reference.com/players/{}/{}{}0{}.html"

fantasy_team_position_list = ["PG", "SG", "SF", "PF", "C", "G", "F", "UTIL1", "UTIL2", "UTIL3"]

fantasy_team_position_dict = \
{
    "PG" : ["PG"],
    "SG" : ["SG"],
    "SF" : ["SF"],
    "PF" : ["PF"],
    "C" : ["C"],
    "G" : ["PG", "SG"],
    "F" : ["SF", "PF"],
    "UTIL1" : ["PG", "SG", "SF", "PF", "C"],
    "UTIL2" : ["PG", "SG", "SF", "PF", "C"],
    "UTIL3" : ["PG", "SG", "SF", "PF", "C"],
}

projection_headers_dict = \
{
    "fg_per_mp" : "FGM",
    "fga_per_mp" : "FGA",
    "fg3_per_mp" : "3PM",
    "fg3a_per_mp" : "3PA",
    "ft_per_mp" : "FTM",
    "fta_per_mp" : "FTA",
    "orb_per_mp" : "ORB",
    "trb_per_mp" : "REB",
    "ast_per_mp" : "AST",
    "stl_per_mp" : "STL",
    "blk_per_mp" : "BLK",
    "tov_per_mp" : "TO",
    "pf_per_mp" : "PF",
    "pts_per_mp" :"PTS"
}

current_season_stats_headers_dict = \
{
    "fg_per_g" : "FGM",
    "fga_per_g" : "FGA",
    "fg3_per_g" : "3PM",
    "fg3a_per_g" : "3PA",
    "ft_per_g" : "FTM",
    "fta_per_g" : "FTA",
    "orb_per_g" : "ORB",
    "trb_per_g" : "REB",
    "ast_per_g" : "AST",
    "stl_per_g" : "STL",
    "blk_per_g" : "BLK",
    "tov_per_g" : "TO",
    "pf_per_g" : "PF",
    "pts_per_g" :"PTS"
}

opponent_full_name_dict = \
{
    "Atlanta Hawks" : "ATL",
    "Brooklyn Nets" : "BRK",
    "Philadelphia 76ers" : "PHI",
    "Orlando Magic" : "ORL",
    "Cleveland Cavaliers" : "CLE",
    "Indiana Pacers" : "IND",
    "Boston Celtics" : "BOS", # fuck the Celtics
    "Milwaukee Bucks" : "MIL",
    "Miami Heat" : "MIA",
    "New York Knicks" : "NYK",
    "Washington Wizards" : "WAS",
    "Toronto Raptors" : "TOR",
    "Chicago Bulls" : "CHI",
    "Charlotte Hornets" : "CHO",
    "Detroit Pistons" : "DET",
    "Minnesota Timberwolves" : "MIN",
    "Los Angeles Clippers" : "LAC",
    "Sacramento Kings" : "SAC",
    "San Antonio Spurs" : "SAS",
    "Oklahoma City Thunder" : "OKC",
    "New Orleans Pelicans" : "NOP",
    "Los Angeles Lakers" : "LAL",
    "Phoenix Suns" : "PHO",
    "Portland Trail Blazers" : "POR",
    "Utah Jazz" : "UTA",
    "Houston Rockets" : "HOU",
    "Memphis Grizzlies" : "MEM",
    "Denver Nuggets" : "DEN",
    "Dallas Mavericks" : "DAL",
    "Golden State Warriors" : "GSW"
}

team_abbreviation_to_name_dict = \
{
    "ATL" : "Atlanta",
    "BRK" : "Brooklyn",
    "PHI" : "Philadelphia",
    "ORL" : "Orlando",
    "CLE" : "Cleveland",
    "IND" : "Indiana",
    "BOS" : "Boston", # fuck the Celtics
    "MIL" : "Milwaukee",
    "MIA" : "Miami",
    "NYK" : "New York",
    "WAS" : "Washington",
    "TOR" : "Toronto",
    "CHI" : "Chicago",
    "CHO" : "Charlotte",
    "DET" : "Detroit",
    "MIN" : "Minnesota",
    "LAC" : "L.A.Clippers",
    "SAC" : "Sacramento",
    "SAS" : "San Antonio",
    "OKC" : "Oklahoma City",
    "NOP" : "New Orleans",
    "LAL" : "L.A.Lakers",
    "PHO" : "Phoenix",
    "POR" : "Portland",
    "UTA" : "Utah",
    "HOU" : "Houston",
    "MEM" : "Memphis",
    "DEN" : "Denver",
    "DAL" : "Dallas",
    "GSW" : "Golden State"
}

# Probably not comperehensive, only valid for H2H Points Leagues
espn_stat_ids_dict = \
{
    0 : "PTS",
    1 : "BLK",
    2 : "STL",
    3 : "AST",
    4 : "OREB",
    5 : "DREB",
    6 : "REB",
    7 : "EJ",
    8 : "FF",
    9 : "PF",
    10 : "TF",
    11 : "TO",
    12 : "DQ",
    13 : "FGM",
    14 : "FGA",
    15 : "FTM",
    16 : "FTA",
    17 : "3PM",
    18 : "3PA",
    23 : "FGMI",
    24 : "FTMI",
    25 : "3PMI",
    37 : "DD",
    38 : "TD",
    39 : "QD",
    40 : "MIN",
    41 : "GS",
    42 : "GP",
    43 : "TW",
}