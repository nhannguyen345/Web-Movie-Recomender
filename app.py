from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import getdata

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///mydatabase.db"  # Sử dụng SQLite làm cơ sở dữ liệu
db = SQLAlchemy(app)


# Định nghĩa model cho bảng User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)


# Định nghĩa model cho bảng Post
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("posts", lazy=True))


# Tạo tất cả các bảng
db.create_all()


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
    data = getdata.read_csv()
    return render_template("homepage.html", data=data)


@app.route("/ratingpage")
def ratingpage():
    # print(getdata.read_csv())
    return render_template("ratingpage.html")


@app.route("/json")
def getjson():
    return getdata.read_csv()


@app.route("/process_data", methods=["POST"])
def process_data():
    if request.method == "POST":
        email = request.form["email"]  # Lấy dữ liệu từ biểu mẫu với key là 'email'
        password = request.form[
            "password"
        ]  # Lấy dữ liệu từ biểu mẫu với key là 'password'
        # Thực hiện xử lý dữ liệu ở đây (ví dụ: lưu vào cơ sở dữ liệu, in ra console, ...)
        print(f"Received data: {email}, {password}")
        return f"Check data"


if __name__ == "__main__":
    app.run(debug=True)
