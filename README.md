# Proyecto 3 BD2

## Organización del equipo

|            Participante             |   Papel   |
|:-----------------------------------:|:---------:|
|  José Rafael Chachi Rodriguez       |  Backend  |
|    Joaquín Francisco Jordán O'Connor|  Backend  |
|     Juan Diego Castro Padilla       |  Backend  |
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

Dataset extraído de ![Face Database](http://vis-www.cs.umass.edu/lfw/).

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

### Faiss

## Análisis de la maldición de la dimensionalidad y mitigación


## Back-End

Se utilizó el framework **FastAPI**, con el cual conectamos con el front-end a través de dos endpoints, los cuales devolverán el top K de nuestro indice creado y PostgreSQL. Para eso, se interpreta la query enviada por el usuario y se devuelve la data a través de un JSON.


### Endpoints
```python
#1
```
- 111.

```python
#2
```
- 222


```python
#3
```

- 333.






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


### Gráficos de resultado


## Conclusiones

- a
- b
- c


## Autores

|                     **Joaquín Jordán**                   |                                 **Juan Diego Castro**                                 |                       **José Chachi**                     |  **Juan Diego Laredo** |
|:---------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------:|:----:|
|           ![Joaquín](https://avatars.githubusercontent.com/u/83974213)            |      ![Juan Diego Castro](https://avatars.githubusercontent.com/u/79115974?v=4)       |              ![José](https://avatars.githubusercontent.com/u/83974741)              | ![Juan Diego Laredo](https://avatars.githubusercontent.com/u/68095284?v=4) |                                             
| <a href="https://github.com/jjordanoc" target="_blank">`github.com/jjordanoc`</a> | <a href="https://github.com/ByJuanDiego" target="_blank">`github.com/ByJuanDiego`</a> | <a href="https://github.com/JoseChachi" target="_blank">`github.com/JoseChachi`</a> | <a href="https://github.com/DarKNeSsJuaN25" target="_blank">`github.com/DarkNeSsJuaN25`</a>|

## Referencias bibliográficas

- [1] No
