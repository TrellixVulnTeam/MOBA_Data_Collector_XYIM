from flask import Flask, render_template, url_for, request
from query import Querying_Agent

app = Flask(__name__)

agent = Querying_Agent("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false", "league", "players")


#print(m.elastic.ping())

@app.route('/', methods=['GET'])
def index():
    if "fetch" in request.args:
        print("!")
        query = agent.top_X_Criteria(5, "Elo", "Challenger")
        print(len(query))
        return render_template('index.html', args = request.args, query = query)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
