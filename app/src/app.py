from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
import os
import time

app = Flask(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://weather_user:weather_pass@localhost:5432/weather"
)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    temperature = db.Column(db.Float)
    windspeed = db.Column(db.Float)
    winddirection = db.Column(db.Float)
    weathercode = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# Ждём, пока PostgreSQL станет доступен
with app.app_context():
    for _ in range(10):
        try:
            db.create_all()
            break
        except Exception:
            time.sleep(2)


@app.route("/log", methods=["POST"])
def log_weather():
    city = "CustomCity"
    lat, lon = 50.0, 50.0

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    res = requests.get(url).json()
    current = res.get("current_weather", {})

    record = Weather(
        city=city,
        temperature=current.get("temperature"),
        windspeed=current.get("windspeed"),
        winddirection=current.get("winddirection"),
        weathercode=current.get("weathercode"),
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({"status": "logged"})


@app.route("/history", methods=["GET"])
def get_history():
    entries = Weather.query.order_by(Weather.timestamp.desc()).all()
    return jsonify(
        [
            {
                "city": e.city,
                "temperature": e.temperature,
                "windspeed": e.windspeed,
                "winddirection": e.winddirection,
                "weathercode": e.weathercode,
                "time": e.timestamp.isoformat(),
            }
            for e in entries
        ]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
