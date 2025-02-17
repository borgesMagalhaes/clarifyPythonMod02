import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot
import seaborn as sborn

from IPython.display import display

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
# # print("############## INICIO DataFrame NY: ##############")
# # print("DataFrame NY: " + links[0])  
# # print(dfNy.head(10))
# # print("############## FIM DataFrame NY: #################")
# # print("--------------------------------------------------")
# # print("############## INICIO DataFrame RJ: ##############")
# # print("DataFrame RJ: " + links[1]) 
# # print(dfRj.head(10)) 
# # print("############## FIM DataFrame RJ: #################")

# # print(f'New York\nEntradas: {dfNy.shape[0]}\nVariaveis:{dfNy.shape[1]}\n')
# # display(dfNy.dtypes)
# # print(f'----------------------------------------------------------------------')    
# # print(f'Rio de janeiro\nEntradas: {dfRj.shape[0]}\nVariaveis:{dfRj.shape[1]}\n')
# # display(dfRj.dtypes)
# # print(f'----------------------------------------------------------------------')

dfNy['last_review'] =  pd.to_datetime(dfNy['last_review'], format="%Y-%m-%d")
# dfNy.last_review =  pd.to_datetime(dfNy.last_review, format="%Y-%m-%d")  
dfNy['year'] = dfNy['last_review'].dt.year

# print(dfNy['last_review'])
# print(dfNy.last_review)

dfNy['price'] = dfNy['price'].mask(dfNy['year'] <= 2011, dfNy['price'] / 1.174)
dfNy['price'] = dfNy['price'].mask(dfNy['year'] <= 2012, dfNy['price'] / 2.174)
dfNy['price'] = dfNy['price'].mask(dfNy['year'] <= 2013, dfNy['price'] / 3.174)
dfNy['price'] = dfNy['price'].mask(dfNy['year'] <= 2014, dfNy['price'] / 4.174)
dfNy['price'] = dfNy['price'].mask(dfNy['year'] <= 2015, dfNy['price'] / 5.174)
dfNy['price'] = dfNy['price'].mask(dfNy['year'] <= 2016, dfNy['price'] / 6.174)
dfNy['price'] = dfNy['price'].mask(dfNy['year'] <= 2017, dfNy['price'] / 7.374)
dfNy['price'] = dfNy['price'].mask(dfNy['year'] <= 2018, dfNy['price'] / 1.674)
dfNy['price'] = dfNy['price'].mask(dfNy['year'] <= 2019, dfNy['price'] / 1.974)
dfNy['price'] = dfNy['price'].mask(dfNy['year'] <= 2020, dfNy['price'] / 3.174)
dfNy['price'] = dfNy['price'].mask(dfNy['year'] <= 2021, dfNy['price'] / 5.674)

variaveis = ['id',
             'name',
             'host_id',
             'host_name',
             'neighbourhood_group',
             'neighbourhood',
             'latitude',
             'longitude',
             'room_type',
             'price',
             'minimum_nights',
             'number_of_reviews',
             'last_review',
             'reviews_per_month',
             'calculated_host_listings_count',
             'availability_365',
             'number_of_reviews_ltm',
             'license'
        ]
vz = []
dado = []

for i in variaveis:
    dado.append(dfNy[i].isnull().sum()/dfNy[i].shape[0])
    dado.append(dfRj[i].isnull().sum()/dfRj[i].shape[0])
    vz.append(dado[:])
    dado.clear()
print(vz)

pd.DataFrame(vz, columns=['New York', 'Rio de Janeiro'], index=variaveis)
print(pd.DataFrame(vz, columns=['New York', 'Rio de Janeiro'], index=variaveis))

dfNy_clean = dfNy.dropna(subset=['name', 'host_name'], axis=0)   
dfRj_clean = dfRj.dropna(subset=['name', 'host_name'], axis=0)

#calcular a mediana de reviews_per_month
rpm_ny_mediana = dfNy_clean.reviews_per_month.median()
rpm_rj_mediana = dfRj_clean.reviews_per_month.median()

#substituir pela mediana
dfNy_clean = dfNy_clean.fillna({'reviews_per_month': rpm_ny_mediana})
dfRj_clean = dfRj_clean.fillna({'reviews_per_month': rpm_rj_mediana})

#calcular o valor usando o metodo de interpolação midpoint para last_review
lr_ny_mediana = dfNy_clean['last_review'].astype('datetime64[ns]').quantile(0.5, interpolation='midpoint')
lr_rj_mediana = dfRj_clean['last_review'].astype('datetime64[ns]').quantile(0.5, interpolation='midpoint')

#substituir pelo valor calculado do last_review pela interpolação midpoint
dfNy_clean = dfNy_clean.fillna({'last_review': lr_ny_mediana}) 
dfRj_clean = dfRj_clean.fillna({'last_review': lr_rj_mediana})

dx0 = ['price', 'minimum_nights']

# for aux in dx0:
#     data_A = dfNy_clean[aux]
#     data_B = dfRj_clean[aux]
#     data_2d = [data_A, data_B]

#     plt.boxplot(data_2d, vert=False, labels=["New York", "Rio de Janeiro"])
#     plt.title(aux)
#     plt.show()

dfNy_clean[['price', 'minimum_nights','number_of_reviews',
                'reviews_per_month',
                'calculated_host_listings_count','availability_365']].describe
    
dfNy_copy = dfNy_clean.copy()
dfNy_copy.drop(dfNy_copy[dfNy_copy.price > 1100].index, axis=0, inplace=True)
dfNy_copy.drop(dfNy_copy[dfNy_copy.minimum_nights > 66].index, axis=0, inplace=True)


dfRj_clean[['price', 'minimum_nights','number_of_reviews',
                'reviews_per_month',
                'calculated_host_listings_count','availability_365']].describe

dfrj_copy = dfRj_clean.copy()
dfrj_copy.drop(dfrj_copy[dfrj_copy.price > 600].index, axis=0, inplace=True)
dfrj_copy.drop(dfrj_copy[dfrj_copy.minimum_nights > 4].index, axis=0, inplace=True)

var = ['Entire Home/Apt', 
       'Private room',
       'Shared room',
       'Hotel room']

dadoVar = {}

for aux in var:
    dadoVar[aux] = [dfNy_copy.loc[dfNy_copy.room_type == aux].shape[0]/dfNy_copy.room_type.shape[0],    
                    dfrj_copy.loc[dfrj_copy.room_type == aux].shape[0]/dfrj_copy.room_type.shape[0] ]
ima = pd.DataFrame(dadoVar, index=['New York', 'Rio de Janeiro'])
ima.plot(kind="barh", stacked=True, figsize=(6,4), color=['blue', 'red', 'green', 'yellow'])
plt.legend(loc="lower left", bbox_to_anchor=(0.8, 1.0))
plt.title("Room Type")
plt.show()
