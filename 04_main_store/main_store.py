import plotly.graph_objects as graph_obj
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash.dependencies import Input, Output
from dash import dcc, html, Input, Output

#Configurando o tema do Dash App com o Dash Bootstrap Components e o Dash Bootstrap Templates
dark_theme = 'darkly'
vapor_theme = 'vapor'
url_dark_theme = dbc.themes.DARKLY
url_vapor_theme = dbc.themes.VAPOR

#importando dados do csv dataset_comp.csv
df = pd.read_csv('dataset_comp.csv')

#Transformando a coluna dt_Venda em datetime
df['dt_Venda']=pd.to_datetime(df['dt_Venda'])

#Criando a coluna mes_Venda
df['Mes']=df['dt_Venda'].dt.strftime('%b').str.upper()

#Criar lista de Clientes
lista_cliente = []
for cliente in df['Cliente'].unique():
    lista_cliente.append({'label':cliente, 'value':cliente})

#Adicionando a opção de selecionar todos os clientes
lista_cliente.append({'label':'Todos os clientes', 'value':'todos_clientes'})

#Criar lista de Meses
meses_br = dict(
    JAN='Janeiro', 
    FEB='Fevereiro', 
    MAR='Março', 
    APR='Abril', 
    MAY='Maio', 
    JUN='Junho', 
    JUL='Julho', 
    AUG='Agosto', 
    SEP='Setembro', 
    OCT='Outubro', 
    NOV='Novembro', 
    DEC='Dezembro')

lista_mes = []
for mes in df['Mes'].unique():
   mes_pt = meses_br.get(mes, mes)
   
   lista_mes.append({'label':mes_pt, 'value':mes})
   
lista_mes.append({'label':'Ano Completo', 'value':'ano_completo'})

lista_categoria=[]
for categoria in df['Categorias'].unique():
    lista_categoria.append({'label':categoria, 'value':categoria})

lista_categoria.append({'label':'Todas as categorias', 'value':'todas_categorias'})

#start do servidor
app = dash.Dash(__name__) 
server = app.server

####################LAYOUT#####################################

layout_titulo = html.Div([
    html.Div(
        dcc.Dropdown(
            id='drpCliente',
            options=lista_cliente,
            style={
                'background-color': 'transparent',
                'color': 'black',
                'border': 'none',
            }
        ),style={'width': '25%'}
    ),
    html.Div(
        html.Legend(
            'Sebrae MA - Vendas por Cliente',
            style={
                'font-size': '150%',
                'text-align': 'center',
            }
        ),style={'width': '50%'}
    ),
    html.Div(
        ThemeSwitchAIO(
            aio_id='theme',
            themes=[url_dark_theme, url_vapor_theme]    
        ),style={'width': '25%'}
    )
 ], style={
    'display': 'flex',
    'justify-content': 'space-around',
    'align-items': 'center',
    'background-color': 'transparent',
    'border': 'none',
    'padding': '10px',
    'margin': '10px',
    'width': '100%',
    'font-family': 'Fira Code',
    'margin-top': '20px'
 })
layout_linha01 = html.Div([  
    html.Div([
        html.H4(id='output_cliente'),
        dcc.Graph(id='visual01')
        ],style={'width': '65%',
                 'text-align': 'center',}) ,
    html.Div([
        dbc.Checklist(
            id="chkMes",
            options=lista_mes,
            inline=True,
        ),
        dbc.RadioItems
        (
            id='rdCategoria',
            options=lista_categoria,
            inline=True
        ),
    ], style={'width': '30%',
              'display': 'flex',
              'flex-direction': 'column',
              'justify-content': 'space-evenly', })
], style={
    'display': 'flex',
    'justify-content': 'space-around',
    'margin-top': '40px',
    'height': '300px'})
layout_linha02 = html.Div([  
    html.Div([  ]) ,
    html.Div([  ])
])
####################FUNCOES DE APOIO###########################

####################CALLBACKS##################################


#executa o server e o app se o arquivo for executado diretamente
if __name__ == '__main__':
    app.run_server(debug=True)