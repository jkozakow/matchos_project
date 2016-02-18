import psycopg2


if __name__ == "__main__":
    try:
        conn = psycopg2.connect("dbname=mydb user=dbuser password=dbpassword host=localhost")
    except:
        print("Unable to connect")

    cur = conn.cursor()

    cur.execute("SELECT * FROM matchos_matchfootball LIMIT 5;")
    for record in cur:
        print(record)

    conn.close()
