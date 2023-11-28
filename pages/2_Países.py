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

st.set_page_config(page_title='Visão Países', page_icon='🇽🇰', layout='wide') 

# ==================================================
# Funções
# ==================================================

def aceit_resev(df1):
    
     """ Está função tem a responsabilidade de preenchimento da uantidade de restaurantes que aceitam reservas por país. 
        Conteúdo:
        1- colocar a quantidade  de restaurantes que aceitam reservas com base no código de cada país.
    """        
     filtro=(df1 ['has_table_booking'] == 1)
 
     df2=df1.loc[filtro, ['restaurant_id', 'country']].groupby(['country']).max().reset_index()

     fig=(px.pie(df2, values='restaurant_id', names='country', hole=0.4))
          
     fig.update_traces(textfont_size=12, textfont_color='black')
     
     return fig


def cul_dist_aceit_resv(df1):
    
    """ Está função tem a responsabilidade de preenchimento da quantidade de culinária distinta por país. 
        Conteúdo:
        1- colocar a quantidade  de culinária distinta com base no código de cada país.
    """
    df2=df1.loc[:,['cuisines', 'country']].groupby(['country']).nunique().reset_index()

    fig=px.sunburst(df2, path=['cuisines', 'country'], color='cuisines', color_continuous_scale='Rainbow')
    
    fig.update_traces(textfont_size=13, textfont_color='black')
    
    return fig

 
def prato_dois(df1):
    
    """ Está função tem a responsabilidade de preenchimento da quantidade média de preço de um prato para duas pessoas por país. 
        Conteúdo:
        1- colocar a quantidade  de restaurantes na média de Preço de um Prato para Duas Pessoas com base no código de cada país.
    """        
    df2=(df1.loc [:, ['currency', 'country', 'average_cost_for_two']]
              .groupby(['currency', 'country', 'average_cost_for_two'])
              .mean().round(2).reset_index())
             
    df3=(df2.loc [:, ['average_cost_for_two', 'country', 'currency' ]].groupby(['country', 'currency'])
              .mean().round(2).sort_values('average_cost_for_two', ascending=False).reset_index()) 

    fig=(px.bar(df3, x='country', y='average_cost_for_two', color='currency', title='Média de preço de um prato para duas pessoas por país', text_auto=True, 
    labels={'country': 'Países', 'average_cost_for_two': 'Preço do Prato para duas Pessoas ', 'currency': 'Moeda'}))

    fig.update_traces(textfont_size=10, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black')
    
    return fig


def med_aval_pais(df1):
    
    """ Está função tem a responsabilidade de preenchimento da quantidade média de avaliações feitas por país. 
        Conteúdo:
        1- colocar a quantidade  por média de avaliações feitas com base no código de cada país.
    """    
    df2=(df1.loc [:, ['votes', 'country']].groupby(['country'])
         .sum().reset_index())

    fig=px.scatter(df2, x ='country', y='votes', size='votes', color='country', title='Média de avaliações feitas por país', text='votes', 
    labels={'country': 'Países', 'votes': 'Total de Avaliações'}) 
    
    fig.update_traces(textfont_size=13, textposition="top center", cliponaxis=False, textfont_color='black') 
     
    return fig 

def qnt_rest_pais(df1):
    
    """ Está função tem a responsabilidade de preenchimento da quantidade de resturantes registrados por país. 
        Conteúdo:
        1- colocar a quantidade de restaurantes com base no código de cada país.
    """
    df2=(df1.loc[:,['restaurant_id','country']].groupby(['country','restaurant_id'])
             .count().reset_index())

    df3=(df2.loc[:,['restaurant_id','country']].groupby(['country']).count()
              .sort_values('restaurant_id', ascending=False ).reset_index())
        
    fig=(px.bar(df3, x ='country', y='restaurant_id', title='Quantidade de restaurantes registrados por país', text_auto=True, 
    labels={'country': 'Países', 'restaurant_id': 'Total de Restaurantes'}))

    fig.update_traces(textfont_size=12, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black')
    
    return fig

def qnt_city_pais(df1):
    
    """ Está função tem a responsabilidade de Preenchimento da quantidade de cidades registradas por país. 
        Conteúdo:
        1- colocar a quantidade de cidades com base no código de cada país.
    """    
    df2=df1.loc[:,['city','country']].groupby(['country','city']).count().reset_index()

    df3=(df2.loc[:,['city','country']].groupby(['country']).count()
             .sort_values('city', ascending=False ).reset_index())

    fig=(px.bar(df3, x='country', y='city', title='Quantidade de cidades registradas por país', text_auto=True, 
    labels={'country': 'Países', 'city': 'Total de Cidades'}))
    
    fig.update_traces(textfont_size=12, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black') 
    
    return fig


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
df=pd.read_csv('dataset/zomato.csv')

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
    default=["Australia", "Brazil", "Canada", "England", "India", "Indonesia", "South Africa", "United States of America"])

st.sidebar.subheader('', divider='gray')
st.sidebar.subheader('Powered by: Jadson N Santos')


#Filtro de Países
todos_paises=df1['country'].isin(paises) 
df1=df1.loc[todos_paises, :]

# ==================================================
# Layout no Streamliy
# ==================================================
st.title('Visão de Negócio - Países')
st.subheader('', divider='gray') 

st.subheader('Informações úteis para tomadas de decisões de negócio com base nos países:')
st.subheader('', divider='gray') 

with st.container():
    col1, col2=st.columns(2, gap='small')
        
    with col1:
        fig=qnt_city_pais(df1)
        st.plotly_chart(fig, use_container_width=True)
        

    with col2:       
        fig=qnt_rest_pais(df1)
        st.plotly_chart(fig, use_container_width=True)
        
st.subheader('', divider='gray')         
        
with st.container():    
        fig=med_aval_pais(df1)         
        st.plotly_chart(fig, use_container_width=True)
        
st.subheader('', divider='gray') 
        
with st.container():
    fig=prato_dois(df1)
    st.plotly_chart(fig, use_container_width=True)

st.subheader('', divider='gray') 


with st.container():
    col1, col2=st.columns(2, gap='small')
        
    with col1:
        st.markdown('###### Quantidade de culinária distinta por país') 
        fig=cul_dist_aceit_resv(df1)        
        st.plotly_chart(fig, use_container_width=True, height=200) 
        

    with col2:
        st.markdown('###### Restaurantes que aceitam reservas por país')       
        fig=aceit_resev(df1)          
        st.plotly_chart(fig, use_container_width=True, height=200)        
        

    

            
