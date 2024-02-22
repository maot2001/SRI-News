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
Para comprender la solución desarrollada hay que dividirla en sus tres elementos teóricos más importantes:


### TF-IDF:
TF de una palabra(término) en un documento, está definido de la sieguiente manera:

```tf(t,d) = count of t in d / number of words in d ```

Esto lo que significa es el número de instancias de una palabra dada t en un docuemnto d (este número normalizado).

Para entender lo que significa __idf__ antes hay que entender lo que significa __df__. Y es que df es la cantidad de veces que aparece una palabra t en un cuerpo o conjunto de documentos:

```df(t) = count of t in documents```

Sabiendo esto, idf es principalmente cómo de relevante es una palabra y está dado por esta fórmula:

```idf(t) = log(N/df(t))```
#### Cómo se usa en el proyecto?
TF-IDF es una de las mejores métricas para determinar qué tan significante es un término dentro de un corpus. Asigna un peso a cada palabra en el documento basada en su __tf__ y la frecuencia recíproca del documento (__tf-idf__). Las palabras con más peso serán más relevantes.

Específicamente en este proyecto se usa para luego comparar las consultas con los textos, y esto se hace usando los vectores de tf-idf que proveé la biblioteca gensim. En el json están las palabras con su __idf__ calculado y cada documento a las que pertencen con el __tf-idf__ correctamente calculado.

Tiene un json con las palabras con su idf y los articulos los que pertence con su tf-idf

### Similitud del coseno:
La similitud del coseno es una medida de similitud que se calcula entre dos vectores distintos de cero dentro del espacio interno del producto que mide el coseno del ángulo entre ellos. 

### Cómo se usa en el proyecto?
En este proyecto se utiliza para comparar los vectores de __tf-idf__ de la consulta y los documentos, ya que la consulta se trata como un documento más.


### Latent Semantic Descomposition (LSA):
La Descomposición Semántica Latente (LSA) es una técnica en procesamiento de lenguaje natural que busca descubrir relaciones semánticas entre palabras y documentos. Utiliza una técnica matemática llamada Descomposición en Valores Singulares (SVD) para lograrlo.  

### Cómo se usa en el proyecto?
En este caso crea una matriz de oraciones*término, donde en cualquier posición está la importancia de esa palabra en la oración, y luego usando SVD factoriza la matriz de forma tal que captura la semántica y ordena las oraciones en cuánto a importancia en el texto, más tarde se decide el número de oraciones a mostrar, en este caso 5, y ese es el resultado.

## Insuficiencias de la solución y mejoras propuestas:
La solución está implementada de una manera para que dada una consulta está busque en más de un documento a la vez, pero hay que tener en cuenta que estos documentos ya están procesados y es con una base de datos determinada. Posiblemente esto sea una restricción si se quisiera usar esta funcionalidad en la vida real en línea, ya que el procesar muchas noticas es costoso en sí, por tanto realizarlo en un tiempo prudencial donde un usuario esté esperando una respuesta en línea con nuestra solución no es posible.




