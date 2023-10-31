from flask import Flask, render_template
import getdata

app = Flask(__name__)


@app.route("/")
def hello_world():
    print(getdata.read_csv())
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
