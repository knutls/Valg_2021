import sqlite3
import json
import os

filepath = 'DB/data.db'

if os.path.exists(filepath):
    os.remove(filepath)
    print("Deleting previous version of db: %s" % filepath)
else:
    print("Creating db file: %s" % filepath)

conn = sqlite3.connect(filepath)

c = conn.cursor()

c.execute("""CREATE TABLE voter (
            token text,
            token_used int,
            is_admin int,
            vote_class text
            )""")

c.execute("""CREATE TABLE votes (
            token text,
            vote_time text,
            candidate_id int
            )""")

c.execute("""CREATE TABLE candidate (
            cand_id int,
            cand_name text,
            vote_class text
            )""")



# c.execute("INSERT INTO voter VALUES ('eMGeB', 0, 0) ")


#leser inn input data
with open('DB/Verification_Codes/IT.json', 'r') as f: 
    data_it = json.load(f)

with open('DB/Verification_Codes/ST.json', 'r') as f:
    data_st = json.load(f)

with open('DB/Verification_Codes/MP.json', 'r') as f:
    data_mp = json.load(f)



#inserter i databasen
for token in data_mp:
    sql = 'insert into voter'
    sql = "INSERT INTO voter VALUES ('%s', 0, 0, 'mp') " % token
    c.execute(sql)


for token in data_st:
    sql = 'insert into voter'
    sql = "INSERT INTO voter VALUES ('%s', 0, 0, 'st') " % token
    c.execute(sql)


for token in data_it:
    sql = 'insert into voter'
    sql = "INSERT INTO voter VALUES ('%s', 0, 0, 'it') " % token
    c.execute(sql)

#commiting the changes to the db
conn.commit()


records = [(1, "Jaime", "it"),
            (2, "Andreas", "it"),
            (3, "Lars", "mp"),
            (4, "Sondre", "mp"),
            (5, "Simen", "st"),
            (6, "Dino", "st")]


c.executemany('INSERT INTO candidate VALUES(?,?,?);',records)

conn.commit()

#henter data fra database sånn at jeg kan lese

sql = 'SELECT * FROM voter'
c.execute(sql)
#print (c.fetchall())
all_voters = c.fetchall()
for item in all_voters:
    print(item)
    

sql = 'SELECT * FROM candidate'
c.execute(sql)
#print (c.fetchall())
all_candidate = c.fetchall()
for item in all_candidate:
    print (item)


sql = 'SELECT * FROM votes'
c.execute(sql)
#print (c.fetchall())
all_votes = c.fetchall()
print(all_votes)
for item in all_votes:
    print(item)

conn.close()

