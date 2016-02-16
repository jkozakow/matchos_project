from lxml import html
import requests
import psycopg2


def convertdate(date):
    date = date[5:-17]
    return date


def scrapPage(page):
    tree = html.fromstring(page.content)
    teams = tree.xpath('//div[@class="item"]/a[div[contains(@title, "finished")]]/div[@class="sub"]/text()')
    score = tree.xpath('//div[@class="item"]/a/div[@class="sub"]/span[not(contains(@class, "ticker_score_cancel")) and not(contains(@class, "ticker_score_live"))]/@class')
    date = tree.xpath('//div[@class="item"]/a/div[@class="sub"]/span[not(contains(@class, "ticker_score_cancel")) and not(contains(@class, "ticker_score_live"))]/../@title')
    teams = [a for a in teams if not a.endswith("vs. ") ]
    teams = [a for a in teams if not a.startswith(":")]
    teams = [a for a in teams if not a.startswith("\n")]
    teams = [item.strip() for item in teams]
    it_t = iter(teams)
    it_s = iter(score)
    it_d = iter(date)
    for x, y in zip(it_t, it_s):
        a_t = next(it_t)
        b_t = next(it_s)
        d_t = next(it_d)
        d_t = convertdate(d_t)
        if y == 'ticker_score_draw' :
            winner = '0'
        elif y == 'ticker_score_win' :
            winner = '1'
        else:
            winner = '2'
        cur.execute('INSERT INTO matches (team1, team2, winner, date) VALUES (%s, %s, %s, %s)', (x, a_t, winner, d_t))


if __name__ == "__main__":
    try:
        conn = psycopg2.connect("dbname=mydb user=dbuser password=dbpassword host=localhost")
    except:
        print("Unable to connect")
    cur = conn.cursor()
    cur.execute('TRUNCATE TABLE matches;')
    for i in range(250):
        url = 'http://www.joindota.com/en/matches&c1=&c2=&c3=&archiv_page=' + str(i)
        page = requests.get(url)
        print("Page: ", i)
        scrapPage(page)

    conn.commit()
    cur.close()
    conn.close()