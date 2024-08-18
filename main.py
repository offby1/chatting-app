import random
from string import ascii_uppercase

from flask import Flask, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "weufhweuf"
socketio = SocketIO(app)


@app.route("/<length>", methods=["POST", "GET"])
def generate_unique_code(length):
    length = int(length)

    code = ""
    for _ in range(length):
        code += random.choice(ascii_uppercase)

    return code


def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="ENTER NAME", code=code, name=name)

        if join and not code:
            return render_template("home.html", error="ENTER CODE", code=code, name=name)

        room = code
        if not create:
            room = generate_unique_code(4)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")


@app.route("/room")
def room():
    return render_template("room.html")


if __name__ == "__main__":
    socketio.run(app, debug=True)
