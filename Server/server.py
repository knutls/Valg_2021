from flask import Flask, request
app = Flask(__name__)
@app.route('/vote', methods=['POST'])
def result():
    print(request.form['fname']) # should display 'bar'
    return 'Received !' # response to your request.


app.run(host="127.0.0.1", port=8080, debug=False)