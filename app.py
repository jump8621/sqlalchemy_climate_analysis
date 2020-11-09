import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#database setup

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
        /api/v1.0/<start></br>
        /api/v1.0/<start>/<end></br>
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
         

@app.route("/api/v1.0/station")
def station():
    session = Session(engine)
#     # * Return a JSON list of stations from the dataset.
    stations_query = session.query(Station.name).all()

    session.close()

    station_list = list(np.ravel(stations_query))

    return jsonify(station_list)
    


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
def start(start):
    session = Session(engine)
    try:
        start = dt.datetime.strptime(start, "%Y-%m-%d")
        
    except:
        return jsonify({"error": "Improper date format. Needs to be YYYY-MM-DD."}), 404
        
    
    # results = session.query(TMIN, TAVG, TMAX).filter(Measurement.date>=start)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .group_by(Measurement.date)\
        .filter(Measurement.date>=start).all()
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
    # print(results)
    session.close()

    temp_list = []

    for i in results:
        start = {}
        start[i[0]] = {
            'TMAX' : i[2],
            'TMIN' : i[1],
            'TAVG' : i[3]
        }
        temp_list.append(start)


    return jsonify (temp_list)
    

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):

    session = Session(engine)
    try:
        start = dt.datetime.strptime(start, "%Y-%m-%d")
        end = dt.datetime.strptime(end, '%Y-%m-%d')
    except:
        return jsonify({"error": "Improper date format. Needs to be YYYY-MM-DD."}), 404
        
    
#     # results = session.query(TMIN, TAVG, TMAX).filter(Measurement.date>=start)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    session.close()

    
    sp_range_temp = []
    for i in (results):
        inclusive_temp_range = {}
        inclusive_temp_range = {
            'Temp_MIN' : i[0],
            'Temp_MAX' : i[1],
            'Temp_AVG' : i[2]
        }

        sp_range_temp.append(inclusive_temp_range) 


    return jsonify (sp_range_temp)
# could just return inclusive_temp_range it comes out the same on jupyter notebook
if __name__=="__main__":
    app.run(debug=True)