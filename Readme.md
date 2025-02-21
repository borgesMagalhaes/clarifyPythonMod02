🐍 Introdução ao Python e Bibliotecas Populares

Bem-vindo ao repositório de Introdução ao Python! Este repositório foi criado para ajudar iniciantes a aprender Python de forma simples e prática. Aqui, você encontrará exemplos envolvendo bibliotecas populares como Pandas, Matplotlib, NumPy, Dash e Plotly para manipulação de dados e visualização interativa.

📚 Objetivos do Repositório

Este repositório tem como objetivo:

Ensinar os conceitos básicos do Python:

Variáveis, tipos de dados, estruturas de controle, funções e manipulação de arquivos.

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

📌 05_oop/

Contém o arquivo oop.py, que implementa um painel interativo com Dash e Plotly.

📌 06_random/

Contém o arquivo random.py, que gera dados fictícios de vendas e salva em CSV.

📌 07_importDash/

Scripts importDash.py e newImportDash, junto com arquivos CSV venda.csv e vendas.csv, para análise de dados de vendas.

📌 08_consultaNome/

Contém consultaNome.py, um painel interativo que consulta dados de nomes na API do IBGE.

📄 Arquivos Principais

🔹 oop.py

Este script cria um painel interativo usando Dash e Plotly. Ele:

Gera um gráfico interativo utilizando Plotly;

Implementa callbacks no Dash para atualizar os gráficos dinamicamente;

Permite visualizar uma série de dados simulados.

🔹 random.py

Este script gera um conjunto de dados de vendas aleatório e salva em CSV. Ele:

Cria dados fictícios sobre produtos vendidos em diferentes regiões;

Usa a biblioteca Pandas para estruturar os dados;

Utiliza random para simular transações com valores variados.

🔹 consultaNome.py

Este script consulta a API do IBGE para obter a frequência de nomes ao longo dos anos. Ele:

Faz uma requisição HTTP para a API do IBGE;

Processa os dados recebidos em um DataFrame do Pandas;

Gera um gráfico interativo com Plotly Express;

Exibe os resultados em um painel interativo usando Dash.

🔧 Como Usar

1️⃣ Clonar o Repositório

git clone https://github.com/seu_usuario/introducao-python.git

cd introducao-python

2️⃣ Instalar Dependências

✅ Usando o script automático (install.bat) no Windows:

        install.bat

✅ Executando os comandos manualmente:

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
