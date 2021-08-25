from datetime import datetime
import sqlite3
from flask import Flask, request
app = Flask(__name__)


DB_PATH = "DB/valg.db"



class Data:
    def __init__(self, request) -> None:
        self.request = request
        def extract(key):
            return self.request.form[key]
        
        self.token = extract("token")
        self.vote = extract("vote")
        self.classname = extract("class")
        self.ts = datetime.utcnow()


@app.route("/vote", methods=["POST"])
def result():
    data = Data(request)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(f"SELECT COUNT(*) FROM voter WHERE token='{data.token}' AND token_used=0 AND vote_class='{data.classname}'")
    is_token_available = bool(c.fetchone()[0])

    if is_token_available == True:
        c.execute(f"UPDATE voter SET token_used = 1 WHERE token='{data.token}'")
        c.execute(f"INSERT INTO votes VALUE ({data.token}, {data.ts}, {data.vote})")
        conn.commit()

    return str(is_token_available)


#-----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)


