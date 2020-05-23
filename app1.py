import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys)
# Save reference to the table
measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/prcp"
    )


@app.route("/api/v1.0/prcp")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all measurement stations"""
    # Query all passengers
    results = session.query(measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/station")
def measurement():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement data """
    # Query measurement data
    results = session.query(measurement.station, measurement.date, measurement.prcp, measurement.tobs).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurement
    all_measurement = []
    for station, date, prcp, tobs in results:
        measurement_dict = {}
        measurement_dict["station"] = station
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        measurement_dict["tobs"] = tobs
        all_measurement.append(measurement_dict)

    return jsonify(all_measurement)


if __name__ == '__main__':
    app.run(debug=True)
