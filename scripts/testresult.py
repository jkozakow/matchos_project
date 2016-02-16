import http.client
import json
import psycopg2


if __name__ == "__main__":

    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'b770d6e9d7a0437d85642297ff3afd37', 'X-Response-Control': 'minified'}
    connection.request('GET', '/v1/soccerseasons/394/fixtures', None, headers )
    response = json.loads(connection.getresponse().read().decode())


    for n, fixture in enumerate(response["fixtures"]):
        ght = response["fixtures"][n]["result"]["goalsHomeTeam"]
        gha = response["fixtures"][n]["result"]["goalsAwayTeam"]
        print(ght, gha)


