import os
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

# file_path = os.path.join(os.getcwd(), 'dataset_comp.csv')
# df = pd.read_csv(file_path)

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
    html.Div([  
        html.H4('Vendas por Mês e Loja/Cidade'),
        dcc.Graph(id='visual02')        
    ], style={'width': '60%',
              'text-align': 'center'}),
    html.Div(
        dcc.Graph(id='visual03')
    , style={'width': '35%',
              'text-align': 'center'})
],style={
    'display': 'flex',
    'justify-content': 'space-around',
    'margin-top': '40px',
    'height': '150px'})

####################CARREGAR O LAYOUT###########################
app.layout = html.Div([
    layout_titulo, 
    layout_linha01, 
    layout_linha02
])
####################FUNCOES DE APOIO###########################
def filtro_cliente(cliente_selecionado):
    if cliente_selecionado is None:
        return pd.Series(True, index=df.index)
    else:
        return df['Cliente'] == cliente_selecionado
    
def filtro_categoria(categoria_selecionada):
    if categoria_selecionada is None:
        return pd.Series(True, index=df.index)
    elif categoria_selecionada == 'todas_categorias':
        return pd.Series(True, index=df.index)
    return df['Categorias'] == categoria_selecionada

def filtro_mes(meses_selecionados):
    if meses_selecionados is None:
        return pd.Series(True, index=df.index)
    elif 'ano_completo' in meses_selecionados:
        return pd.Series(True, index=df.index)
    else:
        return df['Mes'].isin(meses_selecionados)
####################CALLBACKS##################################
@app.callback(
    Output('output_cliente', 'children'),
    [
       Input('drpCliente', 'value'),
       Input('rdCategoria', 'value') 
    ]
)

def atualizar_texto(cliente_selecionado, categoria_selecionada):
    if cliente_selecionado and categoria_selecionada:
        return f'TOP5 {categoria_selecionada} | Cliente: {cliente_selecionado}'
    
    elif cliente_selecionado:
        return f'TOP5 Produtos | Cliente: {cliente_selecionado}'
    
    elif categoria_selecionada:
        return f'TOP5 {categoria_selecionada}'
    
    return f'TOP5 Categorias'

#Callback para atualizar o tema do Dash App com o Dash Bootstrap Components e o Dash Bootstrap Templates 
@app.callback(
    Output('visual01', 'figure'),
    [
        Input('drpCliente', 'value'),
        Input('chkMes', 'value'),
        Input('rdCategoria', 'value'),
        Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
    ]
)
        
#executa o server e o app se o arquivo for executado diretamente
if __name__ == '__main__':
    app.run_server(debug=True)