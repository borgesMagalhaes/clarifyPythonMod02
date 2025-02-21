from atexit import register
import io
from typing import Self
import dash
import os
from matplotlib import markers
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
print(os.getcwd())  # Verifica o diretório atual
print(os.listdir())  # Lista os arquivos na pasta
print(df.head())  # Exibe as primeiras linhas do dataframe
print(df.columns)  #


class analisaVenda:
    def __init__(self, dado):
        self.dado = dado
        self.limpaDado()

    def limpaDado(self):

        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df.dropna(subset=["data"], inplace=True)  # Remove possíveis valores NaT
        print(df["data"].dtypes)
        print(df["data"].head())  # Veja os primeiros valores

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

    def analiseVendaRegiao(self, regioes_filtradas):
        df_regiao = self.dado[self.dado["regiao"].isin(regioes_filtradas)]
        df_regiao = (
            df_regiao.groupby("regiao")["valor"]
            .sum()
            .reset_index()
            .sort_values(by="valor", ascending=False)
        )
        fig = px.pie(
            df_regiao,
            names="regiao",
            values="valor",
            title="Vendas por Região",
            color="valor",
        )
        return fig

    def analiseVendaMensal(self, anoFiltrado):
        dfMes = self.dado[self.dado["ano"] == anoFiltrado]
        dfMes = dfMes.groupby(["mes", "ano"])["valor"].sum().reset_index()
        fig = px.line(
            dfMes,
            x="mes",
            y="valor",
            title=f"Vendas por Mes - {anoFiltrado}",
            color="ano",
            markers=True,
            line_shape="spline",
        )
        return fig

    def analiseVendaDiaria(self, data_inicio, data_fim):
        dfDia = self.dado[
            (self.dado["data"] >= data_inicio) & (self.dado["data"] <= data_fim)
        ]
        dfDia = dfDia.groupby("data")["valor"].sum().reset_index()
        fig = px.line(
            dfDia,
            x="data",
            y="valor",
            title=f"Vendas por Dia ",
            color="valor",
            markers=True,
        )
        return fig

    def analiseVendaDiaSemana(self):
        dfDiaSemana = self.dado.groupby("diaSemana")["valor"].sum().reset_index()
        dfDiaSemana["diaSemana"] = dfDiaSemana["diaSemana"].map(
            {
                0: "Domingo",
                1: "Segunda",
                2: "Terca",
                3: "Quarta",
                4: "Quinta",
                5: "Sexta",
                6: "Sabado",
            }
        )
        fig = px.bar(
            dfDiaSemana,
            x="diaSemana",
            y="valor",
            title="Vendas por Dia da Semana",
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
        html.Div(
            [
                dcc.Graph(
                    id="graphMensal",
                )
            ]
        ),
        html.Div(
            [
                dcc.Graph(
                    id="graphVendaDiaria",
                )
            ]
        ),
        html.Div(
            [
                dcc.Graph(
                    id="graphDiaSemana",
                )
            ]
        ),
    ]
)


# Callback
@app.callback(
    Output("graphProduto", "figure"),
    Output("graphRegiao", "figure"),
    Output("graphMensal", "figure"),
    Output("graphVendaDiaria", "figure"),
    Output("graphDiaSemana", "figure"),
    Input("drpProduto", "value"),
    Input("drpRegiao", "value"),
    Input("drpAno", "value"),
    Input("drpPeriodo", "start_date"),
    Input("drpPeriodo", "end_date"),
)
def test_callback(produtos, regioes, ano, start_date, end_date):
    print("Callback Teste chamado com:", produtos, regioes, ano, start_date, end_date)
    return go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure()


def upgrade_graphs(produtos, regioes, ano, start_date, end_date):
    try:

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        ano = ano

        figProduto = analisa.analisaVendaProduto(produtos)
        figRegiao = analisa.analiseVendaRegiao(regioes)
        figMensal = analisa.analiseVendaMensal(ano)
        figVendaDiaria = analisa.analiseVendaDiaria(start_date, end_date)
        figDiaSemana = analisa.analiseVendaDiaSemana()

        print("🚀 Callback foi chamado!")
        print(
            f"Produtos: {produtos}, Regiões: {regioes}, Ano: {ano}, Datas: {start_date} - {end_date}"
        )

        print(
            "Callback disparado com valores:",
            produtos,
            regioes,
            ano,
            start_date,
            end_date,
        )

        return figProduto, figRegiao, figMensal, figVendaDiaria, figDiaSemana

    except Exception as e:

        print(f"Erro ao atualizar os gráficos: {str(e)}")
        import traceback

        print("ERRO NO CALLBACK")
        print(traceback.format_exc())  # Exibe detalhes do erro
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure()


# Rodar o app
if __name__ == "__main__":
    app.run_server(debug=True)
