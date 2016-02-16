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

if __name__ == "__main__":
    try:
        conn = psycopg2.connect("dbname=mydb user=dbuser password=dbpassword host=localhost")
    except:
        print("Unable to connect")

    addteam(conn)

    conn.commit()

    conn.close()