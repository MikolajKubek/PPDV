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
