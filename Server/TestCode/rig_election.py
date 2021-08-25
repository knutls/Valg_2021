import sqlite3
from datetime import datetime
from random import randrange

DB_PATH = "DB/valg.db"
WINNER = 2

exec(open("DB/Init_DB.py").read())

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()


c.execute("SELECT * FROM voter")
for voter in c.fetchall():
    c.execute(f"UPDATE voter SET token_used = 1 WHERE token='{voter[0]}'")
    vote = randrange(1,7)
    
    c.execute("SELECT * FROM votes")
    votes = [x[2] for x in c.fetchall()]
    
    c.execute("SELECT COUNT(*) FROM candidate")
    for i in range(c.fetchone()[0]):
        if i+1 == WINNER:
            continue
        elif votes.count(str(i+1)) >= votes.count(str(WINNER)):
            vote = WINNER
            break

    c.execute(f"INSERT INTO votes VALUES ('{voter[0]}', '{str(datetime.utcnow())}', {vote})")
    conn.commit()

c.execute("SELECT * FROM votes")
print("\n".join([str(x) for x in c.fetchall()]))
