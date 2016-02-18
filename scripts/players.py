import psycopg2
import http.client
import json
import time


def getLeagueIds(conn):
    conn.request('GET', '/v1/soccerseasons/', None, headers )
    response = json.loads(conn.getresponse().read().decode())
    leagues_id = []
    for i, league in enumerate(response):
        leagues_id.append(response[i]["id"])
    leagues_id.remove(405)
    return leagues_id


def getLeagueTeamsIds(conn, league_id, teams_ids_all_leg):
    conn.request('GET', '/v1/soccerseasons/'+str(league_id)+'/teams', None, headers )
    response = json.loads(conn.getresponse().read().decode())
    teams_ids = []
    for i, team in enumerate(response['teams']):
        if response["teams"][i]["id"] not in teams_ids_all_leg:
            teams_ids.append(response["teams"][i]["id"])
    return teams_ids


def getTeamPlayers(conn_api, team_id, conn):
    conn_api.request('GET', '/v1/teams/'+str(team_id)+'/players', None, headers )
    response = json.loads(conn_api.getresponse().read().decode())
    cur_p = conn.cursor()
    player_ids = []
    for i, player in enumerate(response['players']):
        player_id = response["players"][i]["id"]
        player_name = response["players"][i]["name"]
        player_position = response["players"][i]["position"]
        player_jersey_number = response["players"][i]["jerseyNumber"]
        player_date_of_birth = response["players"][i]["dateOfBirth"]
        player_nationality = response["players"][i]["nationality"]
        player_contract_until = response["players"][i]["contractUntil"]
        player_market_value = response["players"][i]["marketValue"]
        cur_p.execute("INSERT INTO matchos_player (id, name, team_id, position, jersey_number, date_of_birth, nationality, contract_until,"
                      "market_value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (player_id, player_name, team_id, player_position,
                                                                                    player_jersey_number, player_date_of_birth,
                                                                                    player_nationality, player_contract_until,
                                                                                    player_market_value))

    return player_ids

if __name__ == "__main__":
    connection_api = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'b770d6e9d7a0437d85642297ff3afd37', 'X-Response-Control': 'minified'}

    try:
        connection = psycopg2.connect("dbname=mydb user=dbuser password=dbpassword host=localhost")
    except:
        print("Unable to connect")

    cur = connection.cursor()

    #league_ids = getLeagueIds(connection_api)
    league_ids = []
    league_ids.append(397)
    n = 0
    teams_ids_all = []
    for league_id in league_ids:
        teams = getLeagueTeamsIds(connection_api, league_id, teams_ids_all)
        teams_ids_all.append(teams)
        for team in teams:
            players = getTeamPlayers(connection_api, team, connection)
            n += 1
            if n == 39:
                time.sleep(60)
                n = 0
            print(team, players)
    connection.commit()
    connection.close()
