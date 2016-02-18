import http.client
import json
import psycopg2


def addteam(conn):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT hometeamid FROM matchos_matchfootball UNION SELECT DISTINCT awayteamid FROM matchos_matchfootball;") #gather team names

    row = cur.fetchone()
    teams_list = []
    while row is not None:
        row = cur.fetchone()
        teams_list.append(row)
    del teams_list[-1]
    for team in teams_list:
        cur.execute("SELECT * from matchos_matchfootball WHERE hometeamid = (%s) or awayteamid = (%s);", (team, team)) #select team matches
        print("Matches of team: ", team)
        win = 0
        loss = 0
        draw = 0
        for record in cur:
            if record[2] == team[0]:  #id home team
                team_id = record[2]
                team_name = record[1]
                print("home team")
            else:
                team_id = record[4]
                team_name = record[3]
                print("away team")
            if record[5] is not None and record[6] is not None:
                if record[2] == team_id and record[5] > record[6]:
                    print(record)
                    print("TEAM WON")
                    win += 1

                elif record[2] == team_id and record[5] < record[6]:
                    print(record)
                    print("TEAM LOST")
                    loss += 1
                elif record[4] == team_id and record[6] > record[5]:
                    print(record)
                    print("TEAM WON")
                    win += 1
                elif record[4] == team_id and record[6] < record[5]:
                    print(record)
                    print("TEAM LOST")
                    loss += 1
                else:
                    print(record)
                    print("DRAW")
                    draw += 1
        print("WIN/LOSS/DRAW: ", win, loss, draw)
        cur.execute('INSERT INTO matchos_teamfootball (name, wins, loss, draw, teamid) VALUES (%s, %s, %s, %s, %s)', (team_name, win, loss, draw, team_id))
    cur.close()


def mergeleagues(conn):
    cur2 = conn.cursor()
    cur2.execute('TRUNCATE TABLE matchos_matchfootball;')
    for x, y in enumerate(league_names):
        #print("merging")
        cur2.execute('INSERT INTO matchos_matchfootball (hometeamname, hometeamid, awayteamname, awayteamid, goalshometeam, goalsawayteam, season_id, date) '
                'SELECT hometeamname, hometeamid , awayteamname, awayteamid, goalshometeam, goalsawayteam, season_id, date'
                ' from matches'+league_names[x]+';')
    cur2.close()


def getLeagueIds(conn):
    conn.request('GET', '/v1/soccerseasons/', None, headers )
    response = json.loads(conn.getresponse().read().decode())
    leagues_id = []
    for i, league in enumerate(response):
        leagues_id.append(response[i]["id"])
    return leagues_id


def insertLeagueFixtures(cur, leagues_id, league_names, connection):
    for x, league_id in enumerate(leagues_id):
        connection.request('GET', '/v1/soccerseasons/'+str(league_id)+'/fixtures/', None, headers )
        response = json.loads(connection.getresponse().read().decode())
        cur.execute('TRUNCATE TABLE matches'+league_names[x]+';')
        for n, fixture in enumerate(response["fixtures"]):
            htn = response["fixtures"][n]["homeTeamName"]
            atn = response["fixtures"][n]["awayTeamName"]
            htid = response["fixtures"][n]["homeTeamId"]
            atid = response["fixtures"][n]["awayTeamId"]
            ght = response["fixtures"][n]["result"]["goalsHomeTeam"]
            gat = response["fixtures"][n]["result"]["goalsAwayTeam"]
            date = response["fixtures"][n]["date"]
            season_id = response["fixtures"][n]["soccerseasonId"]
            #cur.execute('INSERT INTO matches'+league_names[x]+' (hometeamname, hometeamid, awayteamname, awayteamid, goalshometeam, goalsawayteam, season_id, date) '
                                                             # 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (htn, htid, atn, atid, ght, gat, season_id, date))
            #print("inserting")
            #

            cur.execute('INSERT INTO matches'+league_names[x]+' (hometeamname, hometeamid, awayteamname, awayteamid, goalshometeam, goalsawayteam, season_id, date) '
                                                              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (htn, htid, atn, atid, ght, gat, season_id, date))

    cur.close()


def insertdata(conn, conn_api):
    cur3 = conn.cursor()
    leagues_id = getLeagueIds(connection_api)
    insertLeagueFixtures(cur3, leagues_id, league_names, conn_api)


if __name__ == "__main__":
    connection_api = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': '737ee877051a4f0898a65164c22ec43c', 'X-Response-Control': 'minified'}

    try:
        connection = psycopg2.connect("dbname=mydb user=dbuser password=dbpassword host=localhost")
    except:
        print("Unable to connect")

    league_names = ['1Bundesliga201516', '2Bundesliga201516', 'Ligue1201516', 'Ligue2201516', 'PremierLeague201516',
                    'PrimeraDivision201516', 'SegundaDivision201516', 'SerieA201516', 'PrimeiraLiga201516',
                    '3Bundesliga201516', 'Eredivisie201516', 'ChampionsLeague201516', 'LeagueOne201516']

    #addteam(connection)
    insertdata(connection, connection_api)
    mergeleagues(connection)

    connection.commit()
    connection.close()
