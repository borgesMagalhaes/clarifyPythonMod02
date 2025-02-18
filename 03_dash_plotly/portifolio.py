import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go

#json de dados de conceitos de linguagens
dados_conceito = {
    'java': {
        'variaveis': 8,
        'condicionais': 10,
        'loops': 4,
        'poo': 5,
        'funcoes': 4
    },
    'python': {
        'variaveis': 10,
        'condicionais': 12,
        'loops': 6,
        'poo': 7,
        'funcoes': 4
    },
    "sql": {
        'variaveis': 2,
        'condicionais': 1,
        'loops': 1,
        'poo': 0,
        'funcoes': 1
    },
    "golang": {
        'variaveis': 9,
        'condicionais': 9,
        'loops': 9,
        'poo': 9,
        'funcoes': 9
    },
    "javascript": {
        'variaveis': 8,
        'condicionais': 10,
        'loops': 4,
        'poo': 3,
        'funcoes': 4
    }
}
#dic de cores
cores_map=dict(
    java='red',
    python='blue',
    sql='yellow',
    golang='green',
    javascript='black'
)

#Função para criar o gráfico   
app=dash.Dash(__name__)
app.layout=html.Div([
    html.H1('Conceitos de linguagens de programação',
            style={'textAlign':'center'}),
    html.Div(    
        dcc.Dropdown(
        id='drpLinguaguem',
        options=[
            {'label': 'Java', 'value': 'java'},
            {'label': 'Python', 'value': 'python'},
            {'label': 'SQL', 'value': 'sql'},
            {'label': 'Golang', 'value': 'golang'},
            {'label': 'Javascript', 'value': 'javascript'}
        ],
        value='java',
        multi=True,
        style={'width':'50%', 'margin':'0 auto'}),
    ),
    dcc.Graph(id='Gráfico Linguagens')
    
],
style={'width':'80%', 'margin':'0 auto'}

)