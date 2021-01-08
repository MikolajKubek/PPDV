import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64

df = px.data.iris()

app = dash.Dash(__name__)

image_filename = "/home/mikolaj/Desktop/foot.png" # replace with your own image
with open(image_filename, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
# add the prefix that plotly will want when using the string as source
encoded_image = "data:image/png;base64," + encoded_string

app.layout = html.Div([
    dcc.Graph(id="scatter-plot", config={'displayModeBar': False}),
    html.P("Petal Width:"),
    dcc.RangeSlider(
        id='range-slider',
        min=0, max=2.5, step=0.1,
        marks={0: '0', 2.5: '2.5'},
    ),
])

walk_animation_template = dict(
    plot_bgcolor='rgb(255, 255, 255)',
    width=400,
    height=800,
    xaxis=dict(visible=False, range=[0, 4], fixedrange=True),
    yaxis=dict(visible=False, range=[0, 8], fixedrange=True)
)

walk_animation_xaxis = dict(
    visible=False
)


@app.callback(
    Output("scatter-plot", "figure"),
    [Input("range-slider", "value")])
def update_bar_chart(slider_range):
    fig = go.Figure()

    t = np.linspace(0, 2)

    data = dict(
        xs=[1, 2],
        ys=[2, 4],
        values=[30, 40]
    )

    fig.add_trace(go.Scatter(
        x=data['xs'],
        y=data['ys'],
        mode='markers+text',
        marker_color='rgba(152, 0, 0, .8)',
        text=data['values'],
        marker_size=data['values'],
        hovertemplate=" %{text}<extra></extra>"
    ))

    fig.add_layout_image(
        dict(
            source=encoded_image,
            # source="https://images.plot.ly/language-icons/api-home/python-logo.png",
            xref="x",
            yref="y",
            x=0,
            y=8,
            sizex=4,
            sizey=8,
            sizing="contain",
            opacity=0.6,
            layer="below",
        ))
    fig.update_layout(walk_animation_template)
    return fig


app.run_server(debug=True)