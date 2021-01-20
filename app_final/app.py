import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from threading import Thread

from app_final.components import (left_foot_walk_visualisation, right_foot_walk_visualisation, anomalies_table,
                                  left_foot_sensor_series, right_foot_sensor_series, control_panel)

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def run_data_gathering_thread():
    # thread = Thread(target=data_gatherer, args=(0.5,))
    # thread.start()
    #
    # @atexit.register
    # def close_thread():
    #     print("stopping database manager thread")
    #     thread.join()
    pass


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
            dbc.Row(html.H4("Pan pacjent")),
            dbc.Row([
                dbc.Col([
                    dbc.Row([dbc.Col([control_panel], width=12)]),
                    dbc.Row([
                        dbc.Col([left_foot_walk_visualisation], width=6),
                        dbc.Col([right_foot_walk_visualisation], width=6)
                    ])], width=6),
                dbc.Col([anomalies_table])
            ]),
            dbc.Row([
                dbc.Col([left_foot_sensor_series], width=6),
                dbc.Col([right_foot_sensor_series], width=6)
            ])
        ], style={"padding-left": "1.5%", "padding-top": "1%", "padding-right": "1%", "padding-bottom": "1%"}),
    ]), style={"height": "100% !important"})

    run_data_gathering_thread()

    app.run_server(host="0.0.0.0", port=8050, debug=True)
