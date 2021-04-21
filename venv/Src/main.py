
from scrapper import Scrapper
from mongo import Mongo_Client



s = Scrapper("https://www.leagueofgraphs.com/rankings/summoners")
m = Mongo_Client("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false", "league", "players")
#xpath : '//*[@id="drop-region"]/ul'

data = s.extract_pages_bulk(2, True)
print(f"Amount collected : {len(data)}")
#s.write_csv("all_regions_50.csv", data)




#extract = [data[i] for i in range(0, 20)]

#print("Inserting")
#m.insert_bulk(extract)
#print("Done")


#m.find_one("Name","El Brayayin")

#m.delete_records()

#print(data[len(x)-1])