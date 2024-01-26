import streamlit as st
import pandas as pd
from urllib.request import urlopen
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import json
import requests
from streamlit_lottie import st_lottie
import pydeck as pdk
import snowflake.connector
from google.cloud import bigquery
from google.oauth2 import service_account

#DISPOSICION
st.set_page_config(
    page_title="OptiLocation",
    layout="wide",
    initial_sidebar_state="expanded")

# EXTRACCION DE DATOS Y FUNCIONES 
st.markdown("""
<style>
.big-font {
    font-size:80px !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)


# REALIZA LA CARGA DE LOS ARCHIVOS CSV (DEBE SER MODIFICADA PARA QUE LEA EL BIG QUERY)
@st.cache_data
def pull_clean():
    master_zip=pd.read_csv('MASTER_ZIP.csv',dtype={'ZCTA5': str})
    master_city=pd.read_csv('MASTER_CITY.csv',dtype={'ZCTA5': str})
    return master_zip, master_city



#EJEMPLO PARA QUE PUEDA LEER EL BIG QUERY 

def pull_cleann():
    # Ruta al archivo JSON de la clave de la cuenta de servicio
    credentials_path = 'starlit-woods-407516-5b54cca76454.json'

    # Configura las credenciales para acceder a BigQuery
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=["https://www.googleapis.com/auth/bigquery"],
    )

    # Configura el cliente de BigQuery
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

#MENU DE OPCIONES 
with st.sidebar:
    selected = option_menu('OptiLocation', ["Introducción", 'Predicción','Acerca de'], 
        icons=['play-btn','search','info-circle'],menu_icon='intersect', default_index=0)
    lottie = load_lottiefile("webOptiLocation\similo3.json")
    st_lottie(lottie,key='loc')

#PAGINA DE INTRODUCCION
if selected=="Introducción":
    #Encabezado
    st.title('Bienvenido a OptiLocation')
    st.subheader('*Una herramienta nueva para poder realizar la predicción de donde puede aperturar un nuevo local*')

    st.divider()

    #Casos de Uso
    with st.container():
        col1,col2=st.columns(2)
        with col1:
            st.header('Casos de uso')
            st.markdown(
                """
                - _¿Realiza investigaciones de mercado para la expacion de franquicias?_
                - _¿Quiere aperturar una nueva sucursal, pero no sabe donde?_
                - _¿Desea apeturar un local pero tiene miedo a que no tenga una ubicacion estrategica?_

                """
                )
        with col2:
            lottie2 = load_lottiefile("webOptiLocation\place2.json")
            st_lottie(lottie2,key='place',height=300,width=300)

    st.divider()

    #VIDEO TUTORIAL
    st.header('Tutorial del uso')
    video_file = open('webOptiLocation\Similo_Tutorial3_compressed.mp4', 'rb')  # GRABAR UN VIDEO Y CAMBIARLO 
    video_bytes = video_file.read()
    st.video(video_bytes)
    
# PREDICCION
if selected=="Predicción":

    st.subheader('Seleccionar Ubucación')

    # REALIZA LA NORMALIZACION Y LIMPIEZA DE LOS DATAFRAMES
    master_zip,master_city=pull_clean()
    master_zip.columns = master_zip.columns.str.upper()
    master_zip = master_zip.rename(columns={'ZCTA5': 'ZIP'})
    master_zip['ZIP'] = master_zip['ZIP'].astype(str).str.zfill(5)
    master_city.columns = master_city.columns.str.upper()

    #CITYSTATE = ["ONE", "TWO", "THREE"]  # AQUI PONER LA QUERY PARA LOS ESTADOS

    # SELECCIONA (ZIP , CITY)
    loc_select=st.radio('Type',['City'],horizontal=True, label_visibility="collapsed")

    if loc_select=='City':
        city_select=st.selectbox(label='city',options=['City']+list(master_city['CITYSTATE'].unique()),label_visibility='collapsed')
        st.caption('Nota: La ciudad se agrega a la designación de USPS, que puede incluir ciudades/pueblos/municipios cercanos adicionales')


    with st.expander('Ajustes Avanzados'):

        st.subheader('Filtar Resultados')
        col1,col2=st.columns(2)
        states=sorted(list(master_city['STATE_LONG'].astype(str).unique()))
        state_select=col1.multiselect('Filtrar categorias',states)  #CATEGORIAS 

        count_select=col2.number_input(label='¿Cuántas ubicaciones similares regresaron? (1-3)',min_value=1,max_value=3,value=1,step=1)
        st.subheader('Importancia de la categoría de datos')
        st.caption('Valores más bajos = menor importancia, valores más altos = mayor importancia, valor predeterminado = 1,0')
        home_select=st.slider(label='Rating',min_value=0.1, max_value=2.0, step=0.1, value=1.0)
        work_select=st.slider(label='Categorias',min_value=0.1, max_value=2.0, step=0.1, value=1.0)
        environment_select=st.slider(label='Densidad de sitios',min_value=0.1, max_value=2.0, step=0.1, value=1.0)

    filt_master_zip=master_zip
    filt_master_city=master_city
    if len(state_select)>0:
        filt_master_zip=master_zip[master_zip['STATE_LONG'].isin(state_select)]
        filt_master_city=master_city[master_city['STATE_LONG'].isin(state_select)]



    #Benchmark
    if loc_select=='City':
        if city_select !='City':
            selected_record = master_city[master_city['CITYSTATE']==city_select].reset_index()
            selected_city=selected_record['CITYSTATE'][0]
            
            #Columns for scaling
            HomeCols_sc=['HH_SIZE_SC','PCT_OWN_SC','MED_HOME_SC','PCT_UNIT1_SC','PCT_UNIT24_SC']
            WorkCols_sc=['MEAN_COMMUTE_SC','PCT_WC_SC','PCT_WORKING_SC','PCT_SERVICE_SC','PCT_BC_SC']
            EnvironmentCols_sc=['PCT_WATER_SC','ENV_INDEX_SC','PCT_TOPARK_ONEMILE_SC','POP_DENSITY_SC','METRO_INDEX_SC']
            
            # Calculate the euclidian distance between the selected record and the rest of the dataset
            Home_dist               = euclidean_distances(filt_master_city.loc[:, HomeCols_sc], selected_record[HomeCols_sc].values.reshape(1, -1))
            Work_dist               = euclidean_distances(filt_master_city.loc[:, WorkCols_sc], selected_record[WorkCols_sc].values.reshape(1, -1))
            Environment_dist        = euclidean_distances(filt_master_city.loc[:, EnvironmentCols_sc], selected_record[EnvironmentCols_sc].values.reshape(1, -1))

            # Create a new dataframe with the similarity scores and the corresponding index of each record
            df_similarity = pd.DataFrame({'HOME_SIM': Home_dist [:, 0],'WORK_SIM': Work_dist [:, 0],'ENV_SIM': Environment_dist [:, 0], 'index': filt_master_city.index})

            weights=[home_select,work_select,environment_select]
            # Multiply column values with weights
            df_weighted = df_similarity.loc[:, ['HOME_SIM', 'WORK_SIM','ENV_SIM']].mul(weights)
            df_similarity['OVERALL_W']=df_weighted.sum(axis=1)/sum(weights)

            
            home_max=df_similarity['HOME_SIM'].max()
            work_max=df_similarity['WORK_SIM'].max()
            env_max=df_similarity['ENV_SIM'].max()
            overall_max=df_similarity['OVERALL_W'].max()

            
            df_similarity['HOME']    = 100 - (100 * df_similarity['HOME_SIM'] / home_max)
            df_similarity['WORK']    = 100 - (100 * df_similarity['WORK_SIM'] / work_max)
            df_similarity['ENVIRONMENT']     = 100 - (100 * df_similarity['ENV_SIM'] / env_max)
            df_similarity['OVERALL'] = 100 - (100 * df_similarity['OVERALL_W'] / overall_max)

            # Sort the dataframe by the similarity scores in descending order and select the top 10 most similar records
            df_similarity = df_similarity.sort_values(by='OVERALL_W', ascending=True).head(count_select+1)

            # Merge the original dataframe with the similarity dataframe to display the top 10 most similar records
            df_top10 = pd.merge(df_similarity, filt_master_city, left_on='index', right_index=True).reset_index(drop=True)
            df_top10=df_top10.loc[1:count_select]
            df_top10['Rank']=list(range(1,count_select+1))
            df_top10['Ranking']=df_top10['Rank'].astype(str)+'- '+df_top10['CITYSTATE']
            df_top10['LAT_R']=selected_record['LAT'][0]
            df_top10['LON_R']=selected_record['LON'][0]
            df_top10['SAVE']=False
            df_top10['NOTES']=''

            st.header('Top '+'{}'.format(count_select)+' Ubicaciones más similares')
            #st.write('You selected zip code '+zip_select+' from '+selected_record['County Title'][0])
            # CSS to inject contained in a string
            hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            tab1,tab2=st.tabs(['Map','Data'])
            with tab2:
                with st.expander('Expand for Table Info'):
                    st.markdown(
                    """
                    - The values for OVERALL, HOME, WORK, and ENVIRONMENT are scaled similarity scores for the respective categories with values of 0-100, where 100 represents a perfect match.
                    - Locations are ranked by their OVERALL score, which is a weighted average of the individual category scores.
                    - Save your research by checking locations in the SAVE column which will be added to csv for download.
                    """
                    )
                @st.cache_data
                def convert_df(df):
                    return df.to_csv().encode('utf-8')
                cols=['Rank','CITYSTATE','OVERALL','HOME','WORK','ENVIRONMENT']
                df=df_top10[cols+['SAVE','NOTES']]
                df=df.set_index('Rank')
                edited_df=st.experimental_data_editor(df)
                save=edited_df[edited_df['SAVE']==True]
                save=save.reset_index()
                csv = convert_df(save[cols+['SAVE','NOTES']])
                st.download_button(label="Download Selections as CSV",data=csv,file_name='SIMILO_SAVED.csv',mime='text/csv',)
            with tab1:
                latcenter=df_top10['LAT'].mean()
                loncenter=df_top10['LON'].mean()
                #map token for additional map layers
                token = "pk.eyJ1Ijoia3NvZGVyaG9sbTIyIiwiYSI6ImNsZjI2djJkOTBmazU0NHBqdzBvdjR2dzYifQ.9GkSN9FUYa86xldpQvCvxA" # you will need your own token
                #mapbox://styles/mapbox/streets-v12
                fig1 = px.scatter_mapbox(df_top10, lat='LAT',lon='LON',center=go.layout.mapbox.Center(lat=latcenter,lon=loncenter),
                                     color="Rank", color_continuous_scale=px.colors.sequential.ice, hover_name='CITYSTATE', hover_data=['Rank'],zoom=3,)
                fig1.update_traces(marker={'size': 15})
                fig1.update_layout(mapbox_style="mapbox://styles/mapbox/satellite-streets-v12",
                               mapbox_accesstoken=token)
                fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig1,use_container_width=True)

            st.divider()

            st.header('Prediccion de Ubicacion')
            rank_select=st.selectbox('Select from rankings above',list(df_top10['Ranking']))
            if rank_select:
                compare_record=df_top10[df_top10['Ranking']==rank_select].reset_index(drop=True)
                compare_city=compare_record['CITYSTATE'][0]
                #compare_county=compare_record['County Title'][0]
                compare_state=compare_record['STATE_SHORT'][0].lower()
                   
               

#About Page
if selected=='Acerca de':
    st.title('Datos')
    st.subheader('Todos los datos para este aplicativo se optuvieron de:')
    col1,col2,col3=st.columns(3)
    col1.subheader('Fuente')
    col2.subheader('Descripcion')
    col3.subheader('Link')
    with st.container():
        col1,col2,col3=st.columns(3)
        col1.write(':blue[Dataset de Google Maps]')
        col2.write('(                             )')
        col3.write('https://drive.google.com/drive/folders/1Wf7YkxA0aHI3GpoHc9Nh8_scf5BbD4DA?usp=share_link')
    
    with st.container():
        col1,col2,col3=st.columns(3)
        col1.write(':blue[Dataset de Yelp!]')
        col2.write('(                             )')
        col3.write('https://drive.google.com/drive/folders/1TI-SsMnZsNP6t930olEEWbBQdo_yuIZF?usp=sharing')

    st.divider()
    
    st.title('Creadores')
    with st.container():
        col1,col2,col3,col4,col5,col6=st.columns(6)
        col1.write('')
        col1.write('')
        col1.write('')
        col1.write('**Nombre:**    Mauricio David Figueroa')
        col1.write('**Especialidad:**    Machine Learning')
        col1.write('**Contacto:**   [GitHub](https://www.linkedin.com/in/kevin-soderholm-67788829/) or [linkedin](https://www.linkedin.com/in/kevin-soderholm-67788829/)')
        col1.image('webOptiLocation\fotografias\Claudio.png')
        col2.write('')
        col2.write('')
        col2.write('')
        col2.write('**Nombre:**    Antonio Claudio Ortiz')
        col2.write('**Especialidad:**    Machine Learning')
        col2.write('**Contacto:**   [GitHub](https://github.com/claudiogit2019?tab=repositories) or [linkedin](https://www.linkedin.com/in/antonio-claudio-ortiz-b4a6a41ba/)')
        col2.image('webOptiLocation\fotografias\Claudio.png')
        col3.write('')
        col3.write('')
        col3.write('')
        col3.write('**Nombre:**    Camila Ledesma')
        col3.write('**Especialidad:**     Data Analyst')
        col3.write('**Contacto:**   [GitHub](https://github.com/camiledesma) or [linkedin](https://www.linkedin.com/in/camila-ledesma-966bba1b1/)')
        col3.image('webOptiLocation\fotografias\Camila.png')
        col4.write('')
        col4.write('')
        col4.write('')
        col4.write('**Nombre:**    Jeferson Albornoz Peña')
        col4.write('**Especialidad:**    Data Analyst')
        col4.write('**Contacto:**    [GitHub](//https://github.com/Eljeferson) or [linkedin](https://www.linkedin.com/in/jeferson-albornoz-peña-5018831bb)')
        col4.image('OptiLocation\fotografias\Claudio.png')
        col5.write('')
        col5.write('')
        col5.write('')
        col5.write('**Nombre:**    Jhon Ever Gallego')
        col5.write('**Especialidad:**    Data Engineer')
        col5.write('**Contacto:**   [GitHub](https://github.com/jhonevergallegoate) or [linkedin](https://www.linkedin.com/in/jhonevergallegoate/)')
        col5.image('webOptiLocation\fotografias\Jhon.png')
        col6.write('')
        col6.write('')
        col6.write('')
        col6.write('**Nombre:**    Maria Andrea Soria')
        col6.write('**Especialidad:**    Data Analyst')
        col6.write('**Contacto:**   [GitHub](https://github.com/andreasoria2022) or [linkedin](https://www.linkedin.com/in/andrea-soria-86200b2b1/)')
        col6.image('webOptiLocation\fotografias\Andrea.png')
