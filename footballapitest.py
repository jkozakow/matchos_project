import http.client
import json
import psycopg2
'''
connection.request('GET', '/v1/soccerseasons/354/fixtures/', None, headers )

response = json.loads(connection.getresponse().read().decode())


print(response["count"])
for i, fixture in enumerate(response["fixtures"]):
    print(response["fixtures"][i])
'''

def getLeagueIds(connection):
    connection.request('GET', '/v1/soccerseasons/', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    leagues_id = []
    for i, league in enumerate(response):
        leagues_id.append(response[i]["id"])
    return leagues_id


def getLeagueFixtures(cur, leagues_id, league_names, connection):
    for x, league_id in enumerate(leagues_id):
        connection.request('GET', '/v1/soccerseasons/'+str(league_id)+'/fixtures/', None, headers )
        response = json.loads(connection.getresponse().read().decode())
        for n, fixture in enumerate(response["fixtures"]):
            htn = response["fixtures"][n]["homeTeamName"]
            atn = response["fixtures"][n]["awayTeamName"]
            htid = response["fixtures"][n]["homeTeamId"]
            atid = response["fixtures"][n]["awayTeamId"]
            ght = response["fixtures"][n]["result"]["goalsHomeTeam"]
            gat = response["fixtures"][n]["result"]["goalsAwayTeam"]
            date = response["fixtures"][n]["date"]
            season_id = response["fixtures"][n]["soccerseasonId"]
            cur.execute('INSERT INTO matches'+league_names[x]+' (hometeamname, hometeamid, awayteamname, awayteamid, goalshometeam, goalsawayteam, season_id, date) '
                                                              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (htn, htid, atn, atid, ght, gat, season_id, date))
            #leagues_fixtures = (response["fixtures"][i])
    return None

if __name__ == "__main__":

    connection_api = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'b770d6e9d7a0437d85642297ff3afd37', 'X-Response-Control': 'minified'}
    try:
        conn = psycopg2.connect("dbname=mydb user=dbuser password=dbpassword host=localhost")
    except:
        print("Unable to connect")
    cur = conn.cursor()
    leagues_id = getLeagueIds(connection_api)
    league_names = ['1Bundesliga201516', '2Bundesliga201516', 'Ligue1201516', 'Ligue2201516', 'PremierLeague201516',
                    'PrimeraDivision201516', 'SegundaDivision201516', 'SerieA201516', 'PrimeiraLiga201516',
                    '3Bundesliga201516', 'Eredivisie201516', 'ChampionsLeague201516', 'LeagueOne201516']

    getLeagueFixtures(cur, leagues_id, league_names, connection_api)

    conn.commit()
    cur.close()
    conn.close()
