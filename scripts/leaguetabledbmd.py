import psycopg2
import http.client
import json
import time


def getLeagueIds(conn_api):
    conn_api.request('GET', '/v1/soccerseasons/', None, headers )
    response = json.loads(conn_api.getresponse().read().decode())
    leagues_id = []
    for i, league in enumerate(response):
        leagues_id.append(response[i]["id"])
    leagues_id.remove(405)
    return leagues_id


def getLeagueTable(conn_api, league_id, conn):
    conn_api.request('GET', '/v1/soccerseasons/'+str(league_id)+'/leagueTable', None, headers )
    response = json.loads(conn_api.getresponse().read().decode())
    cur = conn.cursor()
    print(response["leagueCaption"])
    for i, standing in enumerate(response["standing"]):
        team_id = response["standing"][i]["teamId"]
        team_name = response["standing"][i]["team"]
        rank = response["standing"][i]["rank"]
        played_games = response["standing"][i]["playedGames"]
        crest_uri = response["standing"][i]["crestURI"]
        points = response["standing"][i]["points"]
        goals = response["standing"][i]["goals"]
        goals_against = response["standing"][i]["goalsAgainst"]
        goal_difference = response["standing"][i]["goalDifference"]
        cur.execute("INSERT INTO matchos_leaguetable (league_id, team_id, team_name, rank, played_games, crest_uri, points, goals, goals_against, goal_difference)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (league_id, team_id, team_name, rank, played_games, crest_uri, points, goals,
                                                                        goals_against, goal_difference))

if __name__ == "__main__":
    connection_api = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'b770d6e9d7a0437d85642297ff3afd37', 'X-Response-Control': 'minified'}

    try:
        connection = psycopg2.connect("dbname=p1407_matchosdb user=p1407_matchosdb password=Matchos1 host=pgsql7.mydevil.net")
    except:
        print("Unable to connect")

    cur = connection.cursor()

    league_ids = getLeagueIds(connection_api)
    for league_id in league_ids:
        getLeagueTable(connection_api, league_id, connection)

    connection.commit()
    connection.close()
