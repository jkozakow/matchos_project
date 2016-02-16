import http.client
import json
import psycopg2


def getLeagueIds(connection):
    connection.request('GET', '/v1/soccerseasons/', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    leagues_id = []
    for i, league in enumerate(response):
        leagues_id.append(response[i]["caption"])
    return leagues_id


def getLeagueNames(leagues_id, league_names):
    for x, y in enumerate(leagues_id):
        print('INSERT INTO matches'+league_names[x]+' (team1, team2, winner, date)')
    return None


if __name__ == "__main__":
    try:
        conn = psycopg2.connect("dbname=mydb user=dbuser password=dbpassword host=localhost")
    except:
        print("Unable to connect")
    cur = conn.cursor()
    connection_api = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'b770d6e9d7a0437d85642297ff3afd37', 'X-Response-Control': 'minified'}
    league_names = ['1Bundesliga201516', '2Bundesliga201516', 'Ligue1201516', 'Ligue2201516', 'PremierLeague201516',
                    'PrimeraDivision201516', 'SegundaDivision201516', 'SerieA201516', 'PrimeiraLiga201516',
                    '3Bundesliga201516', 'Eredivisie201516', 'ChampionsLeague201516', 'LeagueOne201516']
    league_id = getLeagueIds(connection_api)
    for i, x in enumerate(league_names):
        print(league_names[i])
    getLeagueNames(league_id, league_names)
    for x, y in enumerate(league_id):
        cur.execute('create table matches'+league_names[x]+' (id serial PRIMARY KEY, HomeTeamName varchar, HomeTeamId integer, AwayTeamName varchar, AwayTeamId integer, GoalsHomeTeam integer, GoalsAwayTeam integer, date varchar );')
    conn.commit()
    cur.close()
    conn.close()

