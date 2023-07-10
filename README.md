# Proyecto 3 BD2

## Organización del equipo

|            Participante             |   Papel   |
|:-----------------------------------:|:---------:|
|  José Rafael Chachi Rodriguez       |  Backend  |
|    Joaquín Francisco Jordán O'Connor|  Backend  |
|     Juan Diego Castro Padilla       |  Backend / Frontend  |
|   Juan Diego Lareda Yarma           | Frontend  |

## Video explicativo

Link del video:
[https://drive.google.com/file/d/1crUT1CHy8CX1tj3TdSDlCxwQIOi75kNb/view?usp=sharing](https://www.youtube.com/watch?v=QB7ACr7pUuE)

## Introducción 
En este proyecto se nos ha pedido dar soporte a las búsquedas y recuperación eficientemente de datos multimedia, imágenes. Se utilizarán distintos algoritmos, además se apoyará de estructuras multidimensionales.

## Objetivos
### Principal
Aplicar los algoritmos de búsqueda y recuperación de la información para archivos multimedia aprendidos en clase.
### Secundarios
- Definir una forma de como se almacenará los datos de las imágenes en memoria secundaria.
- Crear una interfaz amigable para la realización de las consultas de imágenes.


## Descripción del dominio de datos
El dataset utilizado son rostros de personas famosas de cualquier profesión. Nótese que una imagen no necesariamente contiene el rostro de solo 1 persona.
El archivo zip contiene lo siguiente:

```markdown
|--- Aaron_Eckhart
|    |--- Aaron_Eckhart_0001.jpg
|
|--- Aaron_Guiel
|    |--- Aaron_Guiel_0001.jpg
...
...
...
```
Es una carpeta lleno con carpetas con los nombres de los rostros principales. Adicionalmente, dentro de cada carpeta existen entre 1 a más imágenes de rostro referentes al nombre de la carpeta.

Dataset extraído de [Face Data](http://vis-www.cs.umass.edu/lfw/).

## Librerías utilizadas

Una de nuestras principales librerías a utilizar es el **Face recognition**. Sin esta librería no se puede extraer el vector característico de una imagen con rostros.
Para realizar las operaciones con archivos multimedia, nos apoyamos de las siguientes librerías para realizar la búsqueda KNN.

### Heapq
- Estructura unidimensional.
- Los nodos del heap son las K imágenes más cercanas a la query.
- Se apoya de un heap para optimizar espacialmente la búsqueda secuencial KNN.

### RTree
- Estructura multidimensional.
- El RTree genera espacios de acceso multidimensional en donde almacena elementos semejantes a estos.
- En la búsqueda, se aplica un filtrado con respecto a estos espacios en las dimensiones del árbol.

### Faiss (LSH)
- Algoritmo de búsqueda de los vectores característicos más semejantes.
- Utiliza una familia de funciones hash. Intenta provocar colisiones en un mismo bucket.
- Almacena buckets no vacíos. Esto para hacer la búsqueda de los vectores en una complejidad menor a la lineal.

## Análisis de la maldición de la dimensionalidad y mitigación

El árbol-R es una estructura dimensional que agrupa sus elementos en distintos locaciones geográficas. Estas locaciones son fijadas de acuerdo a la dimensión indicada en el árbol. Es por ello que es recomendable
aumentar la cantidad de dimensiones del árbol-R para tener los elementos similares agrupados disjuntos. Sin embargo, existe una situación en que si la dimensión es un número demasiado grande, existen variadas locaciones en donde los elementos se agrupan. Si los elementos agrupados están dispersos, en el algoritmo de búsqueda de los elementos KNN no se aplicará un filtro prudente y esto ocasiona que nuestra búsqueda KNN en un
árbol-R sea similar en complejidad computacional a una búsqueda lineal. En otras palabras, hay que ir aumentando la dimensión del RTree para agilizar la búsqueda hasta un tamaño en donde la dimensión no sea excesiva y sea perjudicial.

Con esta limitación del árbol-R, es difícil decidir una dimensión apropiada, puesto que no hay un parámetro establecido que lo establezco más que ensayo y error. Como solución, se han implementado otros algoritmos o técnicas para evitar tener algun problema con la selección de la dimensión. En este proyecto se abordó el Faiss, un algoritmo que hace la búsqueda de vectores característicos semejantes en un tiempo menor al lineal.

## Back-End

Se utilizó el framework **FastAPI**, con el cual conectamos con el front-end a través de dos endpoints, los cuales devolverán el top K de nuestro indice creado y PostgreSQL. Para eso, se interpreta la query enviada por el usuario y se devuelve la data a través de un JSON.


### Endpoints

```python
#1
```
- 111

```python
#2
```
- 222


```python
#3
```

- 333



## Frontend

Se utilizó React para la elaboración de la interfaz. Aquí, el usuario colocará la query y el top k documentos a obtener. Al presionar el botón de **enviar**, se realizará una conexión con las funciones del back-end (una para nuestro índice invertido y otra para Postgres), enviando como parámetros dichas variables. Seguidamente, la página esperará hasta que cada función devuelva un diccionario de los datos obtenidos, para después mostrarlos en formato de tabla, con el tiempo de consulta de cada uno.

### Imágenes del frontend:
Conexión a la PostgreSQL 

![image](https://github.com/ByJuanDiego/db2-project-2/assets/68095284/31d63862-bbfc-453c-a949-16bd85b91b1b)

Conexión al índice creado localmente

![image](https://github.com/ByJuanDiego/db2-project-2/assets/68095284/14de7688-9747-4c1a-9089-e50390fa0d18)

Interfaz al buscar una query

![Resultado](https://github.com/ByJuanDiego/db2-project-2/assets/68095284/80be232e-59cb-49b6-9f71-52ec259d9983)

Comparacion de tiempos al recuperar documentos

![Tiempos](https://github.com/ByJuanDiego/db2-project-2/assets/79115974/84251111-d5b0-4868-b2d0-928993602a83)

## Experimentación

### Resultados

| N     | Seq   | Rtree | HighD |
| ----- | ----- | ----- | ----- |
| 100   | 0.734 | 0.637 | 0.597 |
| 200   | 0.807 | 0.651 | 0.698 |
| 400   | 0.656 | 0.660 | 0.666 |
| 800   | 0.689 | 0.697 | 0.693 |
| 1600  | 0.764 | 0.682 | 0.629 |
| 3200  | 0.726 | 0.632 | 0.666 |
| 6400  | 0.681 | 0.643 | 0.607 |
| 12800 | 0.745 | 0.734 | 0.629 |

![image](https://github.com/ByJuanDiego/db2-project-3/assets/83974213/65770a6e-0a63-471b-9884-8912905d038c)

### Análisis y discusión

Se puede observar que la búsqueda secuencial siempre tarda más que utilizar alguna de las técnicas de indexación propuestas. Asimismo, se observa que a partir de 6400 datos en adelante, el índice de alta dimensionalidad supera al RTree, lo cuál es una manifestación de la maldición de la dimensionalidad.

## Conclusiones

- La búsqueda secuencial puede resultar sencilla de implementar. Sin embargo, existen otras librerías como la de Faiss que resulta aún más sencilla de implementar y en la experimentación resulta más óptimo.
- b
- c


## Autores

|                     **Joaquín Jordán**                   |                                 **Juan Diego Castro**                                 |                       **José Chachi**                     |  **Juan Diego Laredo** |
|:---------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------:|:----:|
|           ![Joaquín](https://avatars.githubusercontent.com/u/83974213)            |      ![Juan Diego Castro](https://avatars.githubusercontent.com/u/79115974?v=4)       |              ![José](https://avatars.githubusercontent.com/u/83974741)              | ![Juan Diego Laredo](https://avatars.githubusercontent.com/u/68095284?v=4) |                                             
| <a href="https://github.com/jjordanoc" target="_blank">`github.com/jjordanoc`</a> | <a href="https://github.com/ByJuanDiego" target="_blank">`github.com/ByJuanDiego`</a> | <a href="https://github.com/JoseChachi" target="_blank">`github.com/JoseChachi`</a> | <a href="https://github.com/DarKNeSsJuaN25" target="_blank">`github.com/DarkNeSsJuaN25`</a>|

## Referencias bibliográficas

- [1] No
