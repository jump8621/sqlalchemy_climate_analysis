import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#database setup
# connection_string = "sqlite://titanic.sqlite"
# engine = create_engine(connection_string)
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
# , echo=False
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

print(Base.classes.keys())
Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app
app = Flask(__name__)


# routes
@app.route("/")
def index():
    return"""
        Available routes:<br/>
        /api/v1.0/precipitaion<br/>
        /api/v1.0/station<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0<start></br>
        /api/v1.0<start>/<end></br>
    """

@app.route("/api/v1.0/precipitation")
def precipitaion():
    session = Session(engine)   
#   * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
#   * Return the JSON representation of your dictionary.
    target_date = dt.date(2017, 8, 23)
    delta= dt.timedelta(days=365)
    query_date = target_date - delta


    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > query_date).order_by(Measurement.date.desc()).all()
    session.close()

    
    precipitation_list = []
    for i in range(len(results)):
        precipitation_dict = {}
        precipitation_dict[results[i][0]] = results[i][1]
        precipitation_list.append(precipitation_dict)
        
    return jsonify(precipitation_list)
        # precipitation_dict = {}
        # precipitation_dict["date"] = Measurement.date
        # precipitation_dict["prcp"] = Measurement.prcp
        # precipitation_list.append(precipitation_dict)

    

@app.route("/api/v1.0/station")
def station():
    session = Session(engine)
#     # * Return a JSON list of stations from the dataset.
    stations_query = session.query(Station.name).all()

    session.close()

    station_list = list(np.ravel(stations_query))

    return jsonify(station_list)
    # stations_query = session.query(Station, Station.id, Station.name, Station.station).all()
#     results = session.query(Passenger.name).all()

#     session.close()

#     names = list(np.ravel(results))
    

    # stations_list = []
    # for i in stations_query:

        # 'name' : Station.name
        # stations_list['id'] : Station.id
        # stations_list['station'] : Station.station
        # stations_list.append(stations_list)

    # return jsonify(station_list)
# session = Session(engine)

#     results = session.query(Passenger.name).all()

#     session.close()

#     names = list(np.ravel(results))

#     return jsonify(names)

# @app.route("/api.v1.0/passengers")
# def passengers():
#     session = Session(engine)

#     results = session.query(Passenger).all

#     session.close()

#     passengers = []
#     for item in results:
#         passenger = { 
#             'name': item.name,
#             'age' : item.age,
#             'sex' : item.sex
#         }
#         passengers.append(passenger)

#     return jsonify(results)



@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
#   * Query the dates and temperature observations of the most active station for the last year of data.
#   * Return a JSON list of temperature observations (TOBS) for the previous year.
    target_date = dt.date(2017, 8, 18)
    delta= dt.timedelta(days=365)
    query_date = target_date - delta

    active_stations = session.query(Measurement.station, func.count(Measurement.tobs))\
        .group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).all()
    
    active_station = session.query(Measurement.tobs, Measurement.date, Measurement.station).filter(Measurement.date>=query_date)\
        .filter(Measurement.station == active_stations[0][0]).all()

    session.close()
    tobs_dict = {}
    # tobs_list = []
    for i in range(len(active_station)):
        
        tobs_dict[active_station[i][1]] = active_station[i][0]
        # precipitation_list.append(precipitation_dict)
        
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start)


    return 
# @app.route("/api/v1.0/passengers/<id>")
# def passenger(id):
#     session = Session(engine)

#     results = session.query(Passenger).filter(Passenger.id == id).first()

#     session.close()
    
#     passenger = { 
#         'name': item.name,
#         'age' : item.age,
#         'sex' : item.sex
#         }
        
#     return jsonify(passenger)

#     @app.route("/api/v1.0/justice-league/superhero/<superhero>")
# def justice_league_by_superhero__name(superhero):
#     """Fetch the Justice League character whose superhero matches
#        the path variable supplied by the user, or a 404 if not."""

#     canonicalized = superhero.replace(" ", "").lower()
#     for character in justice_league_members:
#         search_term = character["superhero"].replace(" ", "").lower()

#         if search_term == canonicalized:
#             return jsonify(character)

#     return jsonify({"error": "Character not found."}), 404
# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

if __name__=="__main__":
    app.run(debug=True)