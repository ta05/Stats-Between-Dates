from nba_api.stats.static import players
from nba_api.stats.endpoints import cumestatsplayer, leaguegamefinder
from dateutil.parser import parse
from datetime import datetime
import pandas as pd
import json
import time
import requests

# Retry Wrapper
def retry(func, retries: int=3):
    def retry_wrapper(*args, **kwargs) -> None:
        attempts = 0
        while attempts < retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(30)
                attempts += 1
            
    return retry_wrapper


def getPlayerId(name: str) -> str:
    return players.find_players_by_full_name(name)[0]['id']


# Gets the player's box score stats for every game between start and end dates
def getPlayerBoxScoreStats(playerID: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:

    @retry
    def getGames(playerID: str, start_date: datetime, end_date: datetime) -> list[str]:
        games = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation="P", season_type_nullable="Regular Season", player_id_nullable=playerID).get_normalized_json()
        games = json.loads(games)['LeagueGameFinderResults']
        return [game['GAME_ID'] for game in games if start_date <= parse(game['GAME_DATE']) and end_date >= parse(game['GAME_DATE'])]


    @retry
    def getGameStats(playerID: str, gameIDs: list[str]) -> pd.DataFrame:
        gameStats = cumestatsplayer.CumeStatsPlayer(player_id=playerID, game_ids=gameIDs, league_id='00', season_type_all_star="Regular Season").get_normalized_json()
        gameStats = pd.DataFrame(json.loads(gameStats)['GameByGameStats'])

        return gameStats


    gameIDs = getGames(playerID=playerID, start_date=start_date, end_date=end_date)

    data = pd.DataFrame()
    for id in gameIDs:
        time.sleep(1)
        data = pd.concat([data, getGameStats(playerID, [id])])

    return data


# Combines the box score stats into totals
def getPlayerTotalStats(boxScoreStats: pd.DataFrame) -> dict:
    totalStats = boxScoreStats[['GP', 'FG', 'FGA', 'PTS', 'FG3', 'FG3A', 'AST', 'OFF_REB', 'DEF_REB', 'TOT_REB', 'STL', 'BLK', 'TURNOVERS']].sum().rename({'TURNOVERS': 'TO'}).to_dict()

    
    totalStats['FG%'] = totalStats['FG'] / totalStats['FGA']
    totalStats['3PTS'] = totalStats['FG3'] * 3
    totalStats['FG3%'] = totalStats['FG3'] / totalStats['FG3A']

    totalStats['2PTS'] = totalStats['PTS'] - totalStats['3PTS']
    totalStats['FG2'] = totalStats['FG'] - totalStats['FG3']
    totalStats['FG2A'] = totalStats['FGA'] - totalStats['FG3A']
    totalStats['FG2%'] = totalStats['FG2'] / totalStats['FG2A']

    return totalStats


def main():
    name = input("Enter Player Name: ")
    playerID = getPlayerId(name)

    start_date = parse(input("Enter Start Date (MM/DD/YYYY): "))
    end_date = parse(input("Enter End Date (MM/DD/YYYY): "))

    boxScoreStats = getPlayerBoxScoreStats(playerID, start_date, end_date)

    totalStats = getPlayerTotalStats(boxScoreStats)

    print(totalStats)


if __name__ == "__main__":
    main()

