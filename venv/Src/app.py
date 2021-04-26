from flask import Flask, render_template, url_for, request
from query import Querying_Agent

app = Flask(__name__)

agent = Querying_Agent("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false", "league", "players")
servers = ["BR", "EUNE", "EUW", "JP", "KR", "LAN", "LAS", "OCE",  "RU",  "TR",]
sorters = ["Rank", "LP", "Win", "Win%"]

#print(m.elastic.ping())
#<input type="text" name="content" id="content">
#<label for="amount">Amount :</label>
#<input type="number" id="amount" name="amount" min="1">

@app.route('/', methods=['GET'])
def index():
    if "top_x" in request.args:
        query = agent.top_X_Criteria(20, "Server", request.args.get("servers"), request.args.get("sorters"))
        print(request.args)
        print(len(query))
        return render_template('index.html', args = request.args, servers=servers, sorters=sorters, query=query)

    return render_template('index.html', servers = servers)


if __name__ == '__main__':
    app.run()
