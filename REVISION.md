# Retroalimentacion

Esto lo llena tu asesor despues de cada revision de avances (semanas 9, 14 y
17). Lo ves haciendo un `git pull` normal de tu repositorio. No lo edites:
crece con una seccion nueva en cada revision, las anteriores no se borran.

Los niveles son los de la rubrica de `evaluacion/individual`: **Excelente**,
**Bueno**, **Suficiente**, **Insuficiente**.

Evidencias, en este curso, es tu codigo en `codigo/`, tus datos en `datos/`,
tus figuras en `figuras/` y la demo del bucle de control.

---

### Nota rápida (2026-09-14)
Tu `sensor.ino.txt` quedó con doble extensión (`.ino.txt` en vez de `.ino`). El Arduino IDE necesita que el archivo termine en `.ino` y se llame igual que su carpeta, así que esto te va a estorbar el día de hardware. Corrígelo antes de la próxima sesión. (El truco de meter un `.txt` para que Git suba las carpetas vacías `datos/` y `figuras/` sí está bien pensado, solo cuida que no se te haya ido también al `.ino`.)

### Nota rápida (2026-09-14) - s02
El `sensor.ino.txt` con doble extensión que te comenté la semana pasada sigue igual, y ahora se agregó otra copia en `codigo/codigo_arduino/codigo_arduino.ino`. El archivo que el curso espera es `codigo/sensor.ino`, tal cual, sin extensión doble ni subcarpeta. Vale la pena resolverlo antes del día de hardware, porque el Arduino IDE necesita ese nombre exacto para poder abrirlo.

### Nota rápida (2026-09-14) - s03
El problema de `sensor.ino.txt` con doble extensión que se comentó hace dos semanas sigue sin resolverse, y ahora hay dos copias distintas (`codigo/sensor.ino.txt` y `codigo/codigo_arduino/codigo_arduino.ino`), ninguna en la ruta que espera el curso (`codigo/sensor.ino`). El resto de la semana 3 va bien: datos balanceados (10/10/10 en `tapado`/`mal_tapado`/`no_tapado`, aunque todavía por debajo del mínimo de 30 por clase). Vale la pena resolver el nombre del archivo ya, antes del día de hardware.

### Nota rápida (2026-09-21) - s05
No veo commits de la semana 05 (`s05 bloque 1`/`s05 bloque 2`). Si tuviste un problema, cuéntamelo para que quede en la bitácora.

### Nota rápida (2026-10-19) - s07
Muy bien: 90 ventanas balanceadas, exactitud de 0.74 reportada con su matriz, y la lectura es concreta (de 8 `tapado` solo acertó 2; `mal_tapado` y `no_tapado` sin errores). Eso es justo lo que la guía pedía. El siguiente paso natural es la autopsia: toma dos o tres de esos `tapado` mal clasificados, búscalos por su `ventana` en `datos_limpios.csv`, grafícalos junto a uno bien clasificado y escribe si tú los habrías distinguido a ojo. Detalle menor: en el bloque 1 dices 72/18, pero tu código usa `test_size=0.25` y partió 67/23; deja el mismo número en los dos lados.
