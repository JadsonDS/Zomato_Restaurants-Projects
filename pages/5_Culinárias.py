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

st.set_page_config(page_title='Visão Culinária', page_icon='🍲', layout='wide') 

# ==================================================
# Funções
# ==================================================
def pior_tip_culi(df1):
    
    """ Está função tem a responsabilidade de preenchimento piores tipos de culinárias por média de avaliação. 
        Conteúdo:
        1- Colocar o nome dos piores tipos de culinárias.
    """              
    filtro=df1['aggregate_rating'] <= 3.2
    
    df2=(df1.loc [filtro, ['cuisines', 'aggregate_rating']].groupby(['cuisines'])
            .max().sort_values('aggregate_rating', ascending=True).reset_index())
    
    df2=df2.head(restaurantes) 

    fig=(px.bar(df2, x='cuisines', y='aggregate_rating', color='cuisines',  text_auto=True,
    labels={'cuisines':'Tipos de Culinárias', 'aggregate_rating':'Média de valiação',}))
    
    st.markdown(f' #### Os {qtde_cul} piores tipos de culinárias')

    fig.update_traces(textfont_size=10, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black')
    
    st.plotly_chart(fig, use_container_width=True) 
    
    return fig
    

def melhs_tip_culi(df1):
    
    """ Está função tem a responsabilidade de preenchimento dos melhores tipos de culinárias por média de avaliação. 
        Conteúdo:
        1- Colocar o nome dos melhores tipos de culinárias.
    """              
    filtro=df1['aggregate_rating'] <= 4.9

    df2=(df1.loc [filtro, ['cuisines', 'aggregate_rating']].groupby(['cuisines'])
            .max().sort_values('aggregate_rating', ascending=False).reset_index())

    df2=df2.head(restaurantes) 

    fig=(px.bar(df2, x='cuisines', y='aggregate_rating', color='cuisines', text_auto=True,
    labels={'cuisines':'Tipos de Culinárias', 'aggregate_rating':'Média de Avaliação',}))

    st.markdown(f' #### Os {qtde_cul} melhores tipos de culinárias')

    fig.update_traces(textfont_size=10, textangle=1, textposition="outside", cliponaxis=False, textfont_color='black')

    st.plotly_chart(fig, use_container_width=True)
    
    return fig


def acet_ped_online_entre(df1):
    
    """ Está função tem a responsabilidade de Preenchimento dos Tipos de culinárias 
        Conteúdo:
        1- colocar o nome dos restaurantes que aceitam pedidos on-line e fazem entregas 
    """        
    st.write('#### Tipos de culinárias que aceitam pedidos on-line e fazem entregas')
    
    colunas=['country', 'city', 'cuisines', 'is_delivering_now', 'has_online_delivery', 'votes']

    entregas=(df1['has_online_delivery'] == 1) & (df1['is_delivering_now'] == 1)
        
    df2=(df1.loc [entregas, colunas].groupby(['cuisines']).count()
            .sort_values('is_delivering_now', ascending=False).reset_index())
    
    st.dataframe(df2, use_container_width=800, height=380)
    
    return df2

        
def melhs_culi(df1):
    
    """ Está função tem a responsabilidade de Preenchimento dos Tipos de culinárias 
        Conteúdo:
        1- colocar o nome das Maiores culinárias com preço médio de um prato pra duas pessoas.
    """   
    st.write(f'#### As {qtde_cul} maiores culinárias com preço médio de um prato para duas pessoas\n')
        
    colunas=['city', 'country', 'average_cost_for_two', 'cuisines', 'currency']
        
    df2=(df1.loc [:,colunas].groupby(['country', 'city', 'cuisines', 'currency']).max()
            .sort_values('average_cost_for_two', ascending=False).reset_index()).head(qtde_cul)
    
    st.dataframe(df2, use_container_width=800, height=380)
    
    return df2

def mel_culi (df1, culinarias, top_n=5):
    
    """ Está função tem a responsabilidade de Preenchimento dos Tipos de culinários
        Conteúdo:
        1- colocar o nome dos Tipos de culinários com melhor avaliação.
    """       
    culinaria=df1['cuisines'].isin(culinarias)

    colunas=['restaurant_id', 'restaurant_name', 'aggregate_rating', 'cuisines', 'country', 'city', 'currency', 'average_cost_for_two']
            
    df2=(df1.loc [culinaria, colunas].groupby(['restaurant_id', 'restaurant_name'])
            .max().sort_values('aggregate_rating', ascending=False).reset_index())
    
    for index, row in df2.iterrows():
        
     st.metric(label=f'{row["cuisines"]}:', 
                    value=f'{row["aggregate_rating"]}/5.0',
                    help=f"""
                    Nome do Restaurante:{row["restaurant_name"]}\n
                    País:{row["country"]}\n 
                    Cidade:{row["city"]},\n
                    Preço para duas pessoas: {row["currency"]}{row["average_cost_for_two"]} 
                    """)
     
     return index
    

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
df=pd.read_csv('../dataset/zomato.csv')

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

paises = st.sidebar.multiselect(
    "Selecione o  país:",
    df1.loc[:, "country"].unique().tolist(),    
    default=["Australia", "Brazil", "England", "India", "South Africa", "United States of America"])


st.sidebar.subheader('', divider='gray')
st.sidebar.subheader('Selecione as quantidades de culinárias que deseja visualizar:')
qtde_cul = st.sidebar.slider("Selecione a quantidade:", 0, 165, 10)

st.sidebar.subheader('', divider='gray')
st.sidebar.subheader('Selecione os tipos de culinárias que deseja visualizar:')

culinaria = st.sidebar.multiselect(
    "Escolha o tipo de culinária:",
    df1.loc[:, "cuisines"].unique().tolist(),
    default=['American', 'Arabian', 'Brazilian', 'Burger', 'Coffee', 'Ice Cream', 'European', 'Italian', 'Japanese', 'Mexican', 'Pizza' ])
 

st.sidebar.subheader('', divider='gray')
st.sidebar.subheader('Powered by: Jadson N Santos')

#Filtro de Países
todos_paises=df1['country'].isin(paises) 
df1=df1.loc[todos_paises, :]

#Filtro Culinária
culinaria1=df1["cuisines"].isin(culinaria) 
df1=df1.loc[culinaria1, :]


restaurantes=qtde_cul


# ==================================================
# Layout no Streamliy
# ==================================================
st.markdown('## Visão de Negócio - Culinária')
st.subheader('', divider='gray') 

st.subheader('Informações úteis para tomadas de decisões de negócio com base nos tipos de culinária:')
st.subheader('', divider='gray')

st.markdown('#### Avaliações dos principais tipos culinários')


with st.container():
    col1, col2, col3, col4, col5=st.columns(5, gap='small')
    
    with col1:
       mel_culi(df1, culinarias=['Italian'])

    with col2:
       mel_culi(df1, culinarias=['American'])
               
    with col3:
        mel_culi(df1, culinarias=['Arabian'])
        
    with col4:
        mel_culi(df1, culinarias=['Japanese'])
           
    with col5:
        mel_culi(df1, culinarias=['Brazilian'])
        
st.subheader('', divider='gray')    
    

with st.container():
    melhs_culi(df1)
        
st.subheader('', divider='gray')  
      

with st.container():
    acet_ped_online_entre(df1)     
    
st.subheader('', divider='gray') 
               
               
with st.container():
    melhs_tip_culi(df1)

st.subheader('', divider='gray')            
with st.container():
    pior_tip_culi(df1)    
            
            
            
            
            
            
            









