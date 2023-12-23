import time
from flask import Flask, request, render_template
import json
import math
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import urllib.request
import os
import ssl

# from flask_sqlalchemy import SQLAlchemy
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
    # Get data from CSV file
    data = getdata.read_csv()

    # Calculate total number of pages
    total_pages = int(math.ceil(len(data) / 10))  # Adjust page size as needed

    # Get current page number from request parameters or default to 1
    page_number = request.args.get("page", 1)
    try:
        page_number = int(page_number)
    except ValueError:
        page_number = 1

    # Validate page number
    if page_number < 1 or page_number > total_pages:
        page_number = 1

    # Get data chunk for the current page
    data_chunk = getdata.get_data_chunk(data, page_number)

    print(page_number)
    # Pass data chunk and page information to the template
    return render_template(
        "homepage.html",
        data=data_chunk,
        page_number=page_number,
        total_pages=total_pages,
    )


@app.route("/ratingpage")
def ratingpage():
    movie_id = request.args.get("movie_id")
    data = getdata.read_csv()
    result = [row for row in data if movie_id == row["movieId"]]
    # print(getdata.read_csv())
    return render_template("ratingpage.html", result=result)


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if (
        allowed
        and not os.environ.get("PYTHONHTTPSVERIFY", "")
        and getattr(ssl, "_create_unverified_context", None)
    ):
        ssl._create_default_https_context = ssl._create_unverified_context


def find_most_similar_users(ratings, new_user_id, new_movie_ratings):
    # Thêm dữ liệu mới vào cuối DataFrame
    new_user_data = pd.DataFrame(
        {
            "userId": [new_user_id] * len(new_movie_ratings),
            "movieId": new_movie_ratings.index,
            "rating": new_movie_ratings.values,
        }
    )

    ratings = pd.concat([ratings, new_user_data], ignore_index=True)

    # Tạo ma trận user-item
    user_item_matrix = ratings.pivot(
        index="userId", columns="movieId", values="rating"
    ).fillna(0)

    # Tính cosine similarity giữa tất cả các người dùng
    similarities = cosine_similarity(user_item_matrix)

    # Chọn người dùng cụ thể để tìm người dùng tương đồng
    selected_user = user_item_matrix.loc[new_user_id].values.reshape(1, -1)

    # Tính cosine similarity giữa người dùng cụ thể và tất cả người dùng
    user_similarities = cosine_similarity(selected_user, user_item_matrix.values)[0]

    # Loại bỏ tương đồng với chính người dùng mới
    user_similarities[new_user_id - 1] = -1  # -1 hoặc một giá trị nhỏ để loại bỏ

    # Tìm người dùng tương đồng cao nhất
    most_similar_user_id = user_item_matrix.index[np.argmax(user_similarities)]

    return most_similar_user_id


def find_movie_name(movieId, csv_file_path):
    # Đọc dữ liệu từ tệp CSV
    movies = pd.read_csv(csv_file_path)

    # Tìm kiếm thông tin phim theo movieId
    movie_info = movies[movies["movieId"] == movieId]

    # Kiểm tra xem movieId có tồn tại không
    if movie_info.empty:
        return None  # Trả về None nếu không tìm thấy

    # Lấy tên và id của phim
    movie_name = movie_info.iloc[0]["title"]
    movie_id = movie_info.iloc[0]["movieId"]

    # Trả về kết quả
    return {"movieId": int(movie_id), "title": movie_name}


@app.route("/recommendation", methods=["GET", "POST"])
def getrecommendation():
    allowSelfSignedHttps(True)
    if request.method == "POST":
        req_data = request.get_json()
        userid = req_data.get("userid")
        movieids = req_data.get("movieid")
        rating = req_data.get("rating")

        ratings = pd.read_csv("./data/ratings.csv")
        new_user_id = 611
        new_movie_ratings = pd.Series(rating, index=movieids)

        most_similar_user = find_most_similar_users(
            ratings, new_user_id, new_movie_ratings
        )
        print(most_similar_user)
        data = {"id": int(most_similar_user), "k": 5}

        body = str.encode(json.dumps(data))

        url = "http://20.165.1.65:80/api/v1/service/aks-compute/score"
        # Replace this with the primary/secondary key or AMLToken for the endpoint
        api_key = "T3ZJNBONPyVF16JWeUpMu5w87EmpBWJp"
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")

        headers = {
            "Content-Type": "application/json",
            "Authorization": ("Bearer " + api_key),
        }

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            result = json.loads(json.loads(result))
            print(type(result))
            arr_title = []
            for movie in result["MovieId"]:
                arr_title.append(find_movie_name(movie, "./data/movies.csv"))
            print(arr_title)
            return json.dumps(arr_title)
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(error.read().decode("utf8", "ignore"))


@app.route("/json")
def getjson():
    return getdata.read_csv()


@app.route("/search")
def getsearchmovie():
    data = getdata.read_csv()
    searchStr = request.args.get("str", "")
    # Tìm kiếm trong trường "movie" và trả về kết quả
    result = [row for row in data if searchStr.lower() in row["title"].lower()]
    result = result[:10]
    return result


@app.route("/check_login", methods=["POST"])
def process_data():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Kiểm tra thông tin đăng nhập trong cơ sở dữ liệu
        user = 611

        if user:
            # Nếu tìm thấy user, có thể trả về thông tin tương ứng
            return {user: user}
        else:
            # Nếu không tìm thấy user, có thể trả về thông báo lỗi hoặc chuyển hướng đến trang đăng nhập lại
            return "Invalid email or password"


@app.route("/check_signup", methods=["POST"])
def process_data1():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        id = 611
        if id:
            # Nếu tìm thấy user, có thể trả về thông tin tương ứng
            return {id: id}
        else:
            # Nếu không tìm thấy user, có thể trả về thông báo lỗi hoặc chuyển hướng đến trang đăng nhập lại
            # Tạo một đối tượng User mới
            return "Lỗi"


if __name__ == "__main__":
    app.run(debug=True)
