import pandas as pd
import random as rd
import os
from datetime import datetime, timedelta

# fixando o diretório de trabalho para evitar erro de [Errno 2] No such file or directory: 'dataset_comp.csv'
os.chdir(os.path.dirname(__file__))


def gerarDadoVenda(numLinha):
    produto = ["Produto A", "Produto B", "Produto C", "Produto D"]
    regiao = ["Nordeste", "Sudeste", "Sul", "Norte", "Centro Oeste"]
    dado = []

    for aux in range(numLinha):
        linha = {
            "Data": datetime.now() - timedelta(days=rd.randint(0, 365)),
            "Produto": rd.choice(produto),
            "Regiao": rd.choice(regiao),
            "Quantidade": rd.randint(1, 100),
            "Valor": round(rd.uniform(10.0, 1000.0), 2),
        }
        dado.append(linha)
    return pd.DataFrame(dado, columns=["Produto", "Regiao", "Valor", "Data"])


dfVenda = gerarDadoVenda(
    999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
)

dfVenda.to_csv("vendas.csv", index=False)

print("Arquivo Gerado com sucesso")
