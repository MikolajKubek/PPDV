import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from threading import Thread
from database_manager import data_gatherer, get_measurements, get_one_measurement, get_anomalies
from walk_visualisation import WalkVisualisation
from sensor_series import SensorSeriesVisualisation
from dash.dependencies import Input, Output, State
import atexit

import pandas as pd
import numpy as np
from datetime import timedelta, datetime

df = pd.read_csv('data.csv')

anomaly_cols = [c for c in df.columns if "anomaly" in c]
df[anomaly_cols] = df[anomaly_cols].astype(int)
current_df = df.loc[df['patient_id'] == 1]
sensors_data = [[{
    "name": f"Sensor {i}",
    "measurement_date": current_df['measurement_date'].to_list(),
    "sensor_values": current_df[f'{j}{i}_value'].to_list(),
    "anomalies": current_df[f'{j}{i}_anomaly'].to_list(),
    "trace_name": current_df['trace_name'].to_list()
} for i in range(3)] for j in ("L", "R")]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def create_data_dict():
    return {
        "patient_id": 1,
        "measurement_date": [],
        "birthdate": 1970,
        "disabled": False,
        "firstname": "Lorem",
        "id": 1,
        "lastname": "Ipsum",
        "trace_id": 1,
        "trace_name": "Lorem",
        "L0_value": [],
        "L0_anomaly": [],
        "L1_value": [],
        "L1_anomaly": [],
        "L2_value": [],
        "L2_anomaly": [],
        "R0_value": [],
        "R0_anomaly": [],
        "R1_value": [],
        "R1_anomaly": [],
        "R2_value": [],
        "R2_anomaly": [],
    }


def read_trace(patient_id, query_function=get_measurements):
    data = create_data_dict()
    for i in query_function(patient_id):
        for key, value in i.items():
            if key in data:
                if isinstance(data[key], list):
                    data[key].extend(value)
                else:
                    data[key] = value[0]
    return data


def convert_anomalies_data(anomalies_data):
    results_dicts = []
    for data in anomalies_data:
        results_dict = {}
        for key, value in data.items():
            if key in ["_id", "date"]:
                continue
            if isinstance(data[key], list):
                results_dict[key] = value.pop()
            else:
                results_dict[key] = value

            if "anomaly" in key:
                results_dict[key] = int(results_dict[key])

        results_dicts.append(results_dict)
    return results_dicts


image_path = "foot1.png"
app.layout = html.Div([
    html.H4(f'{" ".join(current_df.loc[0, ["firstname", "lastname", "birthdate"]].astype(str).to_list())}',
            id="patient_data"),
    html.H5("Patient selection:"),
    html.Div([html.Button(f"Patient: {i}", id=f"button_{i}") for i in range(1, 7)]),

    html.H5("Statistical data:"),
    html.Div([
        dcc.Dropdown(options=[
            {'label': 'Current value', 'value': 'current'},
            {'label': 'Mean value', 'value': 'mean'},
            {'label': 'Median', 'value': 'median'},
            {'label': 'Minimum', 'value': 'min'},
            {'label': 'Maximum', 'value': 'max'},
        ], placeholder="Select metric", className="row", id="metric_select"),
        html.H6("Last 5 minutes", id='last_minutes'),
        dcc.Slider(
            id='x_last_minutes',
            min=0,
            max=10,
            step=0.5,
            value=5,
        ),
    ], className="row"),

    html.H5("Left Foot:"),
    html.Div([
        html.Div([
            dcc.Graph(figure=WalkVisualisation(image_path, xs=[2.45, 1.45, 2.1], ys=[6.3, 5.4, 0.75]),
                      id='left_foot_walk_visualisation')
        ], className="three columns"),

        html.Div([
            dcc.Graph(id='g1', figure=SensorSeriesVisualisation(sensors_data[0]))
        ], className="nine columns"),
    ], className="row"),
    html.H5("Right Foot:"),
    html.Div([
        html.Div([
            dcc.Graph(figure=WalkVisualisation(image_path.replace("1", "2"), xs=[1.55, 2.57, 1.9], ys=[6.3, 5.4, 0.75]),
                      id='right_foot_walk_visualisation')
        ], className="three columns"),

        html.Div([
            dcc.Graph(id='g2', figure=SensorSeriesVisualisation(sensors_data[1]))
        ], className="nine columns"),
    ], className="row"),

    html.H5("Saved anomalies:"),
    html.Div(dash_table.DataTable(
        id="anomalies",
        sort_action='native',
        page_size=10,
        columns=[{'name': 'Date', 'id': 'measurement_date', 'type': 'datetime'},
                 {'name': 'Sensor L0', 'id': 'L0_value'},
                 {'name': 'Sensor L1', 'id': 'L1_value'},
                 {'name': 'Sensor L2', 'id': 'L2_value'},
                 {'name': 'Sensor R0', 'id': 'R0_value'},
                 {'name': 'Sensor R1', 'id': 'R1_value'},
                 {'name': 'Sensor R2', 'id': 'R2_value'}],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{L0_anomaly} != 0',
                    'column_id': 'L0_value'
                },
                'backgroundColor': '#FF4136',
            },
            {
                'if': {
                    'filter_query': '{R0_anomaly} != 0',
                    'column_id': 'R0_value'
                },
                'backgroundColor': '#FF4136',
            },
            {
                'if': {
                    'filter_query': '{L1_anomaly} != 0',
                    'column_id': 'L1_value'
                },
                'backgroundColor': '#FF4136',
            },
            {
                'if': {
                    'filter_query': '{R1_anomaly} != 0',
                    'column_id': 'R1_value'
                },
                'backgroundColor': '#FF4136',
            },
            {
                'if': {
                    'filter_query': '{L2_anomaly} != 0',
                    'column_id': 'L2_value'
                },
                'backgroundColor': '#FF4136',
            },
            {
                'if': {
                    'filter_query': '{R2_anomaly} != 0',
                    'column_id': 'R2_value'
                },
                'backgroundColor': '#FF4136',
            },
        ]
    )),

    dcc.Interval(
        id='interval-component',
        interval=500,
        n_intervals=0
    ),
    dcc.Store(id='memory', data=create_data_dict())
])


def last(iterable):
    return iterable[-1]


def median(iterable):
    return np.median(np.array(iterable))


def mean(iterable):
    return np.array(iterable).mean()


def get_first_most_recent_date_idex(dates, time_delta):
    now = datetime.now()
    for index in range(len(dates)):
        if now - dates[index] <= time_delta:
            return index

    return 0


def update_walk_visualisation(measurements_data, figure, foot="L", function=last, time_delta=None):
    first_index = 0
    if time_delta is not None:
        first_index = get_first_most_recent_date_idex(measurements_data["measurement_date"], time_delta)
    sizes, values, anomalies = [], [], []
    for i in range(0, 3):
        size = 50 * function(measurements_data[f"{foot}{i}_value"][first_index:]) / 1024
        if size < 20:
            sizes.append(20)
        else:
            sizes.append(size)
        values.append(function(measurements_data[f"{foot}{i}_value"][first_index:]))
        anomalies.append(function(measurements_data[f"{foot}{i}_anomaly"][first_index:]))
    figure['data'][0]['marker']['size'] = sizes
    figure['data'][0]['text'] = values
    figure['data'][0]['marker_color'] = values
    figure['data'][0]['customdata'] = anomalies

    return figure


def update_sensor_series_figure(measurements_data, figure, foot="L"):
    for i in range(0, 3):
        trace_value_key = f"{foot}{i}_value"
        figure["data"][i]["x"] = measurements_data["measurement_date"]
        figure["data"][i]["y"] = measurements_data[trace_value_key]
        figure["data"][i]["text"] = [f"Value: {value}<br>Anomaly: {anomaly}<br>Trace: { measurements_data['trace_name']}"
                                     for value, anomaly in
                                     zip(measurements_data[trace_value_key], measurements_data[f"{foot}{i}_anomaly"])]

    return figure


@app.callback(Output(component_id='anomalies', component_property='data'),
              Output(component_id='left_foot_walk_visualisation', component_property='figure'),
              Output(component_id='right_foot_walk_visualisation', component_property='figure'),
              Output(component_id='g1', component_property='figure'),
              Output(component_id='g2', component_property='figure'),
              Input(component_id='interval-component', component_property='n_intervals'),
              State(component_id='x_last_minutes', component_property='value'),
              State(component_id='metric_select', component_property='value'),
              State(component_id='left_foot_walk_visualisation', component_property='figure'),
              State(component_id='right_foot_walk_visualisation', component_property='figure'),
              State(component_id='g1', component_property='figure'),
              State(component_id='g2', component_property='figure'),
              State(component_id='anomalies', component_property='data'),
              State(component_id='memory', component_property='data'))
def visualisation_update(n_intervals, slider_value, selected_metric, lf_figure, rf_figure, g1, g2, anomalies_data, data):
    measurements_data = read_trace(data["patient_id"])

    time_delta = timedelta(minutes=slider_value)
    if selected_metric == "median":
        lf_figure = update_walk_visualisation(measurements_data, lf_figure, function=median, time_delta=time_delta)
        rf_figure = update_walk_visualisation(measurements_data, rf_figure, foot="R", function=median, time_delta=time_delta)
    elif selected_metric == "mean":
        lf_figure = update_walk_visualisation(measurements_data, lf_figure, function=mean, time_delta=time_delta)
        rf_figure = update_walk_visualisation(measurements_data, rf_figure, foot="R", function=mean, time_delta=time_delta)
    elif selected_metric == "min":
        lf_figure = update_walk_visualisation(measurements_data, lf_figure, function=min, time_delta=time_delta)
        rf_figure = update_walk_visualisation(measurements_data, rf_figure, foot="R", function=min, time_delta=time_delta)
    elif selected_metric == "max":
        lf_figure = update_walk_visualisation(measurements_data, lf_figure, function=max, time_delta=time_delta)
        rf_figure = update_walk_visualisation(measurements_data, rf_figure, foot="R", function=max, time_delta=time_delta)
    else:
        lf_figure = update_walk_visualisation(measurements_data, lf_figure)
        rf_figure = update_walk_visualisation(measurements_data, rf_figure, foot="R")

    anomalies_data = convert_anomalies_data(get_anomalies(data["patient_id"]))

    return anomalies_data, lf_figure, rf_figure, \
        update_sensor_series_figure(measurements_data, g1), \
        update_sensor_series_figure(measurements_data, g2, foot="R"),


@app.callback(Output(component_id='memory', component_property='data'),
              Output(component_id='patient_data', component_property='children'),
              *[Input(component_id=f"button_{i}", component_property='n_clicks') for i in range(1, 7)],
              State(component_id='memory', component_property='data'))
def on_click(*args):
    data = args[-1]
    if not len(dash.callback_context.triggered):
        return data
    current_patient_id = data["patient_id"]
    prop_id = dash.callback_context.triggered.pop()['prop_id']
    if prop_id != '.':
        patient_id = int(prop_id.split('.')[0][-1])
        if patient_id != current_patient_id:
            data = read_trace(patient_id, get_one_measurement)

    return (data, f'{data["firstname"]}, {data["lastname"]}, {data["birthdate"]}')


@app.callback(Output(component_id='last_minutes', component_property='children'),
              Input(component_id='x_last_minutes', component_property="value"))
def update_slider(slider_value):
    return f"Last {slider_value} minutes"


if __name__ == "__main__":
    # thread = Thread(target=data_gatherer, args=(0.5,))
    # thread.start()
    #
    # @atexit.register
    # def close_thread():
    #     print("stopping database manager thread")
    #     thread.join()

    app.run_server(host='0.0.0.0', port=8050, debug=True)