import pandas as pd
# import numpy as np
# import matplotlib as plot
# import seaborn as sborn

from IPython.display import display
# from matplotlib import pyplot

with open('./02_pandas/links.txt', 'r') as arquivo:
    links = arquivo.readlines()

links = [link.strip() for link in links]

# dfNy = pd.read_csv("https://www.dropbox.com/s/8i2nw6bd5ha7vny/listingsNY.csv?dl=1")
# dfRj = pd.read_csv("https://www.dropbox.com/s/yyg8hso7fbjf1ft/listingsRJ.csv?dl=1")

dfNy = pd.read_csv(links[0])
dfRj = pd.read_csv(links[1])

# dfNy['Link'] = links[0] 
# dfRj['Link'] = links[1] 

#Apenas para verificar a vizualização dos documentos.
print("############## INICIO DataFrame NY: ##############")
print("DataFrame NY: " + links[0])  
print(dfNy.head(10))
print("############## FIM DataFrame NY: #################")
print("--------------------------------------------------")
print("############## INICIO DataFrame RJ: ##############")
print("DataFrame RJ: " + links[1]) 
print(dfRj.head(10)) 
print("############## FIM DataFrame RJ: #################")


print(f'New York\nEntradas: {dfNy.shape[0]}\nVariaveis:{dfNy.shape[1]}\n')
display(dfNy.dtypes)
print(f'----------------------------------------------------------------------')    
print(f'Rio de janeiro\nEntradas: {dfRj.shape[0]}\nVariaveis:{dfRj.shape[1]}\n')
display(dfRj.dtypes)
print(f'----------------------------------------------------------------------')

dfNy['last_review'] =  pd.to_datetime(dfNy['last_review'], format="%Y-%m-%d")
dfNy.last_review =  pd.to_datetime(dfNy.last_review, format="%Y-%m-%d")   
dfNy['last_review'] = pd.to_datetime(dfNy['last_review'], format="%Y-%m-%d")

print(dfNy['last_review'])
print(dfNy.last_review)
print(dfNy['last_review'].dtype)

