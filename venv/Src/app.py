from flask import Flask, render_template, url_for, request
from query import Querying_Agent
from graph import Graph

app = Flask(__name__)

agent = Querying_Agent("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false", "league", "players")
servers = ["BR", "EUNE", "EUW", "JP", "KR", "LAN", "LAS", "OCE",  "RU",  "TR",]
sorters = ["Rank", "LP", "Win", "Win%"]
graph = Graph()

#print(m.elastic.ping())
#<input type="text" name="content" id="content">
#<label for="amount">Amount :</label>
#<input type="number" id="amount" name="amount" min="1">

@app.route('/', methods=['GET'])
def index():
    if "top_x" in request.args:
        print(request.args)
        query = {}
        if "sorters" in request.args:
            query = agent.top_X_Criteria(20, "Server", request.args.get("servers"), request.args.get("sorters"))
        else:
            query = agent.top_X_Criteria(20, "Server", request.args.get("servers"), None)
        return render_template('index.html', args = request.args, servers=servers, sorters=sorters, querytype = "players", query=query)

    elif "match_player" in request.args:
        print(request.args)
        query_first = agent.search(20, request.args.get("search_bar"))
        query = [r['_source'] for r in query_first['hits']['hits']]
        return render_template('index.html', args = request.args, servers=servers, sorters=sorters, querytype = "players_elastic", query=query, queryname=request.args.get("search_bar"))

    elif "chall_by_server_world_pie" in request.args:
        res = agent.challengers_per_server()
        print(res)
        graph.chall_by_server_world_pie(res)
        return render_template('index.html', args = request.args, servers=servers, sorters=sorters, querytype = "graph", path='chall_by_server_world_pie.png')

    elif "chall_by_server_world_hist" in request.args:
        res = agent.challengers_per_server()
        print(res)
        graph.chall_by_server_world_hist(res)
        return render_template('index.html', args = request.args, servers=servers, sorters=sorters, querytype = "graph", path='chall_by_server_world_hist.png')

    elif "number_server_pie" in request.args:
        res = agent.elo_per_server(request.args.get("servers"))
        print(res)
        graph.number_server_pie(res)
        return render_template('index.html', args = request.args, servers=servers, sorters=sorters, querytype = "graph", path='number_server_pie.png')

    elif "number_server_hist" in request.args:
        res = agent.elo_per_server(request.args.get("servers"))
        print(res)
        graph.number_server_hist(res)
        return render_template('index.html', args = request.args, servers=servers, sorters=sorters, querytype = "graph", path='number_server_hist.png')

    return render_template('index.html', servers = servers, sorters=sorters, querytype = "startpoint")


if __name__ == '__main__':
    app.run()
