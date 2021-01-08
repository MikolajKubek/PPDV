import plotly.graph_objects as go


class SensorSeriesVisualisation(go.Figure):
    def __init__(self, sensors_data):
        super().__init__()
        for data in sensors_data:
            self.add_trace(go.Scatter(
                name=data["name"],
                mode='markers+lines',
                x=data["measurement_date"],
                y=data["sensor_values"],
                text=[f"Value: {sensor_value}<br>Anomaly: {anomaly}<br>Trace: {trace_name}"
                      for sensor_value, anomaly, trace_name
                      in zip(data["sensor_values"], data["anomalies"], data["trace_name"])],
                hovertemplate="%{text}<extra></extra>",
            ))

        self.update_layout(template="plotly_white", hovermode="x unified", xaxis_title="Date", yaxis_title="Value")
