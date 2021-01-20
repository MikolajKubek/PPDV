import plotly.graph_objects as go


class SensorSeriesVisualisation(go.Figure):
    def __init__(self, traces, plot_title=""):
        super().__init__()
        for trace_name in traces:
            self.add_trace(go.Scatter(
                name=trace_name,
                mode='markers+lines',
                x=[],
                y=[],
                text=[],
                hovertemplate="%{text}<extra></extra>",
            ))

        self.update_layout(template="plotly_white", hovermode="x unified", xaxis_title="Date", yaxis_title="Value",
                           title={"text": f"<b>{plot_title}</b>"})

    @staticmethod
    def update_figure_data(measurements_data, figure, foot="L"):
        for i in range(0, 3):
            trace_value_key = f"{foot}{i}_value"
            figure["data"][i]["x"] = measurements_data["measurement_date"]
            figure["data"][i]["y"] = measurements_data[trace_value_key]
            figure["data"][i]["text"] = [
                f"Value: {value}<br>Anomaly: {anomaly}<br>Trace: {measurements_data['trace_name']}"
                for value, anomaly in
                zip(measurements_data[trace_value_key], measurements_data[f"{foot}{i}_anomaly"])]

        return figure
