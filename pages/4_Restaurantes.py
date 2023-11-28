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

st.set_page_config(page_title='Visão Restaurantes', page_icon='🏬', layout='wide') 

# ==================================================
# Funções
# ==================================================
def rest_reserv_aval(df1):
    """ Está função tem a responsabilidade de preenchimento dos nome melhores restaurantes. 
        Conteúdo:
        1- colocar o nome dos restaurantes que aceitam reservas e com isso possuem o maior valor médio de um prato pra duas pessoas.
    """              
    df2=(df1[['has_table_booking', 'average_cost_for_two']].groupby('has_table_booking').mean().round(2)
        .sort_values('average_cost_for_two', ascending=False).reset_index())

    fig=(px.bar(df2, x='has_table_booking', y='average_cost_for_two', text_auto=True, labels={'has_table_booking': 'Restaurantes', 'average_cost_for_two':'Custo'}))

    fig.update_traces(textfont_size=12, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black')
    
    st.plotly_chart(fig, use_container_width=True)
    
    return fig   


def ped_online_aval(df1):
    
    """ Está função tem a responsabilidade de preenchimento dos nome melhores restaurantes. 
        Conteúdo:
        1- colocar o nome dos restaurantes que aceitam pedido online e são os que tem as maiores avaliações.
    """              
    df2 = (df1[['has_online_delivery', 'votes']].groupby('has_online_delivery').mean().round(2)
          .sort_values('votes', ascending=False).reset_index())

    fig = px.bar(df2, x='has_online_delivery', y='votes',text_auto=True, labels={'has_online_delivery': 'Restaurantes', 'votes':'Avaliações'})

    fig.update_traces(textfont_size=12, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black')
    
    st.plotly_chart(fig, use_container_width=True)
    
    return fig   
      

def  rest_cul_brasil(df1): 
    
    """ Está função tem a responsabilidade de preenchimento dos nome melhores restaurantes. 
        Conteúdo:
        1- colocar o nome dos 10 Melhores restaurantes de culinária brasileira do Brasil com maior nota média.
    """              
    culinaria = df1['cuisines'] == 'Brazilian'  

    pais=df1['country'] == 'Brazil'

    colunas=['country', 'city', 'restaurant_name', 'cuisines', 'aggregate_rating']
        
    df2=(df1.loc [culinaria & pais, colunas].groupby(['city', 'restaurant_name', 'cuisines'])
            .agg({'aggregate_rating': 'mean', 'country': 'count'})
            .sort_values('aggregate_rating', ascending=False,)
            .reset_index()).head(10)
            
    fig=(px.line(df2, x='restaurant_name', y='aggregate_rating', text='aggregate_rating', 
                title='Os 10 melhores restaurantes de culinária brasileira do Brasil com maior nota média',  
                labels={'restaurant_name': 'Restaurantes', 'aggregate_rating': 'Nota Média'}))
    
    fig.update_traces(textposition='top right', textfont_color='black')     
        
    st.plotly_chart(fig, use_container_width=True)    
    
    return fig

        
def  rest_aval(df1):
    
    """ Está função tem a responsabilidade de preenchimento dos nome melhores restaurantes. 
        Conteúdo:
        1- colocar o nome dos 10 Melhores restaurantes com maior avaliação.
    """          
    colunas=['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines', 'aggregate_rating', 'votes']
        
    df2=(df1.loc [:,colunas].groupby(['votes', 'restaurant_name']).sum()
            .sort_values('votes', ascending=False)
            .reset_index()).head(10)
    
    fig=(px.bar(df2, x='restaurant_name', y='votes', color='country', title='Os 10 melhores restaurantes com maior avaliação', text_auto=True, 
    labels={'restaurant_name': 'Restaurantes', 'votes': 'Total de Avaliações', 'country': 'País'}))

    fig.update_traces(textfont_size=12, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black')
    
    st.plotly_chart(fig, use_container_width=True)
    
    return fig

        
def melh_rest(df1):  
    
    """ Está função tem a responsabilidade de preenchimento dos nome melhores restaurantes. 
        Conteúdo:
        1- colocar o nome dos 10 Melhores restaurantes base no código dos restaurantes.
    """          
    st.write('##### Os 10 Melhores restaurantes')

    colunas=['restaurant_name', 'country', 'city', 'aggregate_rating', 'votes']

    df2=(df1.loc [:, colunas].groupby(['restaurant_name'])
            .max().sort_values('aggregate_rating', ascending=False)
            .reset_index()).head(10)

    st.dataframe(df2, use_container_width=700, height=379)
    
    return df2
    
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

paises =st.sidebar.multiselect(
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
st.markdown('## Visão de Negócio - Restaurantes')
st.subheader('', divider='gray') 

st.subheader('Informações úteis para tomadas de decisões de negócio com base nos restaurantes:')
st.subheader('', divider='gray')
 
with st.container():
    melh_rest(df1)

st.subheader('', divider='gray')
 
with st.container():
    rest_aval(df1)
       
st.subheader('', divider='gray')   
 
with st.container():
    rest_cul_brasil(df1)
         
st.subheader('', divider='gray')   

with st.container():
    col1, col2=st.columns(2, gap='small')
    
    with col1:
        st.markdown('###### Restaurantes que aceitam pedidos on-line tem maiores avaliações')
        ped_online_aval(df1)
        
    with col2:
        st.write('###### Restaurantes que aceitam reservas, possuem o maior valor médio de um prato para duas pessoas')
        rest_reserv_aval(df1)