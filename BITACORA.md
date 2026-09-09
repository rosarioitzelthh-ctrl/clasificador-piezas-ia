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

### 1. ¿Qué tipo de ruido ves en tu señal y de dónde crees que viene?

Se ven pequeñas variaciones en las mediciones de distancia. Pueden venir de pequeñas diferencias al mover la pieza, del sensor o de cambios en el ambiente.

### 2. ¿Qué rango físico tiene tu sensor y qué valores estás descartando por imposibles?

El HC-SR04 mide distancias en centímetros. Para mi proyecto, la pieza estará aproximadamente a 5 cm del sensor.

Voy a descartar valores que estén fuera del rango que estoy utilizando para la captura o que sean claramente incorrectos.

### 3. ¿Qué tamaño de filtro elegiste y por qué?

Elegí un filtro de tamaño **5** porque ayuda a reducir pequeñas variaciones en las mediciones y permite que la señal se vea más pareja sin cambiar demasiado los datos originales.



### Avance del proyecto
Por el momento corregí lo que tenia mal
