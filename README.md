# Proyecto 3 BD2

## Organización del equipo

|            Participante             |   Papel   |
|:-----------------------------------:|:---------:|
|  José Rafael Chachi Rodriguez       |  Backend  |
|    Joaquín Francisco Jordán O'Connor|  Backend  |
|     Juan Diego Castro Padilla       |  Backend |
|   Juan Diego Laredo Yarma           | Frontend  |

## Introducción 
En este proyecto se nos ha pedido dar soporte a las búsquedas y recuperación eficientemente de datos multimedia, imágenes. Se utilizarán distintos algoritmos, además se apoyará de estructuras multidimensionales.

## Objetivos
### Principal
Aplicar los algoritmos de búsqueda y recuperación de la información para archivos multimedia aprendidos en clase.
### Secundarios
- Utilizar métodos de indexación para hacer las búsquedas multimedia de manera eficiente.
- Crear una interfaz amigable para la realización de las consultas de imágenes.


## Descripción del dominio de datos
El dataset utilizado son rostros de personas famosas de cualquier profesión. Nótese que una imagen no necesariamente contiene el rostro de solo 1 persona.

![image](https://github.com/ByJuanDiego/db2-project-3/assets/83974741/2687074e-0723-47b9-b174-81747e8166f0)

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
Es una carpeta de carpetas con los nombres de los rostros principales. Adicionalmente, dentro de cada carpeta existen entre 1 a más imágenes de rostro referentes al nombre de la carpeta.

Dataset extraído de [Face Data](http://vis-www.cs.umass.edu/lfw/).

## Técnicas de indexación utilizadas

### Sin indexación

La búsqueda secuencial, también llamada lineal, es la técnica utilizada al no implementar ningun tipo de indexación. Esta técnica es muy sencilla de implementar; sin embargo, estamos ejerciendo fuerza bruta al calcular la similitud (distancia) entre los datos lo cual lleva a una alta complejidad computacional. Se desarrolló la búsqueda lineal para que se pueda utilizar la búsqueda KNN y la búsqueda por rango basándose en los siguientes esquemas.

![image](https://github.com/ByJuanDiego/db2-project-3/assets/83974741/415bded7-b068-4705-bea1-5cfff171a3d5)

En ambas implementaciones calculamos la distancia de la query hacia todos los datos. En la búsqueda por rango se añade al resultado solo si la distancia calculada es menor a lo indicado. Mientras que para la búsqueda secuencial KNN, se utilizó una cola de prioridad y se añade al resultado solo si se encuentra una menor distancia calculada con respecto a las distancias dentro del heap.

### RTree

La búsqueda KNN en el RTree se realiza utilizando una búsqueda con un rango inicialmente infinito y luego reduciendo este radio a la máxima distancia de los KNN según se evalúan los MBR hoja.

![image](https://github.com/ByJuanDiego/db2-project-3/assets/83974213/3d8ebbed-ec33-46d5-a7dd-97b34148e7d5)

Por otro lado, la búsqueda por rango no se implementa como un método para el índice en la librería `rtree` de Python, pero se puede simular utilizando la búsqueda por intersección con el MBR {(x-r, y-r),(x+r,y+r)} donde (x,y) es el vector de consulta y luego filtrando aquellos puntos cuya distancia es menor al radio. Esta lógica se puede generalizar a N dimensiones sin ningún problema. 

### Faiss (LSH)

Faiss (Facebook AI Similarity Search) implementa la clase ```IndexLSH```, que permite trabajar de forma eficiente la similitud entre vectores característicos de mayor dimensión. Para ello, el objetivo de esta técnica es asignar vectores característicos que tengan similitudes a los mismos buckets. Mientras que en una tabla hash tradicional el objetivo era minimizar las colisiones, en esta técnica se busca maximizar las colisiones siempre y cuando esta tenga sentido. LSH es usado tanto como para resolver el problema del vecino más cercano como para agrupación de datos. El algoritmo consta de las siguientes partes:

- Dividir los vectores en subpartes (bandas) y en lugar de procesar todo el vector en la funcion hash lo que se hace es pasar cada una de las bandas en la funcion hash.
- Si se tienen b subvectores, pueden usarse b funciones hash o una sola para elegir el bucket donde se asignara el subvector.
- La version mas flexible de este algoritmo indica que si existe una colision entre cualquier par de subvectores se consideran los vectores completos como posibles candidatos.

![image](https://github.com/ByJuanDiego/db2-project-3/assets/83974741/2835ae34-c6c8-435e-b447-933368f8f6b6)

![image](https://github.com/ByJuanDiego/db2-project-3/assets/83974741/2a3b1fb5-6bc8-477b-8f39-c02f12bd639b)

Desventajas:

- Pueden existir falsos positivos, puesto que el algoritmo considera como candidato un vector que tenga una subparte que colisione con la del input, pero puede que la mayor parte del vector en realidad no sea similar.
- Requieren muchas funciones hash para lograr resultados aceptables, lo que se traduce en memoria adicional.
- La función hash no está adaptada a los datos de entrada (es independiente de los datos). Esto lo vuelve mas sencillo y rapido, pero puede conducir a resultados de elección no tan óptimos en la práctica. En general los resultados son bastante buenos, pero puede darse el caso de que existan mejores.

## Análisis de la maldición de la dimensionalidad y mitigación

El árbol-R es una estructura dimensional que agrupa sus elementos en distintos locaciones geográficas. Estas locaciones son fijadas de acuerdo a la dimensión indicada en el árbol. Es por ello que es recomendable
aumentar la cantidad de dimensiones del árbol-R para tener los elementos similares agrupados disjuntos. Sin embargo, existe una situación en que si la dimensión es un número demasiado grande, existen variadas locaciones en donde los elementos se agrupan. Si los elementos agrupados están dispersos, en el algoritmo de búsqueda de los elementos KNN no se aplicará un filtro prudente y esto ocasiona que nuestra búsqueda KNN en un
árbol-R sea similar en complejidad computacional a una búsqueda lineal. En otras palabras, hay que ir aumentando la dimensión del RTree para agilizar la búsqueda hasta un tamaño en donde la dimensión no sea excesiva y sea perjudicial.

Con esta limitación del árbol-R, es difícil decidir una dimensión apropiada, puesto que no hay un parámetro establecido que lo establezco más que ensayo y error. Como solución, se han implementado otros algoritmos o técnicas para evitar tener algun problema con la selección de la dimensión. En este proyecto se abordó el Faiss LSH, un algoritmo que hace la búsqueda de vectores característicos semejantes en un tiempo menor al lineal.

![image](https://github.com/ByJuanDiego/db2-project-3/assets/83974741/e03f9aba-9e23-48fd-8ebd-d2af200401d8)

## Experimentación

### Resultados

| N     | Seq   | Rtree | HighD |
| ----- | ----- | ----- | ----- |
| 100   | 0.001 | 0.001 | 0.000 |
| 200   | 0.001 | 0.001 | 0.000 |
| 400   | 0.002 | 0.001 | 0.001 |
| 800   | 0.003 | 0.003 | 0.000 |
| 1600  | 0.006 | 0.005 | 0.000 |
| 3200  | 0.014 | 0.007 | 0.001 |
| 6400  | 0.038 | 0.022 | 0.001 |
| 12800 | 0.050 | 0.066 | 0.001 |

![image](https://github.com/ByJuanDiego/db2-project-3/assets/83974213/c41c9aca-e74d-4e57-b768-92264013cfb2)


### Análisis y discusión

En el gráfico puede observar una mejora cuando se utiliza el RTree y no hay muchos datos; sin embargo, tomando más de 6400 datos, el rendimiento del RTree es peor que el de la consulta secuencial. También vemos que el índice que utiliza LSH supera a ambas técnicas de manera significativa. Esto tiene sentido, pues es una técnica especializada en manejar datos de alta dimensionalidad, como los vectores característicos de imágenes con los que se trabajó en este proyecto de dimensión 128.

## Conclusiones



## Autores

|                     **Joaquín Jordán**                   |                                 **Juan Diego Castro**                                 |                       **José Chachi**                     |  **Juan Diego Laredo** |
|:---------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------:|:----:|
|           ![Joaquín](https://avatars.githubusercontent.com/u/83974213)            |      ![Juan Diego Castro](https://avatars.githubusercontent.com/u/79115974?v=4)       |              ![José](https://avatars.githubusercontent.com/u/83974741)              | ![Juan Diego Laredo](https://avatars.githubusercontent.com/u/68095284?v=4) |                                             
| <a href="https://github.com/jjordanoc" target="_blank">`github.com/jjordanoc`</a> | <a href="https://github.com/ByJuanDiego" target="_blank">`github.com/ByJuanDiego`</a> | <a href="https://github.com/JoseChachi" target="_blank">`github.com/JoseChachi`</a> | <a href="https://github.com/DarKNeSsJuaN25" target="_blank">`github.com/DarkNeSsJuaN25`</a>|
