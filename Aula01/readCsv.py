import pandas as pd
# import numpy as np
# import matplotlib as plot
# import seaborn as sborn

from IPython.display import display
# from matplotlib import pyplot

dfNy = pd.read_csv("https://www.dropbox.com/s/8i2nw6bd5ha7vny/listingsNY.csv?dl=1")
dfRj = pd.read_csv("https://www.dropbox.com/s/yyg8hso7fbjf1ft/listingsRJ.csv?dl=1")

with open('links.txt', 'r') as arquivo:
    links = arquivo.readlines()

links = [link.strip() for link in links]

dfNy['Link'] = links[0] 
dfRj['Link'] = links[1] 

#Apenas para verificar a vizualização dos documentos.
# print("DataFrame NY:")
# print(dfNy.all)
# print("\nDataFrame RJ:")
# print(dfRj.all)
