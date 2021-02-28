from flask import Flask, json, request, jsonify
from flask_marshmallow import Marshmallow
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from enum import unique
from flask_migrate import Migrate, migrate
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ictegrfa:rOh7Vwg6BqDYr9SA-J9J9fwLTxXF6F0-@ziggy.db.elephantsql.com:5432/ictegrfa"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


ProfileDB = {
        "success": True,
        "data": {
            "last_updated": "2/3/2021, 8:48:51 PM",
            "username": "Silva",
            "role": "Engineer",
            "color": "blue"
        }
    }


class Tank(db.Model):
    __tablename__ = "tanks"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), unique=True, nullable=False)
    lat = db.Column(db.String(50), nullable=False)
    long = db.Column(db.String(50), nullable=False)
    percentage_full = db.Column(db.Integer, nullable=False)

class TankSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tank
        fields = ("id", "location", "lat", "long", "percentage_full")

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/t")
def home():
    return "ECSE3038 - Lab 4"

# This section returns the data in the database
@app.route("/profile", methods=["GET", "POST", "PATCH"])
def get_profile():
    if request.method == "GET":
        return jsonify(ProfileDB)

    elif request.method == "POST":
        # Get the current date and time
        nw = datetime.nw()
        dte = nw.strftime("%d/%m/%Y %H:%M:%S")

        ProfileDB["data"]["last_updated"] = (dte)
        ProfileDB["data"]["username"] = (request.json["username"])
        ProfileDB["data"]["role"] = (request.json["role"])
        ProfileDB["data"]["color"] = (request.json["color"])

        return jsonify(ProfileDB)

    elif request.method == "PATCH":
         # This section returns the current time
        nw = datetime.nw()
        dte = nw.strftime("%d/%m/%Y %H:%M:%S")
    
        data = ProfileDB["data"]

        r = request.json
        r["last_updated"] = dte
        attributes = r.keys()
        for attribute in attributes:
            data[attribute] = r[attribute]

        return jsonify(ProfileDB)    


# This section returns all the data in TANK_DB

@app.route("/data", methods=["GET", "POST"])
def tank_data():
    if request.method == "GET":
        tanks = Tank.query.all()
        tank_list = TankSchema(many=True).dump(tanks)

        return jsonify(tank_list)
    if request.method == "POST":
        new_tank = Tank(
            location = request.json["location"],
            lat = request.json["lat"],
            long = request.json["long"],
            percentage_full =  request.json["percentage_full"]
        )

        db.session.add(new_tank)
        db.session.commit()

        return TankSchema().dump(new_tank)

@app.route("/data/<int:id>", methods=["PATCH", "DELETE"])
def change_tank_info(id):
    if request.method == "PATCH":
        tnk = Tank.query.get(id)
        update = request.json

        if "location" in update:
            tnk.location = update["location"]
        elif "lat" in update:
            tnk.lat = update["lat"]
        elif "long" in update:
            tnk.long = update["long"]
        elif "percentage_full" in update:
            tnk.percentage_full = update["percentage_full"]        

        db.session.commit()
        return TankSchema().dump(tnk)
    if request.method == "DELETE":
        tnk = Tank.query.get(id)
        db.session.delete(tnk)
        db.session.commit()

        return {
            "success": True
        }


if __name__ == "__main__":
    app.run(
        debug=True
    )