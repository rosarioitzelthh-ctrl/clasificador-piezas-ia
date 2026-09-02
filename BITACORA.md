# Bitácora del proyecto
## Semana 1 - Encuadre y configuración del entorno
### Antes de la clase
he logrado hacer push a github desde el cmd, lo cual yo no sabia xd
Se creó el repositorio del proyecto en GitHub y se organizó su estructura con las carpetas necesarias para guardar lo que vamos a hacer durante las clases.
se configuró todo, para así tener todo listo, junto con las librerías correspondientes

este es el procedimiento para hacer push:
-para hacer un push primero edito mi archivo
-luego hago git add .
-luego git commit
-luego git push

1. ¿Cuál es la diferencia entre programar la regla y aprender la regla?
Cuando programo una regla, yo le digo directamente al programa qué tiene que hacer.
Por ejemplo, si quiero que un ventilador se encienda cuando haga mucho calor, puedo decirle que cuando la temperatura pase de cierto número, encienda el ventilador.
2. ¿Cuál es tu dominio y cuáles son tus tres tipos de pieza?
Mi dominio sería clasificación por estado, clasificará si la tapa está bien puesta/ floja/ sin tapa
3. Describe el bucle de control de tu sistema: qué mide tu sensor, qué tiene que decidir el modelo y qué haría el actuador con cada uno de tus tres tipos.
Mi sensor detecta la presencia de un objeto mediante luz infraroja, en este caso, detectaria si hay o no una tapa frente al sensor. Mientras que el actuador cuando la botella este cerrada, no realiazaria accciones, y sin tapa separaria el recipiente.

1. Qué sensor vas a usar y qué tipo de salida tiene.
el KY-032, los valores que entregaria serian 0 y 1.

2. Tres líneas de ejemplo tal como se van a ver saliendo de tu Arduino, con valores plausibles para tu caso.
0
1
0

3. Por qué el Arduino no puede mandar Serial.println("Leyendo...").
Esto se debe a que el Arduino solamente manda datos, puesto que si lo llevara romperia a Python cuando lo intente convertir a numeros.


1. ¿Cuánto tarda tu pieza en cruzar frente al sensor? Es una estimación, mídelo a ojo o con el cronómetro del celular.
2 segundos.
2. Con ese tiempo, ¿qué delay() eliges para tener al menos 20 muestras del evento?
Un delay(100), asi cada muestra se toma cada 0.1 segundos, en 2 segundos habría 20 muestras.
3. ¿Cuántas muestras te da eso mientras la pieza pasa?
aprox. 20 muestras.

Semana 3 - Recolección de datos etiquetados (U2)

1. Columnas de mi datos.csv
Columna	¿Qué guarda?
ventana -El número de la pasada o evento que registró el sensor.
t-El número de muestra dentro de esa ventana.
valor-La lectura que obtiene el sensor.
etiqueta-Indica si la pieza está tapada, mal tapada o no tapada.

2. Mis tres etiquetas
Mis tres etiquetas serán:

tapado
mal_tapado
no_tapado

ojo, escribir en minúsculas y sin acentos para evitar problemas al trabajar con el archivo.

3. Cinco filas de ejemplo de mi tabla
ventana,t,valor,etiqueta
0,0,512,tapado
0,1,510,tapado
0,2,508,tapado
1,0,620,mal_tapado
1,1,615,mal_tapado


### Avance del proyecto
Por el momento corregí lo que tenia mal
