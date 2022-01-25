from flask import Flask
import numgle

app = Flask(__name__)

@app.route("/numgle/<param>")
def convertNumgle(param):
    return numgle.numglefy(param)

if __name__ == "__main__":
    app.run(debug=True, port=3001)