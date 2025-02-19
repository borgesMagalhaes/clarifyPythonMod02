from calendar import c
import os
import re
from flask.cli import F
from matplotlib.pyplot import margins, plot, show
import plotly.graph_objects as graph_obj
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash.dependencies import Input, Output
from dash import dcc, html, Input, Output

#fixando o diretório de trabalho para evitar erro de [Errno 2] No such file or directory: 'dataset_comp.csv'
os.chdir(os.path.dirname(__file__))  # Change to script's directory

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

def visual01(cliente, mes, categoria, toggle):
    template = dark_theme if toggle else vapor_theme

    nomeCliente = filtro_cliente(cliente)
    nomeCategoria = filtro_categoria(categoria)
    nomeMes = filtro_mes(mes)
    
    cliente_mes_categoria = nomeCliente & nomeMes & nomeCategoria
    dfFiltrado = df.loc[cliente_mes_categoria]
    
    dfGrupo = dfFiltrado.groupby(['Produto', 'Categorias'])['Total Vendas'].sum().reset_index()
    dfTop5 = dfGrupo.sort_values(by='Total Vendas', ascending=False).head(5)

#Criando o gráfico de barras
    fig = px.bar(
        dfTop5,
        x='Produto',
        y='Total Vendas',
        color='Total Vendas',
        text='Total Vendas',
        color_continuous_scale='blues',
        height=280,
        template=template
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        margin=dict(t=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, range=[dfTop5['Total Vendas'].min()*0,dfTop5['Total Vendas'].max()*1.2]),
        xaxis_title = None,
        yaxis_title = None,
        xaxis_tickangle = -15,
        font=dict(size=15),
        plot_bgcolor = 'rgb(0,0,0,0)',
        paper_bgcolor = 'rgb(0,0,0,0)'
    )
    return fig

@app.callback(
    Output('visual02', 'figure'),
    Output('visual03', 'figure'),
    [
        Input('chkMes', 'value'),
        Input('rdCategoria', 'value'),
        Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
    ]
)

def visual02(mes, categoria, toggle):
    #SECTION - Atualizar o tema do Dash App com o Dash Bootstrap Components e o Dash Bootstrap Templates
    template = dark_theme if toggle else vapor_theme
    
    #SECTION - Filtro de Mês e Categoria
    nomeMes = filtro_mes(mes)
    nomeCategoria = filtro_categoria(categoria)
    
    mesCategoria = nomeMes & nomeCategoria
    
    #SECTION - Filtrar o DataFrame
    df2 = df.loc[nomeCategoria]  
    df3 = df.loc[mesCategoria]
    
    #SECTION - Agrupar por Mês e Loja
    dfVendasMesLoja02 = df2.groupby(['Mes', 'Loja'])['Total Vendas'].sum().reset_index()
    dfVendasMesLoja03 = df3.groupby(['Mes', 'Loja'])['Total Vendas'].sum().reset_index()
    
    maxSize = dfVendasMesLoja02['Total Vendas'].max()
    minSize = dfVendasMesLoja02['Total Vendas'].min()
    
    ordemMes = [
        'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'
    ]
    
    #SECTION - definindo as cores  do gráfico
    coresLojas = {
        'Rio de Janeiro' : 'rgb(0, 0, 255)',
        'Salvador' : 'rgb(255, 0, 0)',
        'Santos' : 'rgb(0, 255, 0)',
        'São Paulo' : 'rgb(255, 255, 0)',
        'Três Rios' : 'rgb(255, 0, 255)'
    }
    
    #SECTION - Criando o gráfico visual02
    fig2 = graph_obj.Figure()
    
    for loja in dfVendasMesLoja02['Loja'].unique():
        dfLoja = dfVendasMesLoja02[dfVendasMesLoja02['Loja'] == loja]
        cor = coresLojas.get(loja, 'black')

        fig2.add_trace(
            graph_obj.Scatter(
                x = dfLoja['Mes'],
                y =  dfLoja['Total Vendas'],
                mode= 'markers',
                marker= dict(
                    color = cor,
                    size =  (dfLoja['Total Vendas'] - minSize) / 
                            (maxSize - minSize) * 50, 
                    opacity=0.5,
                    line=dict(color=cor, width=0)
                ),
                name=str(loja)
            )
        )
    fig2.update_layout(
        margin=dict(t=0),
        template=template,
        plot_bgcolor = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)',
        xaxis=dict(
            categoryorder='array',
            categoryarray=ordemMes,
            showgrid=False
        ),
        yaxis=dict(showgrid=False)
    )

    #SECTION - Criando o gráfico visual03
    fig3 = graph_obj.Figure(data=graph_obj.Scatterpolar(
        r = dfVendasMesLoja03['Total Vendas'],
        theta= dfVendasMesLoja03['Loja'],
        fill='toself',
        line=dict(color='rgb(31, 119, 180)'),
        marker=dict(color='rgb(31, 119, 180)', size=8),
        opacity=0.7
    ))

    fig3.update_layout(
        template=template,
        polar= dict(
            radialaxis=dict(
                visible=True,
                tickfont=dict(size=10),
                tickangle=0,
                tickcolor='rgba(68,68,68,0)',
                ticklen= 5,
                tickwidth=1,
                tickprefix='',
                ticksuffix='',
                #SECTION - Definindo o range do eixo radial do gráfico visual03 
                range=[0, max(dfVendasMesLoja03['Total Vendas']) + 1000]
            )
        ),
        font=dict(family='Fira Code', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=80, b=40)
    )
    
    return fig2, fig3

#executa o server e o app se o arquivo for executado diretamente
if __name__ == '__main__':
    app.run_server(debug=True)