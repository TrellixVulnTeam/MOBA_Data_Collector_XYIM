
from scrapper import Scrapper


s = Scrapper("https://www.leagueofgraphs.com/rankings/summoners")

for i in range(0, 100001):
    s.next_page()
    print(s.url)