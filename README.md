# SRI-News
Information Recovery System Project
## Autores:
Marco Antonio Ochill Trujillo C-412

Kevin Majim Álvarez Ortega C-412

Jan Carlos Pérez González C-412

## Descripción del problema:
En la era digital actual, la cantidad de información disponible en línea es abrumadora, especialmente en el ámbito de las noticias. Para poder acceder y analizar eficientemente esta gran cantidad de información, es fundamental contar con un sistema automatizado que pueda extraer y estructurar los datos relevantes de los artículos de noticias. Esto permitirá a los usuarios obtener información clave de manera rápida y precisa.

El sistema requerido debe ser capaz de extraer información esencial de los artículos de noticias en línea. Esto incluye elementos como los titulares, los autores, la fecha de publicación, un resumen del contenido que no exceda las 5 oraciones, las entidades involucradas (como personas, organizaciones y países) y la propuesta de otras 3 noticias similares. Estos datos son fundamentales para comprender rápidamente el contenido y la relevancia de los artículos de noticias. 

## Consideraciones tomadas a la hora de desarrollar la solución:
Para la resolución del problema se tomaron noticias del siguiente dataset https://www.kaggle.com/datasets/rmisra/news-category-dataset. Además, para hacer más rápidas las consultas se preprocesan todos los artículos y se guardan en un .json con los campos necesarios de forma tal que cuando se inserte una consulta por donde se busque sea por los documentos procesados.

## Cómo ejecutar el proyecto?:
Por ahora en la terminal:

En Unix/Linux: ```python3 manage.py runserver```

En Windows: ```python manage.py runserver``` 

## Explicación de la solución desarrollada:





