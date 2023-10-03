# Modelo de Machine Learning (docs)

El objetivo es desarrollar un modelo de seleccion binaria que determine si un pais es rentable o no para 
una posible inversion por parte del cliente.

## Conceptos clave para entrenar el modelo

* Indice de esperanza de vida
* Relacion natalidad vs mortalidad
* Nivel de ingreso (se puede considerar PIB o indice GINI)
* Acceso a internet
* Indices de niveles de educacion
* Inflacion / nivel de pobreza
* Porcentaje de clase social.

## Acerca del dataset para el entrenamiento

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

## Variable objetivo

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