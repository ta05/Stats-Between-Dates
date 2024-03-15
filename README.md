# NBA Stats Between Dates

stats.nba.com and basketballreference.com are good sources for NBA statistical data, but one of the features that is missing from both is a tool that allows for retrieving player stats between two dates. This can be frustrating if you would like to see how Jayson Tatum has been shooting from the 3 in his last 15 games or how many blocks per game Chet Holgrem has recorded since Christmas.

This script queries stats.nba.com to retrieve game data between the inputed dates and summates the player's box score numbers.

## Response

The script returns a dictionary that includes the number of games played within the dates, the standard box score info and a 2-pt attempts, makes and percentages.

## Known Issues

The script is slow (2 minutes for a season worth of data). The api doesn't have complete documentation on including dates in api calls and my attempts have not worked, so I've had to filter after the call. The script only pulls in Regular Season data, but can be modified to query for Post or Pre Season games as well.

## Credits

[nba_api](https://github.com/swar/nba_api/tree/master) to retrieve NBA player and game statistics from NBA.com.