import dash
from dash import dcc, html
import requests
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)


def consultaNome():
    url = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/joao|maria"

    response = requests.get(url)
    dados = response.json()

    nomes = []
    for nomeData in dados:
        nome = nomeData["nome"]
        for res in nomeData["res"]:
            periodo = res["periodo"]
            frequencia = res["frequencia"]
            nomes.append({"Nome": nome, "Período": periodo, "Frequência": frequencia})

    return pd.DataFrame(nomes)


def criarGrafico(df):
    fig = px.line(
        df,
        x="Período",
        y="Frequência",
        color="Nome",
        title="Frequência dos nomes ao longo dos anos",
        labels={"Período": "Período", "Frequência": "Frequência"},
    )
    return fig


app.layout = html.Div(
    [
        html.H1("Frequência dos Nomes ao Longo dos Anos"),
        dcc.Graph(id="graphNome", figure=criarGrafico(consultaNome())),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
