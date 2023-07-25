from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("main.html")


@app.route("/man/")
def man():
    return render_template("man.html")


@app.route("/woman/")
def woman():
    return render_template("woman.html")


@app.route("/kids/")
def kids():
    return render_template("kids.html")
