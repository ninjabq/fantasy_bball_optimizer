# Fantasy Basketball Lineup Optimizer
This script is intended to provide the best possible lineup for your fantasy team.

Caveat: It only works for ESPN leagues

Caveat 2: It only works for H2H points leagues

Caveat 3: Some of the decisions made are arbitrary so this may or may not be a random lineup generator


## Metrics
The "scoring" of a lineup is done as follows:

player score -> take a weighted average of the player's season projections and current season stats from basketball-reference.com

player opponents score -> take the average fantasy points given up to the player's position by the teams the player will face the following week

raw_score -> average the previous two scores, then multiply this by the number of games the player is set to appear in this week

adjusted_score -> bring this number down a bit if the player is going to play in 4 games, because they are likely to have a rest day or reduced minutes

## Usage
Two important things you need to do!

1. In variables.py, set espn_league_id and team_id. You can get these from the URL when you go to your My Team page
2. In cookies.py, you need to add the SWID and (if using a private league) the ESPN_S2 cookies from your web browser. You can find these in Chrome in Settings -> Privacy and Security -> Cookies and other site data -> See all cookies and site data -> type ESPN in the saerch bar -> espn.com

Then, just run the script!

## Current list of things to do
1. Potentially add support for waivers, somehow...
2. Maybe add support for daily lineup changes (probably would tell you who to set each day for the following week)
3. Maybe add support for H2H category leagues and/or rotisserie leagues