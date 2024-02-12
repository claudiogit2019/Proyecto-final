<p align='center'>
<img src ="https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png">
<p>

<h1 align='center'>
 <b>PROYECTO FINAL</b>
</h1>

# <h1 align="center">**`TYelp y Google Maps`**</h1>

¡Bienvendios a la explarción de los datos de Yelp y Google Maps para desarrollar un sistema de recomendación;
	Descubre nuestro análisis detallado, objetivos y avances en este repositorio colaborativo!
<p align='center'>
<img src="assets\imgGY.jpg"  height=300>
<p>

## PROYECTO FINAL: DEMO 1 

### **Contexto:**

La proliferación de plataformas de reseñas, como Yelp y Google Maps, ha convertido la retroalimentación de los usuarios en un recurso valioso para las empresas. La reputación en línea juega un papel crucial en la toma de decisiones de los consumidores, especialmente en la industria de restaurantes y servicios relacionados con el turismo. El cliente, parte de un conglomerado de empresas de este sector, busca aprovechar estos datos para obtener una comprensión profunda de la percepción del usuario y utilizarla estratégicamente en la expansión y mejora de sus negocios.

### **Problema a Resolver:**

La empresa enfrenta el desafío de analizar y comprender las opiniones de los usuarios en plataformas clave, Yelp y Google Maps, sobre restaurantes, hoteles y negocios relacionados en el mercado estadounidense. Este análisis debe incluir la predicción de tendencias en diferentes sectores y la identificación de oportunidades y áreas de mejora.
La propuesta incluirá el uso de técnicas de Procesamiento de Lenguaje Natural (NLP) para analizar las reseñas de manera efectiva, y la implementación de modelos de machine learning para la clasificación y predicción.

### **Objetivos:**

- *Realizaremos predicciones con el modelo machine learning para la apertura de nuevos locales en ubicaciones estrategicas, asegurando asi un crecimiento efectivo y sostenible del negocio.*

- *Implementaremos un modelo de machine learning para impulsar la visibilidad y afluencia en sus locales. Este sistema generará recomendaciones personalizadas, beneficiando a los propietarios al aumentar la clientela y los ingresos.*

### **Alcance:**

- *Recopilación y depuración de datos de Yelp y Google Maps.*
- *Creación de un DataWarehouse para integrar datos de diferentes fuentes.*
- *Análisis de sentimientos utilizando NLP.*
- *Desarrollo e implementación de modelos de machine learning para la clasificación y predicción.*
- *Identificación de tendencias en rubros de negocios.*
- *Incorporación de datos adicionales, como cotizaciones en bolsa y tendencias en redes sociales.*
- *Implementación de campañas de marketing específicas.*
- *Integración con sistemas de gestión empresarial (ERP) para un análisis más amplio.*


### **Enfoque:**

- *Desarrollar un sistema de recomendación para los usuarios basado en sus experiencias pasadas y preferencias.*
- *Optimizar la experiencia del usuario al proporcionar recomendaciones personalizadas y relevantes.*
- *Implementar modelos de machine learning para la clasificación y predicción de preferencias de usuarios.*
- *Desarrollar un sistema de recomendación que utilice los resultados del análisis de sentimientos y los modelos de machine learning para proporcionar sugerencias personalizadas.*

`KPIs`
### _**Métrica: Índice de Satisfacción al Cliente.**_
Mide la proporción de reseñas positivas en comparación con el total de reseñas mensuales.
- *KPI: Un objetivo del incremento de un 7% del índice de satisfacción al cliente del mes actual respecto del mes anterior.
  Nos indicaría el esfuerzo continuo por mejorar la satisfacción del cliente de Yelp.*

### _**Metrica: Índice de Sentimiento Positivo.**_
Refleja el promedio de calificaciones en estrellas de negocios en Yelp anualmente:

- *KPI: Conseguir un índice de sentimiento positivo superior al 3.5 del año actual respecto del año anterior. 
  Esto sugiere que el negocio ha conseguido una estabilidad con un buen promedio de calificaciones.*
  
### _**Métrica: Total de reviews.**_
Mide la cantidad de reviews anuales:

- *KPI: Un objetivo del incremento de un 10% del total de reviews del año actual respecto del año anterior. 
  Significaría una mayor popularidad sobre los sitios del análisis.*

### _**Métrica: Índice de Sentimiento Positivo.**_
Mide la cantidad de negocios/franquicias por año:

- *KPI: Conseguir un incremento del 3% de la cantidad de negocios por Estado, del año actual respecto al año anterior. 
  Esto nos indicaría una mayor presencia de nuestras franquicias en el mercado.*

### _**Métrica: Calificación promedio.**_
Calificación promedio de las reviews por semestre:

- *KPI: Mejorar en un 5% la calificación promedio de los negocios de comida por Estado, del semestre actual respecto al semestre anterior*
  
### **Diagrama de Gantt**
<p align='center'>
<img src="assets\diagramaGantt.jpeg"  height=300>
<p>
	
### **Stack Tecnológico:**
- *Limpieza y Transformación de Datos:
Entorno de Desarrollo:
Google Colab (Python 3.0)
Lenguaje de Programación:
Python 3.0
Bibliotecas Python:
Pandas
NumPy
scikit-learn.*

  *Entorno Interactivo:
Jupyter Notebooks.*
- *Almacenamiento de Datos:
Almacenamiento en la Nube:
Google Cloud Storage.*
 *Bases de Datos:
  BigQuery (Google).*

- *Análisis Exploratorio de Datos (EDA):
Librerías de Visualización:
Matplotlib y Seaborn (Python).*

   *Herramientas de BI:
Power BI (Microsoft)
Google - Looker Studio.*

- *Versionado de Código y Repositorio:
Plataforma de Versionado de Código:
GitHub.*

- *Metodología de Trabajo:
Gestión de Proyectos:
Trello.*

- *Documentación:
Documentación Técnica y Presentaciones:
Markdown y Jupyter Notebooks.*

  *Documentación Formal:
Google Docs
Microsoft Word.*

  *README del Repositorio:
README de GitHub.*

### **MVP: OptiLocation**
`Objetivo del Producto:`  *Proporcionar una evaluación rápida de la viabilidad de abrir un restaurante en una ubicación específica utilizando datos estadísticos y características relevantes.*

`Características del MVP:`

*a. Entrada de Datos:*
- *Interfaz simple para que el usuario ingrese detalles sobre la ubicación, como código postal, tipo de vecindario, densidad de población, ingresos promedio, competencia cercana, etc.*
  
*b. Integración de Datos:*
- *Conectar con fuentes de datos públicas para obtener estadísticas demográficas, información sobre competidores locales, tasas de crecimiento poblacional, etc.*

*c. Modelo de Machine Learning:*
- *Implementar un modelo de machine learning simple que analice los datos de entrada y proporcione una puntuación de viabilidad para abrir un restaurante en esa ubicación.*
  
*d. Resultado:*
- *Mostrar una puntuación de viabilidad junto con un resumen de los factores clave que contribuyen a la decisión.*
  
*e. Retroalimentación del Usuario:*
- *Solicitar retroalimentación del usuario sobre la precisión de la evaluación y posibles características adicionales que podrían ser útiles.*
  
`Interfaz de Usuario:` *Una interfaz web simple que permita a los usuarios ingresar la información y visualizar los resultados.*

`Desarrollo Iterativo:` *Lanzar una versión inicial con características mínimas y recopilar comentarios de los usuarios para futuras mejoras.*

`Implementación del Modelo de Machine Learning:`
*Utilizar un modelo simple, como regresión logística, que considere factores clave para la viabilidad de un restaurante.
Este MVP proporciona una manera rápida y sencilla para que los emprendedores evalúen la viabilidad de abrir un restaurante en una ubicación específica. A medida que obtienes comentarios y validas la utilidad de la herramienta, puedes iterar y mejorar el producto.*

### **Link del video de la carga incremental:**

https://youtu.be/bP3isNH58Jo

### **Link del video Presentacion del Prototipo:**

https://www.youtube.com/watch?v=20UUY7rEC04
