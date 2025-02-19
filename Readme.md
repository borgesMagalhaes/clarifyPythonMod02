🐍 Introdução ao Python e Bibliotecas Populares
Bem-vindo ao repositório de Introdução ao Python! Este repositório foi criado para ajudar iniciantes a aprender Python de forma simples e prática. Aqui, você encontrará exemplos envolvendo bibliotecas populares como Pandas, Matplotlib, NumPy, Dash e Plotly para manipulação de dados e visualização interativa.

📚 Objetivos do Repositório
Este repositório tem como objetivo:

Ensinar os conceitos básicos do Python:

Variáveis, tipos de dados, estruturas de controle, funções, e manipulação de arquivos.
Explorar bibliotecas poderosas para manipulação de dados e visualização gráfica:

Pandas: Manipulação de dados em tabelas (DataFrames).
Matplotlib e Seaborn: Visualização gráfica de dados.
NumPy: Cálculos numéricos eficientes.
Dash e Plotly: Construção de painéis interativos e visualizações dinâmicas.
Exemplos práticos e explicativos, ideais para quem está começando a programar em Python.

🗂️ Estrutura do Repositório
O conteúdo está organizado nas seguintes pastas e arquivos:

📌 01_basico_python/
Fundamentos de Python, como variáveis, tipos de dados, listas, loops, funções.

📌 02_pandas/
Manipulação de dados com Pandas, incluindo:

Leitura de arquivos CSV;
Filtragem e agregação de dados;
Tratamento de valores nulos e preenchimento de dados ausentes.
📌 03_dash_plotly/
Criação de visualizações interativas utilizando Dash e Plotly.

📌 04_main_store/
Manipulação de arquivos CSV e criação de filtros avançados para visualizações.

📄 Arquivos Principais
🔹 readCsv.py
Script para leitura e manipulação de dados de arquivos CSV. Ele:

Lê arquivos CSV de hospedagens em Nova York e Rio de Janeiro;
Faz o tratamento de dados, convertendo datas e preenchendo valores ausentes;
Ajusta preços com base no ano;
Gera estatísticas descritivas sobre os dados.
🔹 portifolio.py
Aplicação interativa utilizando Dash e Plotly, que exibe conceitos sobre linguagens de programação. Possui:

Um dropdown para seleção de linguagem;
Um gráfico de dispersão mostrando o nível de conhecimento nos conceitos principais (variáveis, condicionais, loops, POO, funções).
🔹 main_store.py
Painel interativo para análise de vendas, utilizando Dash e Dash Bootstrap Components. Ele:

Carrega dados de vendas a partir de um CSV;
Permite filtragem por cliente, categoria de produto e mês de venda;
Exibe gráficos de vendas por cliente, mês e cidade.

🔧 Como Usar
1️⃣ Clonar o Repositório
  git clone https://github.com/seu_usuario/introducao-python.git
  cd introducao-python

2️⃣ Instalar Dependências
  python.exe -m pip install --upgrade pip
  pip install -r requirements.txt

3️⃣ Executar os Scripts
Para rodar a aplicação do Dash:
  python portifolio.py
  ou
  python main_store.py
  ou
  python readCsv.py
  
🚀 Contribuições
Sinta-se à vontade para contribuir! Se quiser sugerir melhorias, abra um Pull Request ou Issue.