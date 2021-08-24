from datetime import datetime
from flask import Flask, request
app = Flask(__name__)

class Data:
    def __init__(self, request) -> None:
        self.request = request
        def extract(key):
            return self.request.form[key]
        
        self.code = extract("code")
        self.timestamp = datetime.utcnow()
        self.vote = extract("vote")
        self.classname = extract("class")


@app.route('/vote', methods=['POST'])
def result():
    data = Data(request)


app.run(host="127.0.0.1", port=8080, debug=False)