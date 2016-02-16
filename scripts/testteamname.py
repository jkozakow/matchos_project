import http.client
import json
import psycopg2



if __name__ == "__main__":

    try:
        conn = psycopg2.connect("dbname=mydb user=dbuser password=dbpassword host=localhost")
    except:
        print("Unable to connect")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT hometeamname FROM matchos_matchfootball UNION SELECT DISTINCT awayteamname FROM matchos_matchfootball;") #gather team names

    row = cur.fetchone()
    teams_list = []
    while row is not None:
        #print(row)
        row = cur.fetchone()
        teams_list.append(row)
    del teams_list[-1]
    for team in teams_list:
        cur.execute("SELECT * from matchos_matchfootball WHERE hometeamname like (%s) or awayteamname like (%s);", (team, team)) #select team matches
        print("Matches of team: ", team)
        win = 0
        loss = 0
        draw = 0
        for record in cur:
            team_str = str(team).strip('(),')
            team_str = team_str.replace("'", "") #stripping brackets, comma and apostrophe from team tuple to allow comparing later
            if record[5] is not None or record[6] is not None:
                if record[1] == team_str and record[5] > record[6]:
                    win += 1
                elif record[1] == team_str and record[5] < record[6]:
                    loss += 1
                elif record[3] == team_str and record[6] > record[5]:
                    win += 1
                elif record[3] == team_str and record[6] < record[5]:
                    loss += 1
                else:
                    draw += 1
        cur.execute('INSERT INTO matchos_teamfootball (name, wins, loss, draw) VALUES (%s, %s, %s, %s)', (team, win, loss, draw))

    conn.commit()
    cur.close()
    conn.close()
