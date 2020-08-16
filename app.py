import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipiation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end"

    )

@app.route("/api/v1.0/precipiation")
def precipiation():
    session = Session(engine)

    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date

    previous_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    previous_date

# Perform a query to retrieve the data and precipitation scores

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= previous_date).order_by(Measurement.date).all()
    #precipitation_data
    session.close()
    prcp_list = []

    for x in precipitation_data:
        prcp_dict = {}
        prcp_dict[x[0]] = x[1]
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)



@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
# Perform a query to retrieve Station Names
    results = session.query (Station.station, Station.name).all()
    
    session.close()

    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
# Perform a query to retrieve Station Names
    previous_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query (Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= previous_date).all()
    
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/start")
def start():
    start_date = "2017-08-05"
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
        
    session.close()

    all_temps = []
    for tmin, tavg, tmax in results:
        temp_dict = {}
        temp_dict["tmin"] = tmin
        temp_dict["tavg"] = tavg
        temp_dict["tmax"] = tmax
        all_temps.append(temp_dict)

    return jsonify(all_temps)

   
@app.route("/api/v1.0/start_end")
def start_end():
    start_date = "2017-08-05"
    end_date = "2017-08-15"
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).all()
        
    session.close()
    
    all_temps = []
    for tmin, tavg, tmax in results:
        temp_dict = {}
        temp_dict["tmin"] = tmin
        temp_dict["tavg"] = tavg
        temp_dict["tmax"] = tmax
        all_temps.append(temp_dict)

    return jsonify(all_temps)

if __name__ == '__main__':
    app.run(debug=True)
