from flask import Flask, render_template, request, jsonify
import uuid
import os
import json
from datetime import datetime

app = Flask(__name__)

LINK_FILE = "links.json"
LOCATION_FILE = "locations.json"


def load_json(file):
    try:
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return {}


def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


links = load_json(LINK_FILE)
locations = load_json(LOCATION_FILE)

if not isinstance(links, dict):
    links = {}

if not isinstance(locations, list):
    locations = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create_link")
def create_link():

    link_id = str(uuid.uuid4())[:8]

    links[link_id] = {
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    save_json(LINK_FILE, links)

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

    data = request.get_json()

    if not data:
        return jsonify({"error": "no data"}), 400

    locations.append({
        "id": link_id,
        "lat": data.get("lat"),
        "lng": data.get("lng"),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_json(LOCATION_FILE, locations)

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
