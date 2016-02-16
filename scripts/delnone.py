import http.client
import json
import psycopg2



if __name__ == "__main__":

    try:
        conn = psycopg2.connect("dbname=mydb user=dbuser password=dbpassword host=localhost")
    except:
        print("Unable to connect")
    cur = conn.cursor()

    league_names = ['1Bundesliga201516', '2Bundesliga201516', 'Ligue1201516', 'Ligue2201516', 'PremierLeague201516',
                    'PrimeraDivision201516', 'SegundaDivision201516', 'SerieA201516', 'PrimeiraLiga201516',
                    '3Bundesliga201516', 'Eredivisie201516', 'ChampionsLeague201516', 'LeagueOne201516']
    semicolon = ':'
    for x, y in enumerate(league_names):
        cur.execute('SELECT goalshometeam, case when goalshometeam is null then (%s) end from matches'+league_names[x]+';', (semicolon))
        cur.execute('SELECT goalshometeam, case when goalsawayteam is null then (%s) end from matches'+league_names[x]+';', (semicolon))

    conn.commit()
    cur.close()
    conn.close()


