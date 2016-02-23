import psycopg2


def addteam(conn):
    cur = conn.cursor()
    cur.execute('TRUNCATE TABLE matchos_team;')
    cur.execute("SELECT DISTINCT team1 FROM matchos_match UNION SELECT DISTINCT team2 FROM matchos_match;") #gather team names

    row = cur.fetchone()
    teams_list = []
    while row is not None:
        row = cur.fetchone()
        teams_list.append(row)
    del teams_list[-1]
    for team in teams_list:
        cur.execute("SELECT * from matchos_match WHERE team1 like (%s) or team2 like (%s);", (team, team)) #select team matches
        print("Matches of team: ", team)
        win = 0
        loss = 0
        draw = 0
        for record in cur:
            team1 = str(record[1]).strip("(),'")
            team1 = team1.replace("'", "")
            team2 = str(record[2]).strip("(),'")
            team2 = team2.replace("'", "")
            team_str = str(team).strip('"(),')
            team_str = team_str.replace("'", "") #stripping brackets, comma and apostrophe from team tuple to allow comparing later
            if team1 == team_str and record[3] == 1:
                print(record)
                print("TEAM WON")
                win += 1

            elif team1 == team_str and record[3] == 2:
                print(record)
                print("TEAM LOST")
                loss += 1
            elif team2 == team_str and record[3] == 2:
                print(record)
                print("TEAM WON")
                win += 1
            elif team2 == team_str and record[3] == 1:
                print(record)
                print("TEAM LOST")
                loss += 1
            else:
                print(record)
                print("DRAW")
                draw += 1
        print("WIN/LOSS/DRAW: ", win, loss, draw)
        cur.execute('INSERT INTO matchos_team (name, wins, loss, draw) VALUES (%s, %s, %s, %s)', (team, win, loss, draw))
    cur.close()

if __name__ == "__main__":
    try:
        conn = psycopg2.connect("dbname=mydb user=dbuser password=dbpassword host=localhost")
    except:
        print("Unable to connect")


    addteam(conn)

    conn.commit()

    conn.close()