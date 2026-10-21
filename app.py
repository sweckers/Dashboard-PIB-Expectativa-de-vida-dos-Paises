import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Panorama Demográfico e Econômico Global', layout='wide'
)

st.title('Panorama Demográfico e Econômico Global')

arquivo = 'dds.csv'
if arquivo is not None:
  df = pd.read_csv(arquivo)
  df = df.drop_duplicates()

  df['População (Bilhões/Milhões)'] = pd.to_numeric(
      df['População (Bilhões/Milhões)'], errors='coerce'
  )

  df['Expectativa de Vida'] = pd.to_numeric(
      df['Expectativa de Vida'], errors='coerce'
  )

  df['PIB Nominal'] = pd.to_numeric(df['PIB Nominal'], errors='coerce')

  st.subheader('Visualização dos dados')
  st.dataframe(df.head())

  col1, col2 = st.columns(2)
  col1.metric('Quantidade de Países', df['País'].nunique())
  col2.metric('Quantidade de informações obtidas', df.shape[1])

  País = df['País'].dropna().unique().tolist()
  opcoes = ['Todos'] + País

  st.sidebar.header('Filtros para País específico')
  País_escolhido = st.sidebar.selectbox('País:', opcoes)

  População_mínima = st.sidebar.slider(
      'Mínimo de População (Bilhões/Milhões):', 0.0, 1428.6, 0.0
  )

  if País_escolhido == 'Todos':
    df_filtrado = df.copy()
  else:
    df_filtrado = df[df['País'] == País_escolhido]

  df_filtrado = df_filtrado[
      df_filtrado['População (Bilhões/Milhões)'] >= População_mínima
  ]

  st.subheader('Dados filtrados')
  st.dataframe(df_filtrado)

 
  grafico_pop = px.bar(
      df_filtrado,
      x='País',
      y='População (Bilhões/Milhões)',
      title='Taxa de População por País',
  )
  st.plotly_chart(grafico_pop, use_container_width=True)


  grafico_vida = px.bar(
      df_filtrado,
      x='País',
      y='Expectativa de Vida',
      title='Expectativa de vida por País',
  )

  grafico_pib = px.bar(
      df_filtrado, x='País', y='PIB Nominal', title='PIB Nominal por País'
  )

  st.plotly_chart(grafico_pib, use_container_width=True)
  st.plotly_chart(grafico_vida, use_container_width=True)

  
  grafico_disp = px.scatter(
      df_filtrado,
      x='PIB Nominal',
      y='Expectativa de Vida',
      size='População (Bilhões/Milhões)',
      color='País',
      hover_name='País',
      log_x=True,
      size_max=60,
      title='PIB × Expectativa de vida (tamanho = população)',
  )
  st.plotly_chart(grafico_disp, use_container_width=True)

 
  st.title('Não sabe o que é PIB?')
  st.markdown('Colocamos um vídeo explicando o que é um PIB para você!')
  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.video('https://youtu.be/GJ4Ey9JcXiI?si=aNxDncgrfjCUWsNW')