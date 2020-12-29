import dash
import dash_table
import requests
from requests import ConnectionError
from datetime import datetime
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

columns = ["patient_id", "measurement_date", "birthdate", "disabled", "firstname", "id",
           "lastname", "trace_id", "trace_name",  "L0_value", "L0_anomaly", "L1_value",
           "L1_anomaly", "L2_value", "L2_anomaly", "R0_value", "R0_anomaly", "R1_value",
           "R1_anomaly", "R2_value", "R2_anomaly"]

df = pd.DataFrame(columns=columns)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)


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


if __name__ == '__main__':
    ready = False
    while not ready:
        try:
            json_data = requests.get("http://tesla.iem.pw.edu.pl:9080/v2/monitor/1").json()
            ready = True
            df = df.append(pd.DataFrame(measurement_data_to_vector_dict(json_data, 1, datetime.now())))
            app.layout = dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in df.columns],
                            data=df.to_dict('records'),
                        )
        except ConnectionError:
            print("waiting for vpn to connect...")
            continue
    app.run_server(host='0.0.0.0', port=8050, debug=True)
