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

st.set_page_config(page_title='Visão Cidades', page_icon='🏙', layout='wide') 

# ==================================================
# Funções
# ==================================================
def ped_online(df1):      
    
    """ Está função tem a responsabilidade de preenchimento das cidades com maior quantidade de pedidos on-line. 
        Conteúdo:
        1- colocar o nome dos restaurantes registrados com maior quantidade de pedidos on-line com base no código de cadas cidades.
    """                       
    media_acima=df1['has_online_delivery'] == 1

    df2=(df1.loc[media_acima, ['city','country', 'restaurant_id']].groupby(['city','country','restaurant_id'])
                .count().reset_index())

    df3=(df2.loc[:,['city','country', 'restaurant_id']].groupby(['city','country'])
            .count().sort_values('restaurant_id', ascending=False ).reset_index())

    fig=(px.bar(df3, x='city', y='restaurant_id', title='Cidades com maior quantidade pedidos on-line',text_auto=True, color='country', 
    labels={'restaurant_id':'Quantidade de Restaurantes', 'city':'Cidades', 'country' : 'País'}))

    fig.update_traces(textfont_size=10, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black') 
    
    return fig

    
def qnt_ent(df1):
    
    """ Está função tem a responsabilidade de preenchimento das cidades com maior quantidade de entregas. 
        Conteúdo:
        1- colocar o nome dos restaurantes registrados com maior quantidade de entregas com base no código de cadas cidades.
    """                
    media_acima=df1['is_delivering_now'] == 1

    df2=df1.loc[media_acima, ['city','country', 'restaurant_id']].groupby(['city','country','restaurant_id']).count().reset_index()

    df3=(df2.loc[:,['city','country', 'restaurant_id']].groupby(['city','country'])
            .count().sort_values('restaurant_id', ascending=False ).reset_index())

    fig=(px.bar(df3, x='city', y='restaurant_id', title='Cidades com maior quantidade de entregas',text_auto=True, color='country', 
    labels={'restaurant_id':'Quantidade de Restaurantes', 'city':'Cidades', 'country' : 'País'}))

    fig.update_traces(textfont_size=10, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black') 
    
    return fig


def faz_rev(df1):
    
    """ Está função tem a responsabilidade de preenchimento dos melhores restaurantes por cidades que fazem reservas. 
        Conteúdo:
        1- colocar o nome dos restaurantes registrados com médis acima de 2.5 com base no código de cada cidades.
    """            
    reservas=df1['has_table_booking'] ==1
    
    df2=(df1.loc[reservas, ['city','country', 'restaurant_id']].groupby(['city', 'country', 'restaurant_id'])
             .count().reset_index())

    df3=(df2.loc[:,['city', 'country', 'restaurant_id']].groupby(['city', 'country'])
            .count().sort_values('restaurant_id', ascending=False ).reset_index())

    fig=(px.bar(df3, x='city', y='restaurant_id', title='Melhores restaurantes por cidades que fazem reservas',text_auto=True, color='country', 
    labels={'restaurant_id':'Quantidade de Restaurantes', 'city':'Cidades', 'country' : 'País'}))

    fig.update_traces(textfont_size=10, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black') 
    
    return fig


def   med_acima2 (df1):
        
    """ Está função tem a responsabilidade de Ppreenchimento da quantidade 8 melhores restaurantes na média de avaliação acima 2.5. 
        Conteúdo:
        1- colocar o nome dos restaurantes registrados com médis acima de 2.5 com base no código de cada cidades.
    """            
    media_acima=df1['aggregate_rating'] >=2.5

    df2=df1.loc[media_acima, ['city','country', 'restaurant_id']].groupby(['city','country','restaurant_id']).count().reset_index()

    df3=(df2.loc[:,['city','country', 'restaurant_id']].groupby(['city','country'])
            .count().sort_values('restaurant_id', ascending=False ).reset_index()).head(8)

    fig=(px.bar(df3, x='city', y='restaurant_id', title='8 Melhores restaurantes na média de avaliação acima 2.5',text_auto=True, color='country', 
    labels={'restaurant_id':'Quantidade deRrestaurantes', 'city':'Cidades', 'country' : 'País'}))

    fig.update_traces(textfont_size=10, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black') 

    return fig


def   med_acima4 (df1):
    
    """ Está função tem a responsabilidade de preenchimento da quantidade 8 melhores restaurantes na média de avaliação acima 4.0. 
        Conteúdo:
        1- colocar o nome dos restaurantes registrados com médis acima de 4.0 com base no código de cada cidades.
    """            
    media_acima=df1['aggregate_rating'] >= 4.0

    df2=(df1.loc[media_acima, ['city','country', 'restaurant_id']]
            .groupby(['city','country','restaurant_id']).count().reset_index())

    df3=(df2.loc[:,['city','country', 'restaurant_id']].groupby(['city','country'])
            .count().sort_values('restaurant_id', ascending=False ).reset_index()).head(8)

    fig=(px.bar(df3, x='city', y='restaurant_id', title='8 Melhores restaurantes na média de avaliação acima 4.0',text_auto=True, color='country', 
    labels={'restaurant_id':'Quantidade de Restaurantes', 'city':'Cidades', 'country' : 'País'}))

    fig.update_traces(textfont_size=10, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black') 
    
    return fig
    

def qnt_rest_cid (df1):
    
    """ Está função tem a responsabilidade de preenchimento da quantidade de restaurantes registradas por cidades. 
        Conteúdo:
        1- colocar o nome dos restaurantes registrados com base no código de cada cidades.
    """        
    df2=(df1.loc[:,['city','restaurant_id','country']].groupby(['city','restaurant_id','country'])
            .count().reset_index())

    df3=(df2.loc[:,['city','restaurant_id','country']].groupby(['city', 'country' ])
            .count().sort_values('restaurant_id', ascending=False ).reset_index())

    fig=(px.bar(df3, x='city', y='restaurant_id',color='country', title='Quantidade de restaurantes registrados por cidades', text_auto=True, 
    labels={'restaurant_id': 'Total de Restaurantes', 'city': 'Cidades', 'country': 'País'}))

    fig.update_traces(textfont_size=10, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black')  
    
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
    default=["Brazil", "Canada", "Indonesia", "New Zeland", "Philippines", "Qatar", "South Africa", "United Arab Emirates" ])

st.sidebar.subheader('', divider='gray')
st.sidebar.subheader('Powered by: Jadson N Santos')

#Filtro de Países
todos_paises=df1['country'].isin(paises) 
df1=df1.loc[todos_paises, :]

# ==================================================
# Layout no Streamliy
# ==================================================
st.title('Visão de Negócio - Cidades')
st.subheader('', divider='gray') 

st.subheader('Informações úteis para tomadas de decisões de negócio com base nas cidades:')
st.subheader('', divider='gray')

with st.container():
    fig=qnt_rest_cid(df1)
    st.plotly_chart(fig, use_container_width=True)
        
st.subheader('', divider='gray')

with st.container():
    col1, col2=st.columns(2)
        
    with col1:        
        fig=med_acima4(df1)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2: 
        fig=med_acima2(df1)
        st.plotly_chart(fig, use_container_width=True)   
           
st.subheader('', divider='gray')
        
with st.container():
    fig=faz_rev(df1)
    st.plotly_chart(fig, use_container_width=True)
    
st.subheader('', divider='gray')
    
with st.container():
    col1, col2=st.columns(2)
        
    with col1: 
        fig=qnt_ent(df1)
        st.plotly_chart(fig, use_container_width=True)   
        
    with col2:
        fig=ped_online(df1)
        st.plotly_chart(fig, use_container_width=True) 
     