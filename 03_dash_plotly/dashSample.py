import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# Sample using Dash
import plotly.express as px

# Sample data
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

# Sample using Plotly
import plotly.graph_objects as go

# Sample data
fig = go.Figure(data=[
    go.Bar(name='SF', x=['Apples', 'Oranges', 'Bananas'], y=[4, 1, 2]),
    go.Bar(name='Montreal', x=['Apples', 'Oranges', 'Bananas'], y=[2, 4, 5])
])

# Change the bar mode
fig.update_layout(barmode='group')

fig.show()