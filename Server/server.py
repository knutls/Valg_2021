from datetime import datetime
import sqlite3
import os
from flask import Flask, request, Response, send_from_directory, redirect
app = Flask(__name__)


DB_PATH = "DB/valg.db"

class VoteData:
    def __init__(self, request) -> None:
        self.request = request
        def extract(key):
            return self.request.form[key]
        
        self.token = extract("token")
        self.vote = extract("vote")
        self.classname = extract("class")
        self.ts = datetime.utcnow()

class Candidate:
    def __init__(self, from_tuple) -> None:
        self.id, self.name, self.classname = from_tuple
        self.votes = []
    
    def append(self, vote) -> None:
        self.votes.append(vote)


class Vote:
    def __init__(self, from_tuple) -> None:
        self.token, self.ts, self.vote = from_tuple
        self.vote = int(self.vote)

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


@app.route("/vote", methods=["POST"])
def saveVote():
    data = VoteData(request)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(f"SELECT COUNT(*) FROM voter WHERE token='{data.token}' AND token_used=0 AND vote_class='{data.classname}'")
    is_token_available = bool(c.fetchone()[0])

    if is_token_available == True:
        c.execute(f"UPDATE voter SET token_used = 1 WHERE token='{data.token}'")
        c.execute(f"INSERT INTO votes VALUES ('{data.token}', '{str(data.ts)}', '{data.vote}')")
        conn.commit()

    return str(is_token_available)

@app.route("/results", methods=["GET"])
def sendResults():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT * FROM candidate")
    candidates = [Candidate(x) for x in c.fetchall()]
    
    c.execute("SELECT * FROM votes")
    votes = [Vote(x) for x in c.fetchall()]
    
    for cand in candidates:
        for vote in votes:
            if vote.vote == cand.id:
                cand.append(vote)

    result = [x.__dict__ for x in candidates]
    for x in result: x["votes"] = len(x["votes"])
    return str(result)




@app.route("/")
def goHome():
    return redirect("http://stem-im.bakka.party:5000/home", code=302)

@app.route("/home", methods=["GET"])
def sendHome():
    src = os.path.join(root_dir(), "../Website/Kode/html/index.html")
    return Response(open(src).read(), mimetype="text/html")

@app.route('/<path:path>')
def sendWebsite(path):
    return send_from_directory('../Website/Kode/', path)

#-----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

