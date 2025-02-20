from atexit import register
import io
from typing import Self
import dash
import os
from numpy import astype
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib as plt
import io
import base64
from dash import dcc, html
from dash.dependencies import Input, Output

# fixando o diretório de trabalho para evitar erro de [Errno 2] No such file or directory: 'dataset_comp.csv'
os.chdir(os.path.dirname(__file__))

app = dash.Dash(__name__)

df = pd.read_csv("vendas.csv")


class analisaVenda:
    def __init__(self, dado):
        self.dado = dado
        self.limpaDado()

    def limpaDado(self):
        self.dado["data"] = pd.to_datetime(self.dado["data"], errors="coerce")
        self.dado["valor"] = pd.to_numeric(self.dado["valor"], errors="coerce")
        self.dado["mes"] = self.dado["data"].dt.month
        self.dado["ano"] = self.dado["data"].dt.year
        self.dado["dia"] = self.dado["data"].dt.day
        self.dado["diaSemana"] = self.dado["data"].dt.weekday

        self.dado.dropna(subset=["produto", "valor"], inplace=True)

    def analisaVendaProduto(self, produtoFiltrado):
        dfProduto = self.dado[self.dado["produto"].isin(produtoFiltrado)]
        dfProduto = (
            dfProduto.groupby("produto")["valor"]
            .sum()
            .reset_index()
            .sort_values(by="valor", ascending=True)
        )
        fig = px.bar(
            dfProduto, x="produto", y="valor", title="Vendas por Produto", color="valor"
        )
        return fig

    def analisaVendaRegiao(self, regiaoFiltrado):
        dfRegiao = self.dado[self.dado["regiao"].isin(regiaoFiltrado)]
        dfRegiao = (
            dfRegiao.groupby("regiao")["valor"]
            .sum()
            .reset_index()
            .sort_values(by="valor", ascending=False)
        )
        fig = px.pie(
            dfRegiao,
            values="valor",
            names="regiao",
            title="Vendas por Regiao",
            color="valor",
        )
        return fig


analisa = analisaVenda(df)

app.layout = html.Div(
    [
        html.H1("Dashboard de Analise de vendas", style={"textAlign": "center"}),
        html.Div(
            [
                html.Label("Selecione o Produto"),
                dcc.Dropdown(
                    id="drpProduto",
                    options=[
                        {"label": produto, "value": produto}
                        for produto in df["produto"].unique()
                    ],
                    value=df["produto"].unique().tolist(),
                    multi=True,
                    style={"width": "48%"},
                ),
                html.Label("Selecione a Região"),
                dcc.Dropdown(
                    id="drpRegiao",
                    options=[
                        {"label": regiao, "value": regiao}
                        for regiao in df["regiao"].unique()
                    ],
                    value=df["regiao"].unique().tolist(),
                    multi=True,
                    style={"width": "48%"},
                ),
                html.Label("Selecione o Ano"),
                dcc.Dropdown(
                    id="drpAno",
                    options=[
                        {"label": str(ano), "value": ano} for ano in df["ano"].unique()
                    ],
                    value=df["ano"].min(),
                    style={"width": "48%"},
                ),
                html.Label("Selecione um Período"),
                dcc.DatePickerRange(
                    id="drpPeriodo",
                    start_date=df["data"].min().date(),
                    end_date=df["data"].max().date(),
                    display_format="YYYY-MM-DD",
                    style={"width": "100%"},
                ),
            ],
            style={"padding": "20px"},
        ),
        html.Div(
            [
                dcc.Graph(
                    id="graphProduto",
                )
            ]
        ),
        html.Div(
            [
                dcc.Graph(
                    id="graphRegiao",
                )
            ]
        ),
    ]
)


# Callback
@app.callback(
    Output("graphProduto", "figure"),
    Output("graphRegiao", "figure"),
    Input("drpProduto", "value"),
    Input("drpRegiao", "value"),
    Input("drpAno", "value"),
    Input("drpPeriodo", "start_date"),
    Input("drpPeriodo", "end_date"),
)
def upgrade_graphs(produtos, regioes, ano, start_date, end_date):
    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        fig_regiao = analisa.analisaVendaRegiao(regioes)
        fig_produto = analisa.analisaVendaProduto(produtos)
        return fig_produto, fig_regiao

    except Exception as e:

        print(f"Erro ao atualizar os gráficos: {str(e)}")
        return go.Figure()


# Rodar o app
if __name__ == "__main__":
    app.run_server(debug=True)
