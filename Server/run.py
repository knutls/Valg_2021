execute_files = [
    "DB/Init_DB.py",
    "Server/server.py"
]


for path in execute_files:
    exec(open(path).read())