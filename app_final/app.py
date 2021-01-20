import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from datetime import timedelta

from threading import Thread

from app_final.database_manager import data_gatherer, get_measurements, get_one_measurement, get_anomalies
from app_final.components import (left_foot_walk_visualisation, right_foot_walk_visualisation, anomalies_table,
                                  left_foot_sensor_series, right_foot_sensor_series, control_panel)
from app_final.walk_visualisation import WalkVisualisation
from app_final.sensor_series import SensorSeriesVisualisation

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def create_data_dict():
    return {
        "patient_id": 1,
        "measurement_date": [],
        "birthdate": 1,
        "disabled": False,
        "firstname": "",
        "id": 1,
        "lastname": "",
        "trace_id": 1,
        "trace_name": "",
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


def run_data_gathering_thread():
    # thread = Thread(target=data_gatherer, args=(0.5,))
    # thread.start()
    #
    # @atexit.register
    # def close_thread():
    #     print("stopping database manager thread")
    #     thread.join()
    pass


@app.callback(Output(component_id='anomalies', component_property='data'),
              Output(component_id='left_foot_walk_visualisation', component_property='figure'),
              Output(component_id='right_foot_walk_visualisation', component_property='figure'),
              Output(component_id='left_foot_sensor', component_property='figure'),
              Output(component_id='right_foot_sensor', component_property='figure'),
              Input(component_id='interval-component', component_property='n_intervals'),
              State(component_id='x_last_minutes', component_property='value'),
              State(component_id='metric_select', component_property='value'),
              State(component_id='left_foot_walk_visualisation', component_property='figure'),
              State(component_id='right_foot_walk_visualisation', component_property='figure'),
              State(component_id='left_foot_sensor', component_property='figure'),
              State(component_id='right_foot_sensor', component_property='figure'),
              State(component_id='anomalies', component_property='data'),
              State(component_id='memory', component_property='data'))
def visualisation_update(n_intervals, slider_value, selected_metric, lf_figure, rf_figure, left_foot_sensor,
                         right_foot_sensor, anomalies_data, data):
    measurements_data = read_trace(data["patient_id"])

    time_delta = timedelta(minutes=slider_value)
    lf_figure = WalkVisualisation.update_figure_data(measurements_data, lf_figure, function=selected_metric, time_delta=time_delta)
    rf_figure = WalkVisualisation.update_figure_data(measurements_data, rf_figure, foot="R", function=selected_metric, time_delta=time_delta)

    anomalies_data = convert_anomalies_data(get_anomalies(data["patient_id"]))

    return anomalies_data, lf_figure, rf_figure,\
           SensorSeriesVisualisation.update_figure_data(
               measurements_data, left_foot_sensor), \
           SensorSeriesVisualisation.update_figure_data(
               measurements_data, right_foot_sensor, foot="R"),


@app.callback(Output(component_id='memory', component_property='data'),
              Output(component_id='patient_data', component_property='children'),
              Input(component_id="tabs", component_property="active_tab"),
              State(component_id='memory', component_property='data'))
def switch_tab(at, data):
    current_patient_id = data["patient_id"]
    patient_id = int(at[-1])
    if patient_id != current_patient_id:
        data = read_trace(patient_id, get_one_measurement)

    return (data, f'{data["firstname"]}, {data["lastname"]}, {data["birthdate"]}')


@app.callback(Output(component_id='last_minutes', component_property='children'),
              Input(component_id='x_last_minutes', component_property="value"))
def update_slider(slider_value):
    return f"Last {slider_value} minutes"


if __name__ == '__main__':
    patient_ids = [1, 2, 3, 4, 5, 6]

    app.layout = dbc.Card(dbc.CardBody([
        dbc.Tabs([dbc.Tab(label=f"Patient {i}", tab_id=f"patient_{i}") for i in patient_ids],
                 id="tabs", active_tab=f"patient_{patient_ids[0]}"),
        html.Div([
            dbc.Row(html.H4("Pan pacjent", id="patient_data")),
            dbc.Row([
                dbc.Col([left_foot_sensor_series], width=6),
                dbc.Col([right_foot_sensor_series], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Row([dbc.Col([control_panel], width=12)]),
                    dbc.Row([
                        dbc.Col([left_foot_walk_visualisation], width=6),
                        dbc.Col([right_foot_walk_visualisation], width=6)
                    ])], width=6),
                dbc.Col([anomalies_table])
            ]),
        ], style={"padding-left": "1.5%", "padding-top": "1%", "padding-right": "1%", "padding-bottom": "1%"}),

        dcc.Interval(
            id='interval-component',
            interval=500,
            n_intervals=0
        ),
        dcc.Store(id='memory', data=create_data_dict())
    ]), style={"height": "100% !important"})

    run_data_gathering_thread()

    app.run_server(host="0.0.0.0", port=8050, debug=True)
