import dash_core_components as dcc
import dash_html_components as html
import dash_table
from app_final.walk_visualisation import WalkVisualisation
from app_final.sensor_series import SensorSeriesVisualisation


def snake_case(string):
    return string.strip().lower().replace(" ", "_")


_foot_images = {"left": "foot1.png", "right": "foot2.png"}
_sensor_traces = ["sensor_1", "sensor_2", "sensor_3"]
_statistical_data = ["Current value", "Mean", "Median", "Min", "Max"]
_left_foot_walk_visualisation_fig = WalkVisualisation(_foot_images["left"], xs=[2.45, 1.45, 2.1], ys=[6.3, 5.4, 0.75])
_right_foot_walk_visualisation_fig = WalkVisualisation(_foot_images["right"], xs=[1.55, 2.57, 1.9], ys=[6.3, 5.4, 0.75])
_left_foot_sensor_series_fig = SensorSeriesVisualisation(_sensor_traces, "Left foot:")
_right_foot_sensor_series_fig = SensorSeriesVisualisation(_sensor_traces, "Right foot:")

left_foot_walk_visualisation = dcc.Graph(figure=_left_foot_walk_visualisation_fig, id="left_foot_walk_visualisation")
right_foot_walk_visualisation = dcc.Graph(figure=_right_foot_walk_visualisation_fig, id="right_foot_walk_visualisation")
left_foot_sensor_series = dcc.Graph(figure=_left_foot_sensor_series_fig, id="left_foot_sensor")
right_foot_sensor_series = dcc.Graph(figure=_right_foot_sensor_series_fig, id="right_foot_sensor")

control_panel = html.Div([
    html.H5("Statistical data:"),
    dcc.Dropdown(options=[{'label': label, "value": snake_case(label)} for label in _statistical_data],
                 placeholder=_statistical_data[0], id="metric_select"),
    html.H6("Last 5 minutes", id="last_minutes"),
    dcc.Slider(id="x_last_minutes", min=0.5, max=10, step=0.5, value=5)
])

anomalies_table = html.Div([
    html.H5("Saved anomalies:"),
    dash_table.DataTable(
        id="anomalies",
        sort_action="native",
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
    )])
