
from scrapper import Scrapper
from mongo import Mongo_Connector


s = Scrapper("https://www.leagueofgraphs.com/rankings/summoners")

x = s.extract_pages_bulk(55)

#print(x[len(x)-1])