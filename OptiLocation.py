import streamlit as st
from streamlit_option_menu import option_menu
import json
from streamlit_lottie import st_lottie
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

 
#Lectura del big query
def instanciar_client():
    # Ruta al archivo JSON de la clave de la cuenta de servicio
    credentials_path = 'webOptiLocation\starlit-woods-407516-5b54cca76454.json'
    # Configura las credenciales para acceder a BigQuery
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=["https://www.googleapis.com/auth/bigquery"],
    )
    # Configura el cliente de BigQuery
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    return client


# Obtener la media y desvio estandar para estandarizar nuestro input
def obtener_avg_stddev(client):
    QUERY = (
    'SELECT '
    'AVG(avg_rating) AS avg_rating_avg,'
    'STDDEV(avg_rating) AS avg_rating_stddev,'
    'AVG(num_of_reviews) AS num_of_reviews_avg,'
    'STDDEV(num_of_reviews) AS num_of_reviews_stddev,'
    'AVG(num_sitios) AS num_sitios_avg,'
    'STDDEV(num_sitios) AS num_sitios_stddev,'
    'FROM '
    '`modelo_knn.restaurantes_ml`'
    )

    # Necesario instalar en modulo pandas para bq
    # pip install google-cloud-bigquery[pandas]
    df = client.query_and_wait(QUERY).to_dataframe()
    return df

# Obtener las columnas de "restaurantes_ml_std"
def obtener_columnas(client):
    # Obtener las columnas de "restaurantes_ml_std"
    columnas = []

    QUERY = (
        'SELECT COLUMN_NAME '
        'FROM `starlit-woods-407516.modelo_knn.INFORMATION_SCHEMA.COLUMNS` '
        'WHERE TABLE_NAME = "restaurantes_ml_std"'
    )

    query_job = client.query(QUERY)
    result = query_job.result()

    for columna in result:
        columnas.append(columna[0])

    # Elimino el primer campo porque no se incluye en la predicción
    columnas.remove("gmap_id")
    columnas_dict = dict.fromkeys(columnas)
    return columnas_dict

def obtener_states(client):
    # Obtener las columnas de "states"
    states = []

    QUERY = (
            'SELECT state FROM `datawarehouse.states`'
            )

    query_job = client.query(QUERY)  # API request
    result = query_job.result()  # Waits for query to finish

    for state in result:
        states.append(state[0])

    return states

client = instanciar_client()

#MENU DE OPCIONES 
with st.sidebar:
    selected = option_menu('OptiLocation', ["Introducción", 'Predicción','Acerca de'], 
        icons=['play-btn','search','info-circle'],menu_icon='intersect', default_index=0)
    lottie = load_lottiefile("webOptiLocation/similo3.json")
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
            lottie2 = load_lottiefile("webOptiLocation/place2.json")
            st_lottie(lottie2,key='place',height=300,width=300)

    st.divider()

    #VIDEO TUTORIAL
    st.header('Tutorial del uso')
    video_file = open('webOptiLocation/Similo_Tutorial3_compressed.mp4', 'rb')  # GRABAR UN VIDEO Y CAMBIARLO 
    video_bytes = video_file.read()
    st.video(video_bytes)
    

# PREDICCION
if selected=="Predicción":

    st.subheader('Seleccionar Ubucación')

    # REALIZA LA NORMALIZACION Y LIMPIEZA DE LOS DATAFRAMES
    States = obtener_states(client)
    loc_select=st.radio('Type',['Estados'],horizontal=True, label_visibility="collapsed")
    if loc_select=='Estados':
        estado_select=st.selectbox(label='Estados',options=['Estados']+States,label_visibility='collapsed')
        
    Rating_options = [4, 4.5, 5]
    Rating = st.radio('Type', ['Rating'], horizontal=True, label_visibility="collapsed")
    if Rating == 'Rating':
        Rating_select = st.selectbox(label='Rating', options=['Rating'] + [str(option) for option in Rating_options], label_visibility='collapsed')
        st.caption('Nota: 4 = Bueno, 4.5 = Muy Bueno, 5 = Exelente')

    Densidad_Opcion = [1,2,3,4]
    Densidad_Sitios=st.radio('Type',['Densidad_Sitios'],horizontal=True, label_visibility="collapsed")
    if Densidad_Sitios=='Densidad_Sitios':
        Densidad_Sitios_select=st.selectbox(label='Densidad_Sitios',options=['Densidad_Sitios']+ [str(option) for option in Densidad_Opcion] ,label_visibility='collapsed')
        st.caption('Nota: 1 = Baja, 2 = Media, 3 = Alta, 4 = Muy Alta')

    # Elementos a excluir
    elementos_a_excluir = ['standardized_avg_rating', 'standardized_num_of_reviews', 'state', 'standardized_num_sitios']
    Categorias_options = obtener_columnas(client)
    # Eliminar categorias que no deben aparecer en la seleccion
    for elemento in elementos_a_excluir:
        if elemento in Categorias_options:
            del Categorias_options[elemento]
    selected_categories = st.multiselect('Selecciona Categorias', options = ['Categorias'] + list(Categorias_options.keys()), default=['Categorias'])
    st.caption('Nota: Se puede elegir varias categorias')


    with st.expander('Ajustes Avanzados'):

        st.subheader('Filtrar Resultados')
        count_select = st.number_input(label='¿Cuántas ubicaciones similares regresaron? (1-3)', min_value=1, max_value=3, value=1, step=1)

    def estandarizar(df_avg_stddev, Rating_select, Densidad_Sitios_select):
        if Densidad_Sitios_select == 1:
            Densidad_Sitios_select = 20
        elif Densidad_Sitios_select == 2:
            Densidad_Sitios_select = 80
        elif Densidad_Sitios_select == 3:
            Densidad_Sitios_select = 200
        elif Densidad_Sitios_select == 4:
            Densidad_Sitios_select = 500
        else:
            Densidad_Sitios_select = 50
        Rating_select = (Rating_select - df_avg_stddev["avg_rating_avg"])/df_avg_stddev["avg_rating_stddev"]
        Densidad_Sitios_select = (Densidad_Sitios_select - df_avg_stddev["num_sitios_avg"])/df_avg_stddev["num_sitios_stddev"]
        Rating_select = (Rating_select - df_avg_stddev["avg_rating_avg"].values[0])/df_avg_stddev["avg_rating_stddev"].values[0]
        Densidad_Sitios_select = (Densidad_Sitios_select - df_avg_stddev["num_sitios_avg"].values[0])/df_avg_stddev["num_sitios_stddev"].values[0]
        return Rating_select, Densidad_Sitios_select


    def cargar_datos(columnas_dict,Rating_select,Densidad_Sitios_select,estado_select,selected_categories):
        # Cargo los valores ingresados por el usuario
        columnas_dict["standardized_avg_rating"] = Rating_select
        columnas_dict["standardized_num_of_reviews"] = 0
        columnas_dict["standardized_num_sitios"] = Densidad_Sitios_select
        columnas_dict["state"] = f'"{estado_select}"'

        for categoria in selected_categories:
            columnas_dict[categoria] = 'true'

        for columna, valor in columnas_dict.items():
            if valor is None:
                columnas_dict[columna] = 'false'

        # Construye una sola expresión SELECT para todos los pares clave-valor
        columnas_select = ', '.join([f'{valor} AS {clave}' for clave, valor in columnas_dict.items()])

        return columnas_select


    def consultar_modelo_ml(client, columnas_select):
        QUERY = (
        'SELECT * FROM ML.PREDICT(MODEL `modelo_knn.modelo_clusterizacion`, '
        '(SELECT ' + columnas_select + '))'
        )

        # Necesario instalar en modulo pandas para bq
        # pip install google-cloud-bigquery[pandas]
        prediccion = client.query_and_wait(QUERY).to_dataframe()
        return prediccion
    
    def obtener_centroides(prediccion):
        # Utiliza apply para convertir los arrays de NumPy a listas y luego aplica json.loads
        centroid_ids = prediccion['NEAREST_CENTROIDS_DISTANCE'].apply(lambda x: [d['CENTROID_ID'] for d in x]).tolist()[0]
        return centroid_ids
    
    def cluster_mas_recomendado(client, centroid_ids):
        QUERY = (
        'SELECT cluster_id FROM `modelo_knn.predicted_clusters_2` '
        f'WHERE centroid_id = {centroid_ids[0]} AND state = "{estado_select}" '
        'ORDER BY avg_rating DESC'
        )

        clusters = client.query_and_wait(QUERY).to_dataframe()
        clusters = clusters["cluster_id"].tolist()
        # Elimino clusters duplicados
        clusters = list(dict.fromkeys(clusters))

        return clusters[0]
    
    def ubicacion_recomendacion(client, num_cluster):
        QUERY = (
        'SELECT centroide, state, num_sitios, avg_rating FROM `datawarehouse.clusters_restaurantes`'
        f'WHERE cluster_id = {num_cluster}'
        )

        centroide = client.query_and_wait(QUERY).to_dataframe()

        return centroide.values[0]
    
        # Deberia ir en el main

    cliente_bq = instanciar_client()
    df_estandarizar = obtener_avg_stddev(cliente_bq)
    #Rating_select, Densidad_Sitios_select = estandarizar(df_estandarizar, Rating_select, Densidad_Sitios_select)
    columnas_dict = obtener_columnas(cliente_bq)
    columnas_select = cargar_datos(columnas_dict,Rating_select,Densidad_Sitios_select,estado_select,selected_categories)
    prediccion = consultar_modelo_ml(cliente_bq, columnas_select)
    centroides = obtener_centroides(prediccion)
    num_cluster = cluster_mas_recomendado(cliente_bq, centroides)

    # Obtener ubicacion del cluster recomendado
    Ubicacion = ubicacion_recomendacion(cliente_bq, num_cluster)

    st.write('Prediccion:', Ubicacion)

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
        col2.write('(En este data set se ecuentran los datos con los cuales se fueron trabajando)')
        col3.write('https://drive.google.com/drive/folders/1Wf7YkxA0aHI3GpoHc9Nh8_scf5BbD4DA?usp=share_link')
    
    with st.container():
        col1,col2,col3=st.columns(3)
        col1.write(':blue[Dataset de Yelp!]')
        col2.write('(En este data set se ecuentran los datos con los cuales se fueron trabajando)')
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
        col1.write('**Contacto:**   [GitHub](https://github.com/maurifigueroa) or [linkedin](https://www.linkedin.com/in/mfigueroa15)')
        col1.image('webOptiLocation/fotografias/Mauricio.png')
        col2.write('')
        col2.write('')
        col2.write('')
        col2.write('**Nombre:**    Antonio Claudio Ortiz')
        col2.write('**Especialidad:**    Machine Learning')
        col2.write('**Contacto:**   [GitHub](https://github.com/claudiogit2019?tab=repositories) or [linkedin](https://www.linkedin.com/in/antonio-claudio-ortiz-b4a6a41ba/)')
        col2.image('webOptiLocation/fotografias/Claudio.png')
        col3.write('')
        col3.write('')
        col3.write('')
        col3.write('**Nombre:**    Camila Ledesma')
        col3.write('**Especialidad:**     Data Analyst')
        col3.write('**Contacto:**   [GitHub](https://github.com/camiledesma) or [linkedin](https://www.linkedin.com/in/camila-ledesma-966bba1b1/)')
        col3.image('webOptiLocation/fotografias/Camila.png')
        col4.write('')
        col4.write('')
        col4.write('')
        col4.write('**Nombre:**    Jeferson Albornoz Peña')
        col4.write('**Especialidad:**    Data Analyst')
        col4.write('**Contacto:**    [GitHub](//https://github.com/Eljeferson) or [linkedin](https://www.linkedin.com/in/jeferson-albornoz-peña-5018831bb)')
        col4.image('webOptiLocation/fotografias/Jeferson.png')
        col5.write('')
        col5.write('')
        col5.write('')
        col5.write('**Nombre:**    Jhon Ever Gallego')
        col5.write('**Especialidad:**    Data Engineer')
        col5.write('**Contacto:**   [GitHub](https://github.com/jhonevergallegoate) or [linkedin](https://www.linkedin.com/in/jhonevergallegoate/)')
        col5.image('webOptiLocation/fotografias/Jhon.png')
        col6.write('')
        col6.write('')
        col6.write('')
        col6.write('**Nombre:**    Maria Andrea Soria')
        col6.write('**Especialidad:**    Data Analyst')
        col6.write('**Contacto:**   [GitHub](https://github.com/andreasoria2022) or [linkedin](https://www.linkedin.com/in/andrea-soria-86200b2b1/)')
        col6.image('webOptiLocation/fotografias/Andrea.png')