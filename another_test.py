import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from walk_visualisation import WalkVisualisation
from sensor_series import SensorSeriesVisualisation
from dash.dependencies import Input, Output, State

import pandas as pd

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

image_path = "/home/mikolaj/Desktop/foot1.png"
app.layout = html.Div([
    html.H4(f'{" ".join(current_df.loc[0, ["firstname", "lastname", "birthdate"]].astype(str).to_list())}'),
    html.H5("Patient selection:"),
    html.Div([html.Button(f"Patient: {i}", id=f"button_{i}") for i in range(1, 7)]),
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

    html.H5("Statistical data:"),
    html.Div([
        dcc.Dropdown(options=[
            {'label': 'Mean value', 'value': 'mean'},
            {'label': 'Median', 'value': 'median'},
            {'label': 'Minimum', 'value': 'min'},
            {'label': 'Maximum', 'value': 'max'},
        ], placeholder="Select metric", className="row"),
        html.Div([], className="four columns"),
        html.Div([
            dcc.Graph(figure=WalkVisualisation(image_path, xs=[2.45, 1.45, 2.1], ys=[6.3, 5.4, 0.75]),
                      id='left_foot_metrics')
        ], className="three columns"),
        html.Div([
            dcc.Graph(figure=WalkVisualisation(image_path.replace("1", "2"), xs=[1.55, 2.57, 1.9], ys=[6.3, 5.4, 0.75]),
                      id='right_foot_metrics')
        ], className="three columns"),
    ], className="row"),

    html.H6("Last 5 minutes", id='last_minutes'),
    dcc.Slider(
        id='x_last_minutes',
        min=0,
        max=10,
        step=0.5,
        value=5,
    ),

    html.H5("Saved anomalies:"),
    html.Div(dash_table.DataTable(
        id="anomalies",
        sort_action='native',
        data=current_df[
            (current_df[anomaly_cols[0]] == 1) |
            (current_df[anomaly_cols[1]] == 1) |
            (current_df[anomaly_cols[2]] == 1) |
            (current_df[anomaly_cols[3]] == 1) |
            (current_df[anomaly_cols[4]] == 1) |
            (current_df[anomaly_cols[5]] == 1)
        ].to_dict('records'),
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
        interval=2000,
        n_intervals=0
    ),
    dcc.Store(id='memory', data=1)
])


@app.callback(Output(component_id='left_foot_walk_visualisation', component_property='figure'),
              Input(component_id='interval-component', component_property='n_intervals'),
              State(component_id='left_foot_walk_visualisation', component_property='figure'))
def visualisation_update(n_intervals, figure):
    # values = current_df.loc[0, ["L0_value", "L1_value", "L2_value"]]
    # figure['data'][0]['marker']['size'] = values
    # figure['data'][0]['text'] = values
    # figure['data'][0]['customdata'] = [True, True, True]
    return figure


@app.callback(Output(component_id='memory', component_property='data'),
              *[Input(component_id=f"button_{i}", component_property='n_clicks') for i in range(1, 7)],
              State(component_id='memory', component_property='data'))
def on_click(*args):
    if len(dash.callback_context.triggered):
        return 1
    current_patient_id = args[-1]
    prop_id = dash.callback_context.triggered.pop()['prop_id']
    if prop_id != '.':
        patient_id = int(prop_id.split('.')[0][-1])
        if patient_id != current_patient_id:
            # global current_df
            # current_df = df.loc[df['patient_id'] == patient_id]
            return patient_id

    return 1


app.run_server(debug=True)


