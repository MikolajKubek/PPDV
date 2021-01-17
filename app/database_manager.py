import requests
from datetime import datetime
from pymongo import MongoClient
import os
from time import sleep
from threading import Thread

client = MongoClient(os.environ['MONGO_URL'])
data_source_url = os.environ['DATA_SOURCE_URL']


db = client.test_database
measurements = db.measurements
anomalies = db.anomalies
measurements.create_index("date", expireAfterSeconds=60)
anomalies.create_index("date", expireAfterSeconds=5 * 60)

columns = ["patient_id", "measurement_date", "birthdate", "disabled", "firstname", "id",
           "lastname", "trace_id", "trace_name",  "L0_value", "L0_anomaly", "L1_value",
           "L1_anomaly", "L2_value", "L2_anomaly", "R0_value", "R0_anomaly", "R1_value",
           "R1_anomaly", "R2_value", "R2_anomaly"]

anomaly_columns = ["L0_anomaly", "L1_anomaly", "L2_anomaly", "R0_anomaly", "R1_anomaly", "R2_anomaly"]


def get_anomalies():
    return anomalies.find()


def get_one_measurement(patient_id):
    return [measurements.find_one({"patient_id": patient_id})]


def get_measurements(patient_id=None):
    if patient_id is None:
        return measurements.find()
    else:
        return measurements.find({"patient_id": patient_id})


def fetch_server_data():
    for patient_id in range(1, 7):
        json_data = requests.get(f"{data_source_url}{patient_id}").json()
        measurement_data = measurement_data_to_vector_dict(json_data, patient_id, datetime.now())
        measurement_data['date'] = datetime.utcnow()
        if any([measurement_data[col] for col in anomaly_columns]):
            anomalies.insert_one(measurement_data)
        measurements.insert_one(measurement_data)


def measurement_data_to_vector_dict(json_data, patient_id, measurement_date):
    return {
        "patient_id": [patient_id],
        "measurement_date": [measurement_date],
        "birthdate": [json_data["birthdate"]],
        "disabled": [json_data["disabled"]],
        "firstname": [json_data["firstname"]],
        "id": [json_data["id"]],
        "lastname": [json_data["lastname"]],
        "trace_id": [json_data["trace"]["id"]],
        "trace_name": [json_data["trace"]["name"]],
        "L0_value": [json_data["trace"]["sensors"][0]["value"]],
        "L0_anomaly": [json_data["trace"]["sensors"][0]["anomaly"]],
        "L1_value": [json_data["trace"]["sensors"][1]["value"]],
        "L1_anomaly": [json_data["trace"]["sensors"][1]["anomaly"]],
        "L2_value": [json_data["trace"]["sensors"][2]["value"]],
        "L2_anomaly": [json_data["trace"]["sensors"][2]["anomaly"]],
        "R0_value": [json_data["trace"]["sensors"][3]["value"]],
        "R0_anomaly": [json_data["trace"]["sensors"][3]["anomaly"]],
        "R1_value": [json_data["trace"]["sensors"][4]["value"]],
        "R1_anomaly": [json_data["trace"]["sensors"][4]["anomaly"]],
        "R2_value": [json_data["trace"]["sensors"][5]["value"]],
        "R2_anomaly": [json_data["trace"]["sensors"][5]["anomaly"]],
    }


def data_gatherer(interval):
    while True:
        fetch_server_data()
        sleep(interval)


if __name__ == "__main__":
    thread = Thread(target=data_gatherer(), args=(1,))
    thread.start()
    thread.join()
