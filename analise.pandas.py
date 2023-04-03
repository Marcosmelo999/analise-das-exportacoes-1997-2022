#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd                    #Importando as bibliotecas que usarei ou poderei usar
import matplotlib.pyplot as plot
import os 
import numpy as np


# In[3]:


os.chdir(r'C:\Aprendizado\AnaliseDados_Pratica')    #Apontando o caminho dos meus dados


# In[276]:


Tab_Geral = pd.read_csv ('EXP_COMPLETA.csv',  sep=";", encoding = "latin1")  #Carregando meus dados na variável Tab_Geral


# In[277]:


Tab_Geral   # lendo os meus dados


# In[357]:


Tab_Geral.info()   #Boa prática ao se analisar dados é conferir os tipos de dados do dataframe


# In[358]:


Tab_Geral.isnull().sum()   #Fazendo contagem de eventuais dados ausentes


# In[363]:


if Tab_Geral.duplicated().any():                  #Função para verificação de linhas repetidas também uma boa prática no ETL
    print('Existem linhas duplicadas na tabela')
else:
    print('Não existem linhas duplicadas na tabela')


# In[364]:


Tab_Geral_selecao = Tab_Geral[['CO_ANO','CO_MES','VL_FOB']] #Selecionando as colunas que preciso


# In[365]:


Tab_Geral_selecao


# In[366]:


Tab_Geral_Agrupado = Tab_Geral_selecao.groupby(['CO_ANO','CO_MES']).sum() #agrupando pela soma por ANO e MÊS


# In[367]:


Tab_Geral_Agrupado


# In[368]:


Tab_Geral_Agrupado = Tab_Geral_Agrupado.sort_values(by=['CO_ANO','VL_FOB'], ascending=False)
Tab_Geral_Agrupado         #Ordenando os valores do maior para o menor


# In[369]:


Maior_VLFOB_MES_ANO = Tab_Geral_Agrupado.groupby(['CO_ANO', 'CO_MES'])['VL_FOB'].max().reset_index()

#MÊS com maior valor de exportação para cada ano


# In[370]:


Maior_VLFOB_MES_ANO = Maior_VLFOB_MES_ANO.sort_values(['CO_ANO', 'VL_FOB'], ascending=[True, False]).groupby('CO_ANO').first()['CO_MES']
#Pegando apenas o primeiro mês com o màximo valor para cada ano , afim de verificar uma sazonalidade.


# In[371]:


Maior_VLFOB_MES_ANO = Maior_VLFOB_MES_ANO.reset_index()
Maior_VLFOB_MES_ANO


# In[372]:


Mes_Moda = Maior_VLFOB_MES_ANO['CO_MES'].value_counts().idxmax()
Mes_Moda
 
#Agosto é o mês que mais se exporta, visto que é o valor que mais se repete na tabela em termos de valores entre 1997_2022


# In[373]:


Tab_Geral_Agrupado.query('CO_ANO == 2002') #Consulta de verificação usando filtro


# In[374]:


os.listdir()## Trazer tabela PAÍS para fazer um merge com Tab_Geral e fazer gráfico.Boa prática pegar pelo nome do arquivo


# In[375]:


Tb_Aux_Pais = pd.read_csv(r'PAIS.csv', sep=';', encoding = 'Latin1')  


# In[376]:


Tb_Aux_Pais 


# In[377]:


Tab_Geral


# In[378]:


Tab_Geral_Pais = pd.merge(Tab_Geral[['CO_PAIS','CO_ANO','CO_MES','SG_UF_NCM','VL_FOB']] 
                             , Tb_Aux_Pais[['CO_PAIS','NO_PAIS']], on='CO_PAIS')

#Selecionado colunas da Tabela geral e coluna com o nome do País da tabela auxiliar


# In[379]:


Tab_Geral_Pais


# In[380]:


Tabela_Agrupada_Geral_Pais = Tab_Geral_Pais.groupby('NO_PAIS').sum('VL_FOB').sort_values(by='VL_FOB', ascending=False)


# In[381]:


Top_10 = Tabela_Agrupada_Geral_Pais.head(10)
Top_10


# In[382]:


Top_10 = Top_10.reset_index()  #resentando para fazer a plotagem 


# In[383]:


Top_10 = Top_10.sort_values(by='VL_FOB', ascending=True) #ordeanando para plotar do maior para menor Pais e Vl_FOB
Top_10


# In[384]:


# gráfico de barras horizontais
Top_10.plot(x='NO_PAIS', y='VL_FOB',kind='barh', legend=True)

# título do gráfico e dos eixos
plot.title('Principais Destinos das Exportações 1997-2022')
plot.xlabel('Valor FOB')
plot.ylabel('País')

# Exibir
plot.show()


# In[385]:


Tab_Geral_Pais_UF = Tab_Geral_Pais.groupby('SG_UF_NCM').sum('VL_FOB')  #agrupando o total do valor exportado por Estado
Tab_Geral_Pais_UF = Tab_Geral_Pais_UF.sort_values('VL_FOB', ascending=False) #ordenando do maior para menos valor FOB
Tab_Geral_Pais_UF = Tab_Geral_Pais_UF.head(10) #top 10 dos estados com maior valor
Tab_Geral_Pais_UF


# In[386]:


Tab_Geral_Pais_UF = Tab_Geral_Pais_UF.reset_index()   #resetando o index para poder plotar o gráfico
Tab_Geral_Pais_UF


# In[387]:


# Cria o gráfico de barras horizontais
Tab_Geral_Pais_UF.plot(x='SG_UF_NCM', y='VL_FOB',kind='bar', legend=True)

# Define o título do gráfico e dos eixos
plot.title('Exportações por Estado 1997-2022')
plot.xlabel('Estado')
plot.ylabel('Valor FOB')

# Exibe o gráfico
plot.show()


# In[388]:


Tab_Geral_ANO = Tab_Geral.groupby('CO_ANO').sum('VL_FOB')
Tab_Geral_ANO = Tab_Geral_ANO.drop(columns=['CO_MES','CO_NCM','CO_VIA','CO_UNID','CO_PAIS','CO_URF','QT_ESTAT','KG_LIQUIDO']) 
Tab_Geral_ANO


# In[389]:


Tab_Geral_ANO = Tab_Geral_ANO.reset_index()   #Resetando index para plotar


# In[390]:


#Grafico de barras verticais para apresentar a evolução ano a ano das exportações de 1997_2022

# Cria o gráfico de barras horizontais
Tab_Geral_ANO.plot(x='CO_ANO', y='VL_FOB',kind='bar', legend=True)

# Define o título do gráfico e dos eixos
plot.title('Exportações 1997_2022')
plot.xlabel('ANO')
plot.ylabel('Valor FOB')

# Exibe o gráfico
plot.show()


# In[391]:


tabela_BL_Economico = pd.read_csv(r'PAIS_BLOCO.csv', sep=';', encoding = 'Latin1')
tabela_BL_Economico    #Carregando minha tabela auxiliar com o nome bloco econômico


# In[392]:


Tab_Geral_Pais_Bloco = pd.merge (Tab_Geral_Pais[['CO_PAIS','CO_ANO','CO_MES','SG_UF_NCM','VL_FOB','NO_PAIS']],
                                 tabela_BL_Economico[['CO_PAIS','NO_BLOCO']], on='CO_PAIS')

#Unindo a coluna nome do Bloco economico da tabela auxilar na minha tabela principal


# In[393]:


Tab_Geral_Pais_Bloco


# In[394]:


Tab_Bloco = Tab_Geral_Pais_Bloco.groupby('NO_BLOCO').sum('VL_FOB') #Fazendo agregação do Valor exportado para cada Bloco
Tab_Bloco = Tab_Bloco.sort_values('VL_FOB',ascending=False)


# In[395]:


Tab_Bloco


# In[396]:


Tab_Bloco = Tab_Bloco.drop(columns=['CO_PAIS','CO_ANO','CO_MES']) #Exluindo colunas desnecessárias


# In[397]:


Tab_Bloco


# In[398]:


Tab_Bloco = Tab_Bloco.reset_index()  #Faço o reset index para plotar o gráfico


# In[399]:


#Crie um gráfico de pizza com rótulos reduzidos
fig, ax = plot.subplots()
ax.pie(Tab_Bloco['VL_FOB'], labels=Tab_Bloco['NO_BLOCO'], autopct='%1.1f%%', textprops={'fontsize': 10})

# Mostre o gráfico
plot.show()


# In[ ]:


#Conforme gráfico acima venos que temos O continente Europeu como bloco econômico de maior destino das exportações 
#seguido da Ásia.


# In[ ]:




