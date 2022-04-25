from flask import Flask ,render_template

application = Flask(__name__)

@application.route("/")
def home():
    return render_template("home.html")

@application.route("/create_post")
def create_post():
    return render_template("create_post.html")

# run the app
if __name__ == "__main__":
    application.run()