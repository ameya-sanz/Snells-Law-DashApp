import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd

# Load the dataset
df = pd.read_csv("refractive_indices.csv")  # Replace with the path to your dataset

# Extract medium names and refractive indices
mediums = df['Medium'].tolist()
indices = df['Index'].tolist()

# Create a dictionary from the dataset
refractive_indices = dict(zip(mediums, indices))

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Snell's Law Visualization"),
    html.P("Explore how light refracts through different mediums. Created by Ameya Sanjanita."),
    dcc.Dropdown(
        id='medium1',
        options=[{'label': key, 'value': value} for key, value in refractive_indices.items()],
        value=1,
        clearable=False,
        style={'width': '50%'}
    ),
    dcc.Dropdown(
        id='medium2',
        options=[{'label': key, 'value': value} for key, value in refractive_indices.items()],
        value=1.33,
        clearable=False,
        style={'width': '50%'}
    ),
    dcc.Slider(
        id='angle-slider',
        min=0,
        max=89,
        value=30,
        marks={i: f'{i}°' for i in range(0, 90, 10)},
        step=1
    ),
    dcc.Graph(id='snells-law-graph')
])

@app.callback(
    Output('snells-law-graph', 'figure'),
    [Input('medium1', 'value'),
     Input('medium2', 'value'),
     Input('angle-slider', 'value')]
)
def update_graph(n1, n2, angle_of_incidence):
    theta1 = np.radians(angle_of_incidence)
    sin_theta2 = (n1 / n2) * np.sin(theta1)
    fig = go.Figure()

    if abs(sin_theta2) > 1:
        # Total internal reflection
        fig.add_trace(go.Scatter(
            x=[0, -np.sin(theta1)], 
            y=[0, -np.cos(theta1)], 
            mode='lines+markers',
            marker=dict(symbol='circle', size=8, color='blue'),
            name='Incident Ray'
        ))

        # Reflected ray, same angle as incidence but in the opposite direction
        fig.add_trace(go.Scatter(
            x=[0, -np.sin(theta1)], 
            y=[0, np.cos(theta1)], 
            mode='lines+markers',
            marker=dict(symbol='circle', size=8, color='red'),
            name='Reflected Ray'
        ))

        fig.update_layout(
            title=f'Total Internal Reflection: n1={n1} to n2={n2} at {angle_of_incidence}° incidence',
            xaxis_title='Y',
            yaxis_title='X',
            xaxis=dict(
                title='X',
                zeroline=False,
                scaleanchor="y",
                scaleratio=1,
                showgrid=False,
                showline=True,
                showticklabels=True
            ),
            yaxis=dict(
                title='Y',
                zeroline=False,
                showgrid=False,
                showline=True,
                showticklabels=True
            ),
            shapes=[
                dict(
                    type='line',
                    x0=0,
                    y0=-1,
                    x1=0,
                    y1=1,
                    line=dict(
                        color="Black",
                        width=2,
                        dash="dashdot",
                    ),
                )
            ],
            annotations=[
                dict(
                    x=-np.sin(theta1) / 2,
                    y=-np.cos(theta1) / 2,
                    xref="x",
                    yref="y",
                    text=f'{angle_of_incidence}°',
                    showarrow=True,
                    arrowhead=2,
                    ax=20,
                    ay=-30
                ),
                dict(
                    x=np.sin(theta1) / 2,
                    y=(-np.cos(theta1)) / 2,
                    xref="x",
                    yref="y",
                    text=f'{angle_of_incidence}°',
                    showarrow=True,
                    arrowhead=2,
                    ax=-20,
                    ay=30
                )
            ]
        )
    else:
        theta2 = np.arcsin(sin_theta2)
        # Incident ray
        fig.add_trace(go.Scatter(
            x=[0, -np.sin(theta1)], 
            y=[0, -np.cos(theta1)], 
            mode='lines+markers',
            marker=dict(symbol='circle', size=8, color='blue'),
            name='Incident Ray'
        ))

        # Refracted ray
        fig.add_trace(go.Scatter(
            x=[0, np.sin(theta2)], 
            y=[0, np.cos(theta2)], 
            mode='lines+markers',
            marker=dict(symbol='circle', size=8, color='red'),
            name='Refracted Ray'
        ))

        fig.update_layout(
            title=f'Refraction: n1={n1} to n2={n2} at {angle_of_incidence}° incidence',
            xaxis_title='Y',
            yaxis_title='X',
            xaxis=dict(
                title='X',
                zeroline=False,
                scaleanchor="y",
                scaleratio=1,
                showgrid=False,
                showline=True,
                showticklabels=True
            ),
            yaxis=dict(
                title='Y',
                zeroline=False,
                showgrid=False,
                showline=True,
                showticklabels=True
            ),
            shapes=[
                dict(
                    type='line',
                    x0=0,
                    y0=-1,
                    x1=0,
                    y1=1,
                    line=dict(
                        color="Black",
                        width=2,
                        dash="dashdot",
                    ),
                )
            ],
            annotations=[
                dict(
                    x=-np.sin(theta1) / 2,
                    y=-np.cos(theta1) / 2,
                    xref="x",
                    yref="y",
                    text=f'{angle_of_incidence}°',
                    showarrow=True,
                    arrowhead=2,
                    ax=20,
                    ay=-30
                ),
                dict(
                    x=np.sin(theta2) / 2,
                    y=np.cos(theta2) / 2,
                    xref="x",
                    yref="y",
                    text=f'{np.degrees(theta2):.1f}°',
                    showarrow=True,
                    arrowhead=2,
                    ax=-20,
                    ay=30
                )
            ]
        )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
