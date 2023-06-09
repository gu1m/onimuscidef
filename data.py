# importando as bibliotecas necessarias para realização da analise
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
import statistics as sts

# OBS: o tratamento de dados foi feito no arquivo do jupyternotebook e foi visto que nenhum dados estava NaN e nenhum dos dados estava duplicado ou representados de forma errada 
# para melhor aproveitamento das informações apresentadas anteriormente baixe o arquivo do jupyternotebook


# importando o arquivo csv 
dataset = pd.read_csv("Spotify.csv")


# deixando o front do app com uma interface amigave1
st.set_page_config(
    page_title="Dataframe Spotify",
    page_icon="bar_chart:",
    layout="wide"
    
)
st.header("Dataframe Spotify")

st.markdown("""---""")

# fazendo uma sidebar para melhor visualização dos dados

# primeiro item da sidebar (visualização dos dados individuais e gerais do dataframe)
opcoes = ["Geral","Individual"]
indi_geral = st.sidebar.selectbox("Escolha quais dados serão analisados", opcoes)

# aqui se o usuario tera que escolher entre Individual ou Geral no primeiro item da sidebar

# se o usuario digitar individual ira aparecer informações individuais 
if indi_geral == "Individual":
    
    # visualizando o total de musicas e artistas no dataframe
    total_musicas = len(dataset["track_name"])
    data = dataset.drop_duplicates(subset="artist_name", keep='first')
    total_artistas = len(data["artist_name"])

    # colocando na interface o numero de artistas e musicas no dataframe
    col1,col2,col3 = st.columns(3)
    col1.metric("Total de músicas", total_musicas)
    col3.metric("Número de artistas", total_artistas)
    
    # colocando area de digitação para o usuario digitar a musica ou o artista para ser analisado
    keyword = st.text_input("Digite o nome de um artista")
    clicado = st.button("search")
    st.markdown("""---""")
    
    # verificando se há algo escrito no espaço para digitar
    if keyword is not None and len(str(keyword)) > 0:
        # se o usuario escolher para analisar musica
        dado = dataset.loc[dataset["track_name"].isin ([keyword])]  
        # se o usuario escolher para analisar artista
        
         
        st.header("Dados Individuais do Artista Selecionado")

        st.write("Artista pesquisado")
            
        dado = dataset.loc[dataset["artist_name"].isin ([keyword])]
            
        if dado.empty:
            st.subheader("Cantor não catalogado")
        else:
                
            dado = dataset.loc[dataset["artist_name"].isin ([keyword])]
            st.write(dado)

            # realizando as estatisicas do artista 
            media_pop = round(sts.mean(dado["popularity"]),2)
            media_ene = round(sts.mean(dado["energy"]),2)
            moda_mode = sts.mode(dado["mode"])

            # deixando a interface mais amigavel
            col10,col22,col33 = st.columns(3)
            col10.metric("Média de Popularidade do Artista", media_pop)
            col22.metric("Média de Energia", media_ene)
            col33.metric("Escala musical mais usada", moda_mode)

            col222 = st.columns(1)

            # vendo qual é o gênero mais utilizado pelo o artista
            moda_gen = sts.mode(dado["genres"])
            st.write("O gênero mais utilizado por este artista é:")
            st.write(moda_gen)

            st.markdown("""---""")

            # espaço para o usuario pesquisar uma música dentro dos dados do artista selecionado
            keyword2 = st.text_input("Digite o nome de uma música do artista selecionado")
            clicado2 = st.button("search ")

                # verificando se há algo escrito no espaço para digitar
            if keyword2 is not None and len(str(keyword2)) > 0:
                 # encontrando o nome da música nos dados do Artista
                dado_music = dado.loc[dado["track_name"].isin ([keyword2])]
                
                # se a música não estiver catalogada
                if dado_music.empty:
                    st.subheader("Música não catalogada")
                
                # se a música estiver catalogada 
                else:
                    st.write(dado_music)

                    # pegando as informações da música
                    pop_mu = sts.mode(dado_music["popularity"])
                    dance  = sts.mode(dado_music["danceability"])
                    genre = sts.mode (dado_music["genres"])

                    # deixando as informções mais visiveis para o usúario
                    col111,col222,col333 = st.columns(3)
                    col111.metric("A popularidade desta música é:", pop_mu)
                    col222.metric("A danceabilidade desta música é de:", dance)

                    with col333:
                        st.write("O gênero músical usado nesta música foi:")
                        st.write(genre)

            st.markdown("""---""")

            # Gráficos do artista 
            st.subheader("Gráficos e dados gerais do artista")



            # realizando os graficos individuais do artista
            data1 = dataset.loc[dataset["artist_name"].isin ([keyword])]

            # neste histograma pode-se perceber o numero de musicas em correlação a popularidade
            fig07 =px.histogram(data1, x="popularity", nbins=15)

            # neste plotbox pode ver a correlação de tempo ritmico e popularidade 
            fig08 = px.box(data1, x='time_signature', y='popularity', color='time_signature')

            # neste plotbox pode ver a correlação de tom e popularidade 
            fig09 = px.box(data1, x='key', y='popularity', color='key')

            #neste plotbox pode ver o modo muscial em correlação com a popularidade 
            fig10 = px.box(data1, x='mode', y='popularity', color='mode')

            # nesta matriz é apresentado a correlação entre os dados do dataframe
            fig11 = data1.corr(numeric_only = True)

            # aqui colocamos na variavel data1 a musica mais famosa do artista selecionado
            data1 = data1.nlargest(1, 'popularity')[["track_name","popularity"]]
            st.write("A música mais famosa do artista selecionado é", data1)

            st.markdown("""---""")
            #graficos em relação ao artista
            col0,col00 = st.columns(2)

            # aqui plotamos os graficos de fato no dashboard de forma organizada 
            with col0:
                fig07.update_layout(title='Relação ao número de músicas para cada popularidade')
                st.write(fig07)
                st.write("""O grafico a seguir analisa para cada popularidade o número de músicas presentes nela""")
                st.markdown("""---""")

            with col00:
                fig08.update_layout(title='Relação a Tempo ritmico e  Popularidade')
                st.write(fig08)
                st.markdown("""---""")

            col99, col90 = st.columns(2)

            with col99:
                fig09.update_layout(title='Relação a Tom e a Popularidade')
                st.write(fig09)
                st.markdown("""---""")

            with col90:
                fig10.update_layout(title='Relação entre o Modo musical e a Popularidade')
                st.write(fig10)
                st.markdown("""---""")   

            fig11.style.background_gradient(cmap='cividis')
            st.write("Matriz de Correlação entre os dados do Dataframe")
            st.write(fig11)
            st.write("""Este gráfico apresenta a dependência entre os dados do gráfico em relação a eles mesmos""")
            


# se o usuario escolher geral 
elif indi_geral == "Geral":
    # aqui apresentei o head do dataframe para o usuario visualizar os dados que estamos lidando
    st.header("Dados Gerais do Dataframe")
    # visualizando o total de musicas e artistas no dataframe
    total_musicas = len(dataset["track_name"])
    data = dataset.drop_duplicates(subset="artist_name", keep='first')
    total_artistas = len(data["artist_name"])

    # colocando na interface o numero de artistas e musicas no dataframe
    col1,col2,col3 = st.columns(3)
    col1.metric("Total de músicas", total_musicas)
    col3.metric("Número de artistas", total_artistas)
    
    
    
    st.write("""Amostra de Dados""")
    st.write(dataset.head())
    
    col999, col000 =st.columns(2)
    
    with col999:
        # vendo qual o artista mais popular no dataframe
        st.write("""Música mais popular:""")
        dataset.nlargest(1, 'popularity')[['track_name','artist_name',"popularity"]]
    
    with col000:
        # vendo qual gênero músical mais presente no Dataframe
        moda_genre = sts.mode(dataset["genres"])
        st.write("Gênero mais popular:")
        st.write(moda_genre)

    st.markdown("""---""")
    # começando a plotar os graficos
    col01, col02 = st.columns(2)
   
    # O primeiro grafico representa a relação de popularidade com o numero de músicas presentes no dataframe
    with col01:
        fig06 =px.histogram(dataset, x="popularity")
        fig06.update_layout(title='Relação ao número de músicas para cada popularidade')
        st.write(fig06)
        st.write("""O grafico a seguir analisa para cada popularidade o número de músicas presentes nela""")
        st.markdown("""---""")

    # O segundo grafico apresenta a correlção entre o tempo ritmico e a popularidade da música
    with col02:
        fig = px.box(dataset, x='time_signature', y='popularity', color='time_signature')
        fig.update_layout(title='Correlação entre Tempo ritmico e Popularidade')
        fig.show()
        st.write(fig)
        st.markdown("""---""")
        
    
    # O Terceiro grafico apresenta a correlação entre o tom e a popularidade
    col03, col04 = st.columns(2)

    with col03:
        fig2 = px.box(dataset, x='key', y='popularity', color='key')
        fig2.update_layout(title='Correlação entre o tom e Popularidade')
        fig2.show()
        st.write(fig2)
        st.markdown("""---""")

    # O quarto grafico apresenta a correlação entre o mode da música e a popularidade
    with col04:
        fig3 = px.box(dataset, x='mode', y='popularity', color='mode')
        fig3.update_layout(title='Correlação entre Modo musical e Popularidade')
        fig3.show()
        st.write(fig3)
    
        st.markdown("""---""")
    col756, col456 = st.columns(2)
    # O quinto grafico apresenta a correlação entre a escala/ e a popularidade
    with col756:
        fig4 = px.box(dataset, x='mode', y='popularity', color='key')
        fig4.update_layout(title='Correlação entre Escala/tom e Popularidade')
        fig4.show()
        st.plotly_chart(fig4)
        
    
    with col456:
        fig11 = dataset.corr(numeric_only = True)
        fig11.style.background_gradient(cmap='cividis')
        st.write("Matriz de Correlação entre os dados do Dataframe")
        st.write(fig11)
        st.write("""Este gráfico apresenta a dependência entre os dados do gráfico em relação a eles mesmos""")
        
       
    
