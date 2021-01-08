import plotly.graph_objects as go
import base64


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
            marker_color='rgba(0, 124, 0, .8)',
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
