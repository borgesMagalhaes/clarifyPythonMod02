import dash
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output

# Fixar diretório para evitar erro
os.chdir(os.path.dirname(__file__))

# Carregar os dados
df = pd.read_csv("vendas.csv")

df["data"] = pd.to_datetime(df["data"], errors="coerce")
df.dropna(subset=["data", "valor", "produto", "regiao"], inplace=True)

app = dash.Dash(__name__)


class AnalisaVenda:
    def __init__(self, dado):
        self.dado = dado
        self.limpaDado()

    def limpaDado(self):
        self.dado["valor"] = pd.to_numeric(self.dado["valor"], errors="coerce")
        self.dado["mes"] = self.dado["data"].dt.month
        self.dado["ano"] = self.dado["data"].dt.year
        self.dado["dia"] = self.dado["data"].dt.day
        self.dado["diaSemana"] = self.dado["data"].dt.weekday

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


analisa = AnalisaVenda(df)

app.layout = html.Div(
    style={"max-width": "1200px", "margin": "auto", "padding": "20px"},
    children=[
        html.H1("Dashboard de Análise de Vendas", style={"text-align": "center"}),
        html.Div(
            style={"display": "flex", "flex-wrap": "wrap", "gap": "20px"},
            children=[
                html.Div(
                    children=[
                        html.Label("Selecione o Produto"),
                        dcc.Dropdown(
                            id="drpProduto",
                            options=[
                                {"label": p, "value": p} for p in df["produto"].unique()
                            ],
                            value=df["produto"].unique().tolist(),
                            multi=True,
                            style={"width": "100%"},
                        ),
                    ],
                    style={"flex": "1"},
                ),
                html.Div(
                    children=[
                        html.Label("Selecione a Região"),
                        dcc.Dropdown(
                            id="drpRegiao",
                            options=[
                                {"label": r, "value": r} for r in df["regiao"].unique()
                            ],
                            value=df["regiao"].unique().tolist(),
                            multi=True,
                            style={"width": "100%"},
                        ),
                    ],
                    style={"flex": "1"},
                ),
                html.Div(
                    children=[
                        html.Label("Selecione o Ano"),
                        dcc.Dropdown(
                            id="drpAno",
                            options=[
                                {"label": str(ano), "value": ano}
                                for ano in df["ano"].unique()
                            ],
                            value=df["ano"].min(),
                            style={"width": "100%"},
                        ),
                    ],
                    style={"flex": "1"},
                ),
                html.Div(
                    children=[
                        html.Label("Selecione um Período"),
                        dcc.DatePickerRange(
                            id="drpPeriodo",
                            start_date=df["data"].min().date(),
                            end_date=df["data"].max().date(),
                            display_format="YYYY-MM-DD",
                            style={"width": "100%"},
                        ),
                    ],
                    style={"flex": "1"},
                ),
            ],
        ),
        html.Div(
            style={"margin-top": "20px"},
            children=[dcc.Graph(id="graphProduto")],
        ),
    ],
)


@app.callback(
    Output("graphProduto", "figure"),
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

        produtos = list(produtos) if produtos else []
        regioes = list(regioes) if regioes else []
        ano = int(ano) if ano else df["ano"].max()

        fig_produto = analisa.analisaVendaProduto(produtos)
        return fig_produto

    except Exception as e:
        print(f"Erro ao atualizar os gráficos: {str(e)}")
        return go.Figure()


# Rodar o app
if __name__ == "__main__":
    app.run_server(debug=True)
