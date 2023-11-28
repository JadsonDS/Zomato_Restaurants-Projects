# ==================================================
# Bibliotecas Necessárias
# ==================================================
import pandas as pd
import plotly as pl
import haversine as hs
import inflection
import numpy as np
import plotly.express as px
import folium 
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from PIL import Image 

#-------------------------------------Início das Funções-----------------------------------

st.set_page_config(page_title='Visão Geográfica', page_icon='🌎', layout='wide') 

# ==================================================
# Funções
# ==================================================
def mapa(df1):
    
    """ Está função tem a responsabilidade de criar a visão geográfica dos restaurantes por país.
        Conteúdo:
        1- A localização central de cada cidade por tipo de restaurante por país.
    """    
    df_aux=(df1.loc[:,['restaurant_id', 'restaurant_name', 'city', 'average_cost_for_two', 'currency',
                     'longitude', 'latitude', 'cuisines', 'aggregate_rating']]
               .groupby(['restaurant_id']).max().reset_index())

    map=folium.Map()
    marker_cluster=MarkerCluster(name ="restaurantes").add_to(map)

    def cor(rating_name):
        cores=df_aux.iloc[rating_name,8]
        return cores

    for i, location_info in df_aux.iterrows():
        folium.Marker([location_info['latitude'],location_info['longitude']],
                      popup=location_info[['restaurant_name',
                      'average_cost_for_two',
                      'currency',
                      'aggregate_rating']],
                      icon=folium.Icon(color=cor(i), icon='home')).add_to(marker_cluster) 

    folium_static(map, width=1300, height=550)

    return None

def country_name(country_id):
    
    """ Está função tem a responsabilidade de preenchimento do nome dos países. 
        Conteúdo:
        1- colocar o nome dos países com base no código de cada país.
    """    
    COUNTRIES={
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",}
    
    return COUNTRIES[country_id]


def create_price_type(price_range):
    
    """ Está função tem a responsabilidade de criar o tipo de categoria de comida. 
        Conteúdo:
        1- Criar a categoria do tipo de comida com base no range de valores.
    """        
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
def rename_columns(dataframe):
        
    """ Está função tem a responsabilidade de renomear as colunas do dataframe. 
    Conteúdo:
    1- Para renomear as colunas do dataframe.
    """    
    df=dataframe.copy()
    title=lambda x: inflection.titleize(x)
    snakecase=lambda x: inflection.underscore(x)
    spaces=lambda x: x.replace(" ", "")
    cols_old=list(df.columns)
    cols_old=list(map(title, cols_old))
    cols_old=list(map(spaces, cols_old))
    cols_new=list(map(snakecase, cols_old))
    df.columns=cols_new
    
    return df

def color_name(color_code):
    
    """ Está função tem a responsabilidade de criar o do nome das Cores. 
    Conteúdo:
    1- Criar o nome das cores com base nos códigos de cores.
    """    
    COLORS={
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",}

    return COLORS[color_code]


def clean_code(df1):
    
    """ Está função tem a responsabilidade de limpar o dataframe. 
    
        Tipos de Limpesa:
        1- Utilizando para renomear e substituir espaço por underline;
        2- Utilizando para criar a coluna com o nome dos países baseado nos códigos e na função country_name;
        3- Criando a coluna com os nomes das cores da avaliação;
        4- Criando a coluna com os nomes dos tipos de preço de comida (barato, normal e etc);
        5- Removendo as linhas com NAs;
        6- Todos os restaurantes somente por um tipo de culinária.
        
        Imput: Dataframe.
        Output: Dataframe.   
    """  
    df1=rename_columns(df1)
    
    df1['country']=df1.loc[:, 'country_code'].apply(lambda x: country_name(x)) 
    
    df1['color_rating_name']=df1.loc[:, 'rating_color'].apply(lambda x: color_name(x)) 
    
    df1['price_type']=df1.loc[:, 'price_range'].apply(lambda x: create_price_type(x)) 
    
    df1=df1.dropna() 
    df1=df1.drop_duplicates()
    
    df1["cuisines"]=df1.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0])
    
    return df1
   
#---------------------------Início da Estrutura lógica do código----------------------------

# ==================================================
# Import dataset
# ==================================================
df=pd.read_csv('zomato.csv')

# ==================================================
# Limpando os dados
# ==================================================
df1=clean_code(df)


# ==================================================
# Barra Lateral
# ==================================================
image=Image.open('logo.png')
st.sidebar.image(image, width=250)

st.sidebar.title('Zomato Restaurants')
st.sidebar.subheader('For the love of Food')
st.sidebar.subheader('', divider='gray')

st.sidebar.subheader('Selecione os países que deseja analisar:')

paises=st.sidebar.multiselect(
    "Selecione o  país:",
    df1.loc[:, "country"].unique().tolist(),    
    default=["Australia", "Brazil", "England", "India", "South Africa", "United States of America"])

st.sidebar.subheader('', divider='gray')
st.sidebar.subheader('Powered by: Jadson N Santos')

#Filtro de Países
todos_paises=df1['country'].isin(paises) 
df1=df1.loc[todos_paises, :]

# ==================================================
# Layout no Streamliy
# ==================================================
st.title('Visão de Negócio - Geográfica')
st.subheader('', divider='gray') 

st.subheader('Informações úteis para análise geral e geográfica de negócio:')

with st.container():
    col1, col2, col3, col4, col5=st.columns(5)
        
    with col1:
        rest_unic=len(df1['restaurant_id'].unique())
        col1.metric('Restaurantes:', rest_unic)

    with col2:       
        paises_unic=len(df1['country_code'].unique())
        col2.metric('Países:', paises_unic)
        
    with col3:
        city_unic=len(df1['city'].unique())
        col3.metric('Cidades:', city_unic)
        
    with col4:
        total_votes=len(df1['votes'].unique())
        col4.metric('Avaliações:', total_votes)
        
    with col5:    
        total_cuis=len(df1['cuisines'].unique())
        col5.metric('Culinárias:', total_cuis)
        
st.text('')              
        
st.subheader('', divider='gray')      
st.write('##### Mapa com a localização dos restaurantes por país:')
mapa(df1)
