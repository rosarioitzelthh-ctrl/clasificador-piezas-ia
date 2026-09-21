# Bitácora del proyecto

## Semana 1 - Encuadre y configuración del entorno

### Antes de la clase

He logrado hacer push a GitHub desde el CMD, lo cual yo no sabía xd.

Se creó el repositorio del proyecto en GitHub y se organizó su estructura con las carpetas necesarias para guardar lo que vamos a hacer durante las clases.

También se configuró todo para tener listo el entorno y las librerías que vamos a utilizar.

Este es el procedimiento que sigo para hacer un push:

* Primero edito mi archivo.
* Luego hago `git add .`
* Después hago `git commit`.
* Finalmente hago `git push`.

### Preguntas

**1. ¿Cuál es la diferencia entre programar la regla y aprender la regla?**

Cuando programo una regla, yo le digo directamente al programa qué tiene que hacer.

Por ejemplo, si quiero que un ventilador se encienda cuando haga mucho calor, puedo decirle que cuando la temperatura pase de cierto número, encienda el ventilador.

**2. ¿Cuál es tu dominio y cuáles son tus tres tipos de pieza?**

Mi proyecto será para clasificar el estado de una botella. Se clasificará si la tapa está bien puesta, está mal puesta o no tiene tapa.

Mis tres tipos de pieza serán:

* tapado
* mal_tapado
* no_tapado

**3. Describe el bucle de control de tu sistema: qué mide tu sensor, qué tiene que decidir el modelo y qué haría el actuador con cada uno de tus tres tipos.**

Mi sensor medirá la distancia entre el sensor y la botella mediante ondas ultrasónicas.

El modelo tendrá que decidir si la botella está tapada, mal tapada o no tiene tapa.

Cuando la botella esté bien tapada, no se realizaría ninguna acción. Si está mal tapada o no tiene tapa, el sistema podría separar la botella para revisarla.

---

# Semana 2 - Lectura del sensor

### 1. ¿Qué sensor vas a usar y qué tipo de salida tiene?

Voy a utilizar un sensor ultrasónico **HC-SR04**.

El sensor mide la distancia que hay entre él y la pieza, y entrega un valor en centímetros.

### 2. Tres líneas de ejemplo tal como se van a ver saliendo de tu Arduino

```text
24.52
24.31
23.87
```

Estos valores representan la distancia aproximada entre el sensor y la pieza.

### 3. ¿Por qué el Arduino no puede mandar `Serial.println("Leyendo...")`?

Esto se debe a que Python espera recibir números para poder trabajar con los datos del sensor.

Si Arduino manda palabras junto con las lecturas, Python podría tener problemas al intentar convertirlas en números.

---

# Semana 3 - Recolección de datos etiquetados

### Bloque 1

**1. ¿Cuánto tarda tu pieza en cruzar frente al sensor?**

Aproximadamente 5 segundos.

**2. Con ese tiempo, ¿qué `delay()` eliges para tener al menos 20 muestras del evento?**

Elegí un `delay(100)`, porque se toma una muestra cada 0.1 segundos. En aproximadamente 2 segundos tendría unas 20 muestras.

**3. ¿Cuántas muestras te da eso mientras la pieza pasa?**

Aproximadamente 20 muestras.

---

### Mis datos

**1. Columnas de mi `datos.csv`**

| Columna  | ¿Qué guarda?                                            |
| -------- | ------------------------------------------------------- |
| ventana  | El número de la pasada o evento que registró el sensor. |
| t        | El número de muestra dentro de esa ventana.             |
| valor    | La distancia que obtiene el sensor en centímetros.      |
| etiqueta | Indica si la pieza está tapada, mal tapada o no tapada. |

**2. Mis tres etiquetas**

Mis tres etiquetas serán:

* `tapado`
* `mal_tapado`
* `no_tapado`

Las escribiré en minúsculas y sin acentos para evitar problemas con el archivo.

**3. Cinco filas de ejemplo de mi tabla**

```text
ventana,t,valor,etiqueta
0,0,24.52,tapado
0,1,24.48,tapado
0,2,24.51,tapado
1,0,20.31,mal_tapado
1,1,20.15,mal_tapado
```

---

## Bloque 2 - Protocolo de recolección

### 1. ¿Cuántas ventanas por clase?

Voy a capturar 30 ventanas por cada clase, teniendo un total de 90 ventanas.

Mis tres clases serán:

* `mal_tapado`
* `no_tapado`
* `tapado`

### 2. Orden de las pasadas

Voy a alternar las clases para que los datos queden repartidos durante toda la captura:

**tapado → mal_tapado → no_tapado → tapado → mal_tapado → no_tapado**

Y repetiré este orden hasta completar las 30 ventanas de cada clase.

### 3. ¿Cómo voy a mantener pareja la velocidad?

Para que la velocidad sea lo más parecida posible, voy a marcar con cinta en la mesa el punto donde empieza y termina el recorrido.

La pieza recorrerá aproximadamente 20 cm y trataré de hacer cada pasada en aproximadamente 2 segundos.

También voy a intentar mantener el mismo movimiento y no cambiar la velocidad dependiendo de la clase de pieza.

### 4. Distancia del sensor

Voy a colocar el sensor HC-SR04 en una posición fija y la pieza pasará aproximadamente a 5 cm del sensor.

Voy a marcar la posición para que todas las piezas pasen por el mismo lugar.

El sensor permanecerá fijo durante toda la captura para evitar que la distancia cambie entre una prueba y otra.

---

# Semana 4 - Limpieza y normalización de señales

#### 1. ¿Qué tipo de ruido ves en tu señal y de dónde crees que viene?

Se observan variaciones y algunos cambios repentinos en las lecturas del sensor. Considero que este ruido puede venir de pequeñas variaciones en la posición de la botella, del movimiento que pueda tener a causa del pulso de mi mano y de cambios en la distancia que detecta el sensor ultrasónico. También pueden existir pequeñas variaciones propias de las lecturas del sensor.

#### 2. ¿Qué rango físico tiene tu sensor y qué valores estás descartando por imposibles?

El sensor ultrasónico HC-SR04 tiene un rango aproximado de 2 a 400 cm. Por eso, en la limpieza se descartan los valores menores o iguales a 0 y los valores mayores a 400 cm, ya que están fuera del rango físico que puede medir el sensor.

#### 3. ¿Qué tamaño de filtro elegiste y por qué, en relación con la duración de tu evento?

Se eligió un filtro de media móvil de 5 muestras. Se escogió este tamaño porque permite reducir pequeñas variaciones y ruido sin modificar demasiado la forma de la señal. Como cada ventana contiene 200 muestras, el filtro de 5 muestras es pequeño en comparación con la duración completa del evento y permite conservar los cambios importantes de la señal.
## Bloque 2

### Resultados de la limpieza

#### 1. ¿Cuánto se movió tu línea base entre la primera y la última ventana de la sesión?

La línea base se calculó utilizando el promedio de las primeras muestras de cada ventana. Al comparar la primera y la última ventana se observa que existe un cambio en la línea base, por lo que fue necesario corregirla antes de realizar la normalización.

El movimiento de la línea base fue de **32.83 cm** entre la primera y la última ventana.

#### 2. ¿Qué normalización elegiste y por qué?

Se utilizó una normalización Min-Max. Se eligió porque permite llevar los valores de cada ventana a un rango entre 0 y 1. Esto facilita la comparación entre las diferentes ventanas y evita que las diferencias de escala afecten demasiado al clasificador.

#### 3. Al comparar antes y después: ¿se parecen más entre sí las ventanas de una misma clase?

Después de aplicar el filtrado, la corrección de la línea base y la normalización, las señales presentan menos variaciones causadas por el ruido y son más fáciles de comparar. Las ventanas de una misma clase muestran un comportamiento más parecido que antes de realizar la limpieza, aunque todavía existen algunas diferencias debido a las lecturas del sensor y a la posición de la botella.

## Semana 5 - Características en el dominio del tiempo

### Bloque 1: Selección de características

Para esta semana elegí algunas características que pueden ayudar a diferenciar los tres estados de las tapas: `tapado`, `mal_tapado` y `no_tapado`.

| Característica | Por qué debería distinguir mis clases |
|---|---|
| **Media** | Me puede ayudar a conocer cuál fue el valor promedio de la distancia durante la medición. |
| **Desviación estándar** | Puede mostrar qué tanto cambió la señal mientras la pieza estaba frente al sensor. |
| **Mínimo** | Puede indicar qué tan cerca llegó la pieza al sensor. |
| **Máximo** | Me permite conocer cuál fue la distancia más grande registrada durante la ventana. |
| **Rango** | Puede mostrar qué tanto cambió la distancia entre el valor más pequeño y el más grande. |
| **Energía** | Resume los cambios que tuvo la señal durante toda la ventana. |
| **Duración** | Puede ayudar a saber cuánto tiempo estuvo la pieza frente al sensor. |

### Mi predicción

Creo que la característica que puede ser más útil será el **rango**, porque puede mostrar qué tanto cambia la distancia cuando la tapa está bien puesta, floja o no está puesta.

La característica que creo que puede ser menos útil es el **máximo**, porque puede tener valores parecidos entre algunas piezas y también puede cambiar dependiendo de la posición de la pieza frente al sensor.


### Bloque 2: `features.py` y la tabla final

En este bloque trabajamos con el archivo `datos_limpios.csv` para obtener características de cada ventana. El programa agrupa las muestras por ventana y calcula diferentes valores para resumir cada una de ellas.

Las características que obtuvimos fueron la **media, desviación, mínimo, máximo, rango, energía y duración**. También conservamos la columna `ventana`, ya que sirve para saber de qué señal salió cada registro y poder identificar alguna muestra posteriormente.

### 1. ¿Cuántas filas y columnas tiene `features.csv` y por qué?

El archivo `features.csv` quedó con **91 filas y 9 columnas**.

Las filas corresponden a cada ventana que teníamos registrada, por lo que hay una fila por cada pasada o muestra completa de una pieza. Las columnas corresponden a la ventana, las características calculadas y la etiqueta de cada clase.

### 2. ¿Qué par de características separa mejor las clases?

Realizamos diferentes gráficas de dispersión utilizando distintos pares de características para comparar las tres clases.

El par que mejor separa las clases fue **rango_vs_duracion**, ya que en la gráfica se pueden observar las tres clases con una separación más clara entre sus puntos.

También realizamos otras dos combinaciones para comprobar si existía una mejor separación. Esto nos permitió comparar visualmente las características antes de continuar con el clasificador.

### 3. ¿Hay dos clases que se encimen?

Al revisar las gráficas, se puede observar que **minimo_vs_rango y desv_vs_energia** son las graficas que no se estan encimando del todo, pero si estan muy juntos los puntos y es mas difcil diferenciar los datos.

Si existe un poco de encimamiento, esto significa que algunas ventanas tienen características parecidas aunque pertenezcan a clases diferentes. Por ahora, podemos continuar con estas características y posteriormente comprobar qué tan bien funciona el clasificador.

### Conclusión

En este bloque convertimos las señales de cada ventana en una tabla de características que será más fácil de utilizar para entrenar el modelo. También comparamos diferentes pares de características mediante gráficas para observar cuáles ayudan más a diferenciar las clases.


#   Semana 6 - Características en el dominio de la frecuencia (U2)

#### Bloque 1: Mirar una señal en frecuencia

1. **Frecuencia de muestreo**

En nuestro proyecto estamos tomando aproximadamente **100 muestras por segundo (100 Hz)**. Esto se debe principalmente al `delay(10)` que tenemos en el código del sensor, que representa aproximadamente 10 ms entre muestras.

2. **Frecuencia de Nyquist**

La frecuencia de Nyquist es de **50 Hz**, ya que corresponde a la mitad de nuestra frecuencia de muestreo:

**100 Hz / 2 = 50 Hz**

Esto significa que nuestra señal puede representar frecuencias de hasta aproximadamente 50 Hz. Las frecuencias mayores no se pueden detectar correctamente y pueden provocar aliasing.

3. **Resolución en frecuencia**

Cada ventana que utilizamos tiene **200 muestras**. Por lo tanto, la resolución en frecuencia es:

**100 Hz / 200 = 0.5 Hz**

Esto significa que podemos distinguir cambios en frecuencia aproximadamente cada **0.5 Hz**.

4. **Predicción**

Creo que nuestras clases podrían presentar algunas diferencias en frecuencia, pero no espero que sean demasiado grandes. Nuestro sensor ultrasónico mide la distancia y las diferencias entre las piezas principalmente cambian la forma y el nivel de la señal. Por eso pienso que las características que obtuvimos en el dominio del tiempo podrían ser más útiles, aunque la frecuencia nos puede ayudar a encontrar diferencias que no se notan fácilmente en la gráfica normal.

###  Bloque 2: FFT y características de las señales

**1. ¿Cuál es la frecuencia dominante que observas y qué sentido físico tiene?**

Al ver la gráfica, la mayor parte de la señal se encuentra en las frecuencias bajas. Esto tiene sentido porque el sensor está midiendo la distancia de las botellas y los cambios no ocurren tan rápido. El punto más alto de la gráfica representa la frecuencia que aparece más en la señal.

**2. ¿Las características de frecuencia ayudan a separar las clases? ¿Qué observas en la gráfica?**

Sí ayudan un poco, pero no separan completamente las tres clases. En la gráfica se pueden notar algunas diferencias entre las señales, aunque en algunas partes se parecen bastante. Por eso creo que estas características pueden servir como apoyo, pero no serían suficientes por sí solas para distinguir si la tapa está bien puesta, floja o si no tiene tapa.

**3. ¿Conservarías o eliminarías las características de frecuencia? ¿Por qué?**

Yo las conservaría porque pueden aportar información que no se veía tan claramente con las características anteriores. Aunque no separan completamente las clases, pueden servir junto con las demás características para que el programa tenga más información al momento de identificar cada tipo de tapa.


### Avance del proyecto
Por el momento corregí lo que tenia mal
