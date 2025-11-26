import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide')

df = pd.read_csv('Ecommerce Geolocated.csv')


#------------------------------------------ SIDEBAR


st.sidebar.title('Amazon Ecommerce')
st.sidebar.image('logo.png')

paises= df['Country'].unique().tolist()
paises_escolhidos= st.sidebar.multiselect('Países',paises, paises)

df=df[df['Country'].apply(lambda x:x in paises_escolhidos)]



#-------------------------------------------- PRINCIPAL

with st.container():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True, height="stretch"):
            st.metric('Total de vendas', f'${df['Purchase Price']. sum():.0f}')

    with col2:
        with st.container(border=True, height="stretch"):
            st.metric('Total de Países', len(paises_escolhidos))

    with col3:
        with st.container(border=True, height="stretch"):
            st.metric('Total de Empresas',df['Company'].nunique())

    
    with col4:
        with st.container(border=True, height="stretch"):
            st.metric('Provedores de Crédito', df['CC Provider'].nunique())



with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True, height="stretch"):
            prices_country = df.groupby('Country').agg({'Purchase Price' : ['count', 'sum' ,'max', 'min', 'mean']}).reset_index()
            prices_country.columns = ['Country', 'Quantidade de Vendas', 'Total em Dólares', 'Preço Máximo', 'Preço Mínimo', 'Preço Médio']


            opcao = st.radio('Ranking por:', ['Quantidade de Vendas', 'Total em Dólares', 'Preço Máximo', 'Preço Mínimo', 'Preço Médio'],horizontal=True)


            prices_country = prices_country.sort_values(opcao, ascending=False).head()
            fig = px.bar(prices_country.sort_values(opcao, ascending=True), x=opcao, y='Country', orientation='h')


            st.markdown('##### Top 5 Países')
            st.plotly_chart(fig)
   
   
   
    with col2:
        with st.container(border=True, height="stretch"):
            df['Ano'] = df['CC Exp Date'].apply(lambda x: x.split('/')[1]).astype(int)


            df_aux = df.groupby(['Ano', 'Country'])['Purchase Price'].sum().reset_index().sort_values('Ano', ascending=True)
            fig = px.line(df_aux, x='Ano', y='Purchase Price', width=400, color='Country', markers=True)


            st.markdown('### Vendas por Ano')
            st.plotly_chart(fig)

    with col3:
        with st.container(border=True, height="stretch"):
            cc_providers = df.groupby('CC Provider')['Purchase Price'].sum().reset_index().sort_values('Purchase Price', ascending=False)
            
            st.markdown('##### Vendas por Provedor de Crédito')


            count = 1
            for i,j in zip(cc_providers['CC Provider'], cc_providers['Purchase Price']):
                st.markdown(f'{count}º - {i:20} - ${j:.2f}')
                count +=1


coordenadas = df[~(df['Latitude'].isna())]
st.map(coordenadas, latitude='Latitude', longitude='Longitude')