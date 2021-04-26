
from scrapper import Scrapper
from query import Querying_Agent



s = Scrapper("https://www.leagueofgraphs.com/rankings/summoners")
m = Querying_Agent("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false", "league", "players")
#xpath : '//*[@id="drop-region"]/ul'

#data = s.extract_pages_bulk(2, True)
#print(f"Amount collected : {len(data)}")
#s.write_csv("files\\all_regions_50.csv", data)




#extract = [data[i] for i in range(0, 20)]

#print("Inserting")
#m.insert_bulk_csv("files\\all_regions_50.csv")
print("Done")


m.find_one("Name","El Brayayin")

print(m.total())

# m.delete_records()
# print(m.total())
# m.insert_bulk_csv("files\\all_regions_50.csv")
# print(m.total())



# query = m.top_X_Criteria(5, "Server", "BR", "Rank")
# print(query)
# m.list()

#m.delete_records()

#print(data[len(x)-1])