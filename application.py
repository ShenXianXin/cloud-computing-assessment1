from flask import Flask, render_template
import database

application = Flask(__name__)


@application.route("/")
def home():
    posts = database.get_posts()
    return render_template("home.html", posts=posts)


@application.route("/create_post")
def create_post():
    return render_template("create_post.html")


# run the app
if __name__ == "__main__":

    # init table
    database.init_table()

    application.run()
