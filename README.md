# Zomato Dashboard
![image](https://github.com/JadsonDS/Zomato_Restaurants-Projects/blob/main/logo.png)
### For the love of Food

# Sobre a Zomato
  A zomato é um serviço de busca de restaurantes e delivery, ela atua em diversos países da Ásia, Europa e alguns páises na américa,
   ela foi fundada em julho de 2008 com o intuito de ajudar os clientes a encontrarem restaurantes que atendessem suas necessidades, 
   se tornando um excelente lugar para empresas do segmento de restaurantes ficarem expostas para seus clientes, potencializando seus 
   resultados. 
   
# 1. Problema de negócio
O CEO recém contratado de uma renomada empresa de tecnologia do seguimento de marketplace de restaurantes deseja conhecer melhor o negócio da empresa, para que o mesmo tome as melhores decisões estratégicas visando alavancar ainda mais a companhia. Ele nos pediu então para criarmos um dashboard utilizando alguns dados históricos, onde o mesmo poderia acompanhar e responder algumas importantes questões para o negócio.

# 2. Premissas assumidas para a análise
  1. Os dados utilizados no estudo e construção deste dashboard foram disponibilizados na plataforma Kaggle, sendo assim, os dados 
   ficaram publicos para utilizá-los em suas analises. O link é: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv.     
   É importante salientar que a empresa Zomato cresceu e hoje atua em mais países e cidades além das apresentadas aqui.
  2. Marketplace foi o modelo de negócio assumido.
  3. As principais visões que podemos análisar com os dados divulgados são: Visão Geográfica, Visão Países, Visão Cidades, Visão Restaurantes e Visão Culinárias.

# 3. Estratégia da solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as principais visões do modelo de negócio da empresa:

Cada visão é representada pelo seguinte conjunto de métricas.
#### - Visão Geográfica: 
1. Informações úteis para análise geral e geográfica de negócio sobre:    
    - Quantos restaurantes únicos estão registrados?            
    - Quantos países únicos estão registrados?  
    - Quantas cidades únicas estão registradas?  
    - Qual o total de avaliações feitas?  
    - Qual o total de tipos de culinária registrados?
2. Mapa com a localização dos restaurantes por país.
   
#### - Visão Países:
1 Quantidade de restaurantes registrados por país;    
2 Quantidade de restaurantes registrados por país;    
3 Quantidade de cidades registradas por país;    
4 Média de avaliações feitas por país;    
5 Média de preço de um prato para duas pessoas por país;    
6 Quantidade de culinária distinta por país;    
7 Restaurantes que aceitam reservas por país.   

#### - Visão Cidades:     
1 Quantidade de restaurantes registrados por cidades;    
2 8 Melhores restaurantes na média de avaliação acima 4.0;    
3 8 Melhores restaurantes na média de avaliação acima 2.5;    
4 Melhores restaurantes por cidades que fazem reservas;    
5 Cidades com maior quantidade de entregas;    
6 Cidades com maior quantidade pedidos on-line.  

#### - Visão Restaurantes:               
1 Os melhores restaurantes;    
2 Os 10 melhores restaurantes com maior avaliação;    
3 Os 10 melhores restaurantes de culinária brasileira do Brasil com maior nota média;    
4 Restaurantes que aceitam pedidos on-line tem maiores avaliações;    
5 Restaurantes que aceitam reservas, possuem o maior valor médio de um prato para duas pessoas.  

#### - Visão Culinárias: 
1 Avaliações dos principais tipos culinários;    
2 As 10 melhores culinárias com preço médio de um prato para duas pessoas;      
3 Tipos de culinárias que aceitam pedidos on-line e fazem entregas;    
4 Os 10 melhores tipos de culinárias;    
5 Os 10 piores tipos de culinárias.  

# 4. Principais insights  
Dos 6929 restaurantes cadastrados na plataforma, 3110 estão na índia, o que significa que grande parte do faturamento do negócio está concentrado neste país. Além da expansão que pode acontecer no restante do mundo, visto que em apenas um país temos concentrado aproximadamente 45% restaurantes da plataforma, ou seja, existe muita área para cobrir no mundo.

A Inglaterra, Estados Unidos da América e Brasil, Canada possuem um custo médio de prato para 2 em sua moeda local, muito baixo quando comparado com os demais países além de possuirem grandes metrópoles e população, somado ao fato da expansão territorial do primeiro insight, devem ser os primeiros países a receberem investimentos buscando o crescimento da plataforma neles.





# 5 O produto final do projeto:
Um dashboard iterativo hospedado em cloud que está disponível para acesso de qualquer dispositivo com conexão à internet. Para acessá-los basta clicar no link a seguir: https://projects-zomato.streamlit.app/

# 6 Conclusão
Este projeto teve como objetivo a criação de um dashboard iterativo para auxiliar o CEO da empresa na tomada de decisões, de maneira simples e rápida. 
A Índia e sua culinária seguem sendo as mais populares no conjunto de dados da plataforma.
Territoriamente, existem muitas expansões possíveis para se fazerem, o novo CEO terá uma maior gama de informações e métricas relevantes sobre o negócio para elaborar uma reestruturação do planejamento de negócio que poderá levar a um outro patamar, tornando a Zomato como umas das maiores empresas no segmento dos marketplaces que atendem a restaurantes.

# 7 Próximo passos
1 Verificar outros dados da empresa, como, quantidade total de usuários, idade média dos usuários, % de homens e mulheres, tipos de culinárias preferidos por homens e mulheres, qual a idade média de quem prefere delivery.

2 Adicionar novas tabelas com as novas informações relevantes, adicionando novos filtros.

3 Adicionar novas visões do negócio, com essas novas conclusões, novas ações de marketing direcionado podem ser feitas.






