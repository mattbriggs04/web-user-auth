from flask import Flask, render_template
from utils.pyuser import DBManager

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")