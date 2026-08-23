from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

locations = []


@app.route("/")
def home():
    return render_template("dashboard.html", locations=locations)


@app.route("/send_location", methods=["POST"])
def send_location():
    data = request.json

    locations.append({
        "lat": data.get("lat"),
        "lng": data.get("lng")
    })

    return jsonify({
        "status": "success"
    })


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        locations=locations
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
