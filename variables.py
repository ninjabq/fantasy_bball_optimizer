current_year = 21

opponent_position_statistics_urls = \
{
    "SF" : f"http://www.hoopsstats.com/basketball/fantasy/nba/opponentstats/{current_year}/8/eff/1-1",
    "PF" : f"http://www.hoopsstats.com/basketball/fantasy/nba/opponentstats/{current_year}/9/eff/1-1",
    "C" : f"http://www.hoopsstats.com/basketball/fantasy/nba/opponentstats/{current_year}/10/eff/1-1",
    "SG" : f"http://www.hoopsstats.com/basketball/fantasy/nba/opponentstats/{current_year}/11/eff/1-1",
    "PG" : f"http://www.hoopsstats.com/basketball/fantasy/nba/opponentstats/{current_year}/12/eff/1-1",
}

schedule_url = "https://www.basketball-reference.com/teams/{}/2021_games.html"

position_list = \
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

scoring_settings = \
    {
        "FG" : 2,
        "FGA" : -1,
        "FT" : 1,
        "FTA" : -1,
        "3P" : 1,
        "TRB" : 1,
        "AST" : 2,
        "STL" : 3,
        "BLK" : 4,
        "TOV" : -2,
        "PTS" : 1
    }

player_list = \
[
    "Simmons, Ben",
    "Harden, James",
    "Bazley, Darius",
    "Gallinari, Danilo",
    "Bryant, Thomas",
    "Wright, Delon",
    "Middleton, Khris",
    "Drummond, Andre",
    "Vucevic, Nikola",
    "Plumlee, Mason",
    "Warren, T.J.",
#    "Green, Draymond", have to ignore draymond for now cuz he aint played yet
    "Ingles, Joe",
    "Reddish, Cam",
]

player_positions = \
{
    "Simmons, Ben" : ["PG"],
    "Harden, James" : ["SG", "PG"],
    "Bazley, Darius" : ["SF"],
    "Gallinari, Danilo" : ["PF", "SF"],
    "Bryant, Thomas" : ["C"],
    "Wright, Delon" : ["SG", "PG"],
    "Middleton, Khris" : ["SF", "SG"],
    "Drummond, Andre" : ["C"],
    "Vucevic, Nikola" : ["C"],
    "Plumlee, Mason" : ["C"],
    "Warren, T.J." : ["SF"],
    "Green, Draymond" : ["PF"],
    "Ingles, Joe" : ["SF"],
    "Reddish, Cam" : ["SF", "SG"],
}

player_urls = \
{
    "Simmons, Ben" : "https://www.basketball-reference.com/players/s/simmobe01.html",
    "Harden, James" : "https://www.basketball-reference.com/players/h/hardeja01.html",
    "Bazley, Darius" : "https://www.basketball-reference.com/players/b/bazleda01.html",
    "Gallinari, Danilo" : "https://www.basketball-reference.com/players/g/gallida01.html",
    "Bryant, Thomas" : "https://www.basketball-reference.com/players/b/bryanth01.html",
    "Wright, Delon" : "https://www.basketball-reference.com/players/w/wrighde01.html",
    "Middleton, Khris" : "https://www.basketball-reference.com/players/m/middlkh01.html",
    "Drummond, Andre" : "https://www.basketball-reference.com/players/d/drumman01.html",
    "Vucevic, Nikola" : "https://www.basketball-reference.com/players/v/vucevni01.html",
    "Plumlee, Mason" : "https://www.basketball-reference.com/players/p/plumlma01.html",
    "Warren, T.J." : "https://www.basketball-reference.com/players/w/warretj01.html",
    "Green, Draymond" : "https://www.basketball-reference.com/players/g/greendr01.html",
    "Ingles, Joe" : "https://www.basketball-reference.com/players/i/inglejo01.html",
    "Reddish, Cam" : "https://www.basketball-reference.com/players/r/reddica01.html",
}

projection_headers_dict = \
{
    "fg_per_mp" : "FG",
    "fga_per_mp" : "FGA",
    "fg3_per_mp" : "3P",
    "fg3a_per_mp" : "3PA",
    "ft_per_mp" : "FT",
    "fta_per_mp" : "FTA",
    "orb_per_mp" : "ORB",
    "trb_per_mp" : "TRB",
    "ast_per_mp" : "AST",
    "stl_per_mp" : "STL",
    "blk_per_mp" : "BLK",
    "tov_per_mp" : "TOV",
    "pf_per_mp" : "PF",
    "pts_per_mp" :"PTS"
}

current_season_stats_headers_dict = \
{
    "fg_per_g" : "FG",
    "fga_per_g" : "FGA",
    "fg3_per_g" : "3P",
    "fg3a_per_g" : "3PA",
    "ft_per_g" : "FT",
    "fta_per_g" : "FTA",
    "orb_per_g" : "ORB",
    "trb_per_g" : "TRB",
    "ast_per_g" : "AST",
    "stl_per_g" : "STL",
    "blk_per_g" : "BLK",
    "tov_per_g" : "TOV",
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