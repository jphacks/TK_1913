from flask import Flask, request
from database import init_db
from database import db

app = Flask(__name__)
app.config.from_object("config.Development")
init_db(app)

@app.route("/")
def index():
    return "Hello"

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    app.run(host=host, port=port)
