<h1 align="center"> ESPERANZA DE VIDA </h1>

![VIDA](https://assets.sutori.com/user-uploads/image/e7e0f55e-65e7-4943-b9f9-304b5baf90e9/09d89a731e7fde7ea1314a4076142e17.jpeg)

# **INTRODUCCION**

La esperanza de vida es una estimación del número promedio de años de vida adicionales que una persona podría esperar vivir si las tasas de mortalidad por edad específica para un año determinado permanecieran durante el resto de su vida.

## *CONTEXTO DEL ANALISIS*

En este caso nos situamos en el rol de una consultora de datos que tiene como cliente a una aseguradora de vida, la cual nos pide evaluar las diferencias entre países, regiones o grupos demográficos sobre la esperanza de vida para identificar oportunidades de negocio.

La expectativa de vida, es decir la edad promedio que la gente alcanza en un país, suele ser uno de los mejores indicadores de desarrollo y calidad de vida en el mundo. Los lugares donde las personas se mueren más jóvenes tiene una correlación con una baja calidad de vida.


## *OBJETIVO GENERAL*

Establecer un análisis del impacto de los factores socioeconómicos en la esperanza de vida en los diferentes países seleccionados (30), para ayudar a una aseguradora de vida a expandir su negocio en un nuevo mercado internacional.


## *OBJETIVOS ESPECIFICOS*

-  Averiguar cuál de los países en estudio tienen la capacidad de adquirir un seguro de vida, a partir del estudio de indicadores bases como por ejemplo el acceso a posibilidades de obtener un empleo estable.

- Analizar profundamente cuestiones inherentes al estilo de vida de los posibles clientes como por ejemplo, el estado civil, la cantidad de hijos que tiene, si es extranjero o no, si tiene casa propia, si tiene vehiculo, etc.
  
- Analizar la situación financiera de los posible clientes, cosas como si solicita préstamos de dinero, si tiene deudas, actitud crediticia con instituciones financieras.

- Analizar la influencia que tiene el acceso a la educación (principalmente en el nivel Universitario).

- Medir la pobreza del país en estudio, evidentemente en países que tiene un ingreso per cápita alto nos da referencia del nivel de bienestar de su población dándonos un resultado clave en el cual se muestran las posibilidades de adquisición de un seguro de vida que tienen sus habitantes.

## *KPIS ASOCIADOS*

- Principalmente se determinará el volumen de oportunidades que surgen en un país de posible expansión.

- Tasa de Precisión del Modelo.

- ROI de la compañía de Seguros.
  
- Crecimiento de las inversiones.

- Tasa de conversion.


## *ALCANCE*

Producir un resultado acertado por medio de un Modelo de Machine Learning tomando en consideración todos los puntos anteriores, y si en un año la ganancia de la inversión es retornada podremos deducir que el estudio de los datos se estuvo ejecutando de manera correcta, vale la pena destacar que se tomarán en cuenta medidas ya existentes dentro de la aseguradora y el comportamiento de las ganancias de los últimos años de desempeño dentro del ámbito empresarial.


## *SOLUCIÓN DEL PROBLEMA*

Se ofrece implementar un Modelo de Machine Learning para dar un reporte a la Aseguradora con datos reales y actuales, con el fin de garantizar que la expansión que está en proyección se logre con el menor riesgo posible, generando un perfil óptimo de posibles clientes bajo el analisis de criterios de tipo socio-economico de cada país en estudio.

### Organizacion y metodologias de trabajo.


Este proyecto esta segmentando en 3 areas de trabajo:
* Analisis de Datos
* Ingenieria de Datos
* Equipo de Machine Learning

En el siguiente Diagrama se puede observar el flujo de trabajo ademas de cuales son las minimas tecnologias necesarias para alcanzar los objetivos del presente proyecto


![Stack](https://github.com/Lilsup99/indice_esperanza_vida/blob/main/Stack%20Tecnologico/STACK.jpg?raw=true)

## Modelo de Machine Learning (docs)

El objetivo es desarrollar un modelo de seleccion binaria que determine si un pais es rentable o no para 
una posible inversion por parte del cliente.

### Conceptos clave para entrenar el modelo

* Indice de esperanza de vida
* Relacion natalidad vs mortalidad
* Nivel de ingreso (se puede considerar PIB o indice GINI)
* Acceso a internet
* Indices de niveles de educacion
* Inflacion / nivel de pobreza
* Porcentaje de clase social.

### Acerca del dataset para el entrenamiento

Esta compuesto de las siguientes columnas

1. `year`: corresponde al año del respectivo registro
2. `country`: el pais
3. `Life expectancy at birth, total (years)`: Es el indice de esperanza de vida
4. `Population growth (annual %)`: Crecimiento poblacional anual, este indicador se usa para expresar la relacion natalidad vs mortalidad
5. `School enrollment, tertiary (% gross)`: inscripcion escolar, educacion terciara implica a la 
cantidad de matriculas en el nivel universitario. Esto se usara para medir el nivel de educacion.
6. `Internet Users(%)`: Porcentaje de acceso a internet en un determinado pais, el nivel de acceso
a internet alto puede implicar altas cantidades de potenciales clientes para ofrecer servicios
por medio de campañas de marketing digital.
7. `GDP per capita (current US$)`: PIB per capita
8. `Inflation, consumer prices (annual %)`: Inflacion anual.

### Variable objetivo

Se debe incorporar al dataset de entrenamiento una variable que indique el objetivo de seleccion
para la clasificacion binaria del modelo de ML, recordemos que el objetivo es clasificar un pais 
con excelente potencial para hacer inversiones. Por ser clasificacion binaria dicha columna que se incorporara 
al dataset solo contendra dos valores `0` y `1`

* `0`: El pais tiene potencial para hacer una inversion
* `1`: El pais NO tiene potencial para hacer una inversion

Para hacer la seleccion de estos valores a cada registro del dataset, se van a tomar en cuenta los conceptos claves mencionados anteriormente. Primeramente, tomando en cuenta cada concepto por individual, se clasifica un pais sea en la categoria `0` o en la categoria `1`, esto se hace de la siguiente manera:

- Indice de esperanza de vida: Si el valor del dato en la columna `Life expectancy at birth, total (years)` es mayor o igual a `75.0` entonces el pais se clasifica en `0`, caso contrario `1`.

- Relacion natalidad vs mortalidad: Si el valor en la columna `Population growth (annual %)` es mayor a 0, entonces el pais se clasifica en `1.0`, caso contrario, se clasifica en `1`.

- Nivel de ingreso: Si el valor en la columna `GDP per capita (current US$)` es mayor o igual a `6955.594138`, entoces el pais se clasifica en `0`, caso contrario se clasifica en `1`.

- Acceso a internet: Si el valor en la columna `Internet Users(%)` es mayor a `60.0`(%), entonces el pais se clasifica en
`0`, caso contrario se clasifica en `1`.

- Indices de niveles de educacion: Si el valor en la columna `School enrollment, tertiary (% gross)` es mayor o igual a `45.0`, entonces el pais se 
clasifica en `0`, caso contrario se clasifica en `1`.

- Inflacion / nivel de pobreza: Si el valor en la columna `Inflation, consumer prices (annual %)` es menor que 
`7.5`(%), entonces el pais se clasifica en `0`, caso contrario, se clasifica en `1`.

### Observacion

Para asignacion de la variable objetivo se puede por ejemplo establecer que el registro cumpla con todas las 
condiciones, confirmando que el valor sera 0, o tambien se puede tomar un numero menor al total de opciones, para el primer modelo entrenado se considero solo los registros que cumplen por lo minimo 4 condiciones. Ese valor de condiciones minimas a cumplir puede ser considerado un hiperparametro especifico para este modelo de Machine Learning.


## *DISCLAIMER*

Este trabajo investigativo es con fines educacionales, el resultado arrojado por los productos producidos ofrece un análisis exploratorio de la data recolectada en bancos de datos mundiales y  no da referencia para que sea tomado como fundamento para hacer inversiones de capital de empresas en expansión.
