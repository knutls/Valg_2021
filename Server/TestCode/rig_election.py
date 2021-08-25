import sqlite3
from datetime import datetime
from random import randrange

DB_PATH = "DB/valg.db"

exec(open("DB/Init_DB.py").read())

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()



c.execute("SELECT * FROM voter")
for voter in c.fetchall():
    c.execute(f"UPDATE voter SET token_used = 1 WHERE token='{voter[0]}'")
    vote = randrange(1,7)
    c.execute(f"INSERT INTO votes VALUES ('{voter[0]}', '{str(datetime.utcnow())}', '{vote}')")
    conn.commit()
