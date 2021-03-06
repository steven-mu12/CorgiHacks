import os
from flask import Flask, render_template, redirect, url_for, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Pylance doesn't like this but it works
from image_api import image_api_blueprint, db

app = Flask(__name__)
app.register_blueprint(image_api_blueprint)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/images.db"
db.init_app(app)
if not os.path.exists("./data/images.db"):
    with app.app_context():
        db.create_all()


# TODO: Configure text file to store chat messages (I heard you like plain text Emre)
# 		- Actually, use CSV format so that we store users names as well? and timestamps
# TODO: Configure sockets to send signals for when to update the chat
# TODO: Configure API to send JSON of chat when requested
# TODO: Configure send message API
# TODO: Configure send images API
# TODO: Configure get images API


@app.route("/")
def home_page():
    return render_template("index.html")


# All of our api routes will be prefaced with /api
@app.route("/api/get_chat", methods=["GET"])
def get_chat():
    chat = []
    with open("chat.txt", "r") as f:
        chat = f.readlines()
        # Convert each item to a dict so it can be sent as JSON
        chat = [{"message": x} for x in chat]
        # Get last 50 messages only, don't want it to be super slow
        chat = chat[-50:]
    # Return a Python dict, Flask will auto-convert it to JSON
    return chat


@app.route('/api/send_chat', methods=["POST"])
def send_chat():
    # Check if they are verified with Recaptcha
    # If they are verified, add the message to the file
    # TODO: Implement profanity filter API

    # If request is in wrong format, return bad request status
    if not request.is_json:
        return Response(status=400)

    received_message = request.get_json()["message"]

    with open("chat.txt", "w") as f:
        f.write(received_message + "\n")
        print(received_message)

    # Return HTTP "Created" response
    return Response(status=201)


# Fallback route if they just type something random
@app.route("/*")
def undefined_page():
    return redirect(url_for("home_page"))


if __name__ == "__main__":
    app.run()
