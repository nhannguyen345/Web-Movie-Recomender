from flask import Flask, render_template
import getdata

app = Flask(__name__)


@app.route("/")
def loading():
    # print(getdata.read_csv())
    return render_template("loading.html")


@app.route("/login")
def login():
    # print(getdata.read_csv())
    return render_template("login.html")


@app.route("/signup")
def signup():
    # print(getdata.read_csv())
    return render_template("signup.html")


@app.route("/homepage")
def homepage():
    # print(getdata.read_csv())
    return render_template("homepage.html")


@app.route("/ratingpage")
def ratingpage():
    # print(getdata.read_csv())
    return render_template("ratingpage.html")


@app.route("/json")
def ratingpage():
    return getdata.read_csv()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
