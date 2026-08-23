from flask import Flask, render_template, request, jsonify
import uuid
import os
import json
from datetime import datetime

app = Flask(__name__)

LINK_FILE = "links.json"
LOCATION_FILE = "locations.json"


def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


links = {}
locations = load_data(LOCATION_FILE)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create_link")
def create_link():

    link_id = str(uuid.uuid4())[:8]

    links[link_id] = {
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify({
        "link": "/share/" + link_id
    })


@app.route("/share/<link_id>")
def share(link_id):

    if link_id not in links:
        return "Invalid Link"

    return render_template(
        "share.html",
        link_id=link_id
    )


@app.route("/send_location/<link_id>", methods=["POST"])
def send_location(link_id):

    data = request.json

    locations.append({
        "id": link_id,
        "lat": data.get("lat"),
        "lng": data.get("lng"),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_data(LOCATION_FILE, locations)

    return jsonify({
        "status": "received"
    })


@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        locations=locations
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
