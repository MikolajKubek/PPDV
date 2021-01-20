import plotly.graph_objects as go
import base64
from datetime import datetime
import numpy as np


class WalkVisualisation(go.Figure):
    sensor_data = {}

    def __init__(self, image_path, background_color='rgb(255, 255, 255)',
                 image_rect=(0, 8, 4, 8), xs=[], ys=[]):
        super().__init__()
        self.add_layout_image(dict(
            source=self._base64_encode_image(image_path),
            xref="x",
            yref="y",
            x=image_rect[0],
            y=image_rect[1],
            sizex=image_rect[2],
            sizey=image_rect[3],
            sizing="stretch",
            opacity=0.6,
            layer="below",
        ))

        self.update_layout(dict(
            plot_bgcolor=background_color,
            xaxis=dict(visible=False, range=[0, image_rect[2]], fixedrange=True),
            yaxis=dict(visible=False, range=[0, image_rect[3]], fixedrange=True)
        ))

        self.sensor_data = dict(
            xs=xs,
            ys=ys,
            values=[30, 40, 35],
            anomalies=[True, False, False]
        )

        self.add_trace(go.Scatter(
            mode='markers+text',
            customdata=self.sensor_data['anomalies'],
            hovertemplate="Value: %{text}<br>Anomaly: %{customdata}<extra></extra>",
            marker=dict(colorscale='sunset')
        ))
        self.update_sensor_positions(self.sensor_data['xs'], self.sensor_data['ys'])
        self.update_sensor_values(self.sensor_data['values'])

    def update_sensor_positions(self, xs, ys):
        self.sensor_data['xs'] = xs
        self.sensor_data['ys'] = ys
        self.update_traces(x=self.sensor_data['xs'], y=self.sensor_data['ys'])

    def update_sensor_values(self, values):
        self.sensor_data['values'] = values
        self.update_traces(marker_size=self.sensor_data['values'], text=self.sensor_data['values'], marker_color=values)

    @staticmethod
    def _base64_encode_image(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return "data:image/png;base64," + encoded_string

    @staticmethod
    def last(iterable):
        return iterable[-1]

    @staticmethod
    def median(iterable):
        return np.median(np.array(iterable))

    @staticmethod
    def mean(iterable):
        return np.array(iterable).mean()

    @staticmethod
    def get_first_most_recent_date_index(dates, time_delta):
        now = datetime.now()
        for index in range(len(dates)):
            if now - dates[index] <= time_delta:
                return index

        return 0

    @staticmethod
    def update_figure_data(measurements_data, figure, foot="L", function=last, time_delta=None):
        if function == "mean":
            function = WalkVisualisation.mean
        elif function == "median":
            function = WalkVisualisation.median
        elif function == "min":
            function = min
        elif function == "max":
            function = max
        else:
            function = WalkVisualisation.last

        first_index = 0
        if time_delta is not None:
            first_index = WalkVisualisation.get_first_most_recent_date_index(measurements_data["measurement_date"], time_delta)
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

