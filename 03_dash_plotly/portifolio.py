import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.graph_objects as go

#json de dados de conceitos de linguagens
dados_conceito = {
    'java': {
        'variaveis': 8,
        'condicionais': 10,
        'loops': 5,
        'poo': 5,
        'funcoes': 7
    },
    'python': {
        'variaveis': 10,
        'condicionais': 12,
        'loops': 6,
        'poo': 7,
        'funcoes': 3
    },
    "sql": {
        'variaveis': 2,
        'condicionais': 1,
        'loops': 1,
        'poo': 1,
        'funcoes': 1
    },
    "golang": {
        'variaveis': 3,
        'condicionais': 9,
        'loops': 9,
        'poo': 9,
        'funcoes': 9
    },
    "javascript": {
        'variaveis': 4  ,
        'condicionais': 7,
        'loops': 4,
        'poo': 3,
        'funcoes': 4
    }
}

#dic de cores
cores_map=dict(
    java='red',
    python='blue',
    sql='brown',
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

@app.callback(
    Output('Gráfico Linguagens', 'figure'),
    [Input('drpLinguaguem', 'value')]
)

def scarter_linguagem(linguagens_selecionadas):
    
    if not isinstance(linguagens_selecionadas, list):
        linguagens_selecionadas = [linguagens_selecionadas]

    scarter_trace = []
    for linguagem in linguagens_selecionadas:
        dados_linguagem = dados_conceito[linguagem]
        for conceito, conhecimento in dados_linguagem.items():
            scarter_trace.append(
                go.Scatter(
                    x=[conceito],
                    y=[conhecimento],
                    mode='markers',
                    name=linguagem.title(),
                    marker={'size': 15, 'color': cores_map[linguagem]},
                    showlegend=False
                )
            )
    
    scarter_layout = go.Layout(
        xaxis=dict(title='Conceitos', showgrid=False),
        yaxis=dict(title='Nivel de Conhecimento', showgrid=False),
        title='Conceitos de linguagens de programação'
    )
    
    return {'data': scarter_trace, 'layout': scarter_layout}

if __name__ == '__main__':
    app.run_server(debug=True)
