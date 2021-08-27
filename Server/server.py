from datetime import datetime
import sqlite3
import os
from flask import Flask, request, Response, send_from_directory, redirect
app = Flask(__name__)


DB_PATH = "DB/data.db"
ROOT = "Valg_2021"


path_to_root = ""
while os.path.basename(os.path.normpath(os.path.dirname(os.path.join(os.getcwd(), path_to_root)))) not in (ROOT, ""):
    path_to_root += "../"

DB_PATH = path_to_root + DB_PATH


class VoteData:
    def __init__(self, request) -> None:
        self.request = request
        def extract(key):
            return self.request.form[key]
        
        self.token = extract("token")
        self.vote = extract("vote")
        self.classname = extract("class")
        self.ts = datetime.utcnow()


# Not used
class Vote:
    def __init__(self, from_tuple) -> None:
        self.token, self.ts, self.vote = from_tuple


class Candidate:
    def __init__(self, from_tuple) -> None:
        self.id, self.name, self.classname = from_tuple
        
        # Get votes from DB
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(f"SELECT * FROM votes WHERE cand_id={self.id}")
        self.votes = len(c.fetchall())
    




def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


@app.route("/vote", methods=["POST"])
def saveVote():
    data = VoteData(request)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(f"SELECT COUNT(*) FROM voter WHERE token='{data.token}' AND token_used=0 AND classname='{data.classname}'")
    is_token_available = bool(c.fetchone()[0])

    if is_token_available == True:
        c.execute(f"UPDATE voter SET token_used = 1 WHERE token='{data.token}'")
        c.execute(f"INSERT INTO votes VALUES ('{data.token}', '{str(data.ts)}', '{data.vote}')")
        conn.commit()

    return redirect("http://stem-im.bakka.party:5000/home", code=302)

@app.route("/results", methods=["GET"])
def sendResults():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT * FROM candidate")
    candidates = [Candidate(x) for x in c.fetchall()]

    result = [x.__dict__ for x in candidates]
    return str(result)




@app.route("/")
def goHome():
    return redirect("http://stem-im.bakka.party:5000/home", code=302)

@app.route("/home", methods=["GET"])
def sendHome():
    src = path_to_root+"Website/Code/HTML/index.html"
    return Response(open(src).read(), mimetype="text/html")

@app.route('/<path:path>')
def sendFile(path):
    return send_from_directory(path_to_root+'Website/', path)

#-----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

