from flask import Flask, redirect, render_template, request, url_for
import database

application = Flask(__name__)


@application.route("/")
def home():
    posts = database.get_posts()
    return render_template("home.html", posts=posts)


@application.route("/create_post", methods=["GET", "POST"])
def create_post():

    if request.method == "GET":
        return render_template("create_post.html")

    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        database.put_post(title, text)
        return redirect(url_for("home"))


# run the app
if __name__ == "__main__":

    # init table
    database.init_table()

    application.run()
