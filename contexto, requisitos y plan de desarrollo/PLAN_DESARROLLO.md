# PLAN DE DESARROLLO
## Calculadora de Programación Lineal

**Primera entrega:** viernes 4 de septiembre de 2026

---

# 1. Regla de trabajo

Este proyecto se desarrollará de forma incremental.

## Instrucción principal para ChatGPT Desktop

> Trabaja solamente en la fase o versión que se indique. No desarrolles de una vez funcionalidades pertenecientes a versiones posteriores. Antes de avanzar, explica de manera breve qué se hizo, muestra los cambios y comprueba que la versión actual funciona.

Reglas adicionales:

1. Mantener un único archivo principal:
   `programacion_lineal.py`

2. No generar desde el comienzo un programa enorme.

3. Introducir las funciones y clases solamente cuando sean necesarias.

4. Mantener nombres sencillos y descriptivos.

5. Evitar sobrearquitectura.

6. Evitar funcionalidades fuera del alcance.

7. Antes de cada cambio importante:
   - explicar qué se va a hacer;
   - explicar por qué;
   - implementar;
   - probar;
   - hacer commit.

8. Si una solución puede implementarse de dos maneras, preferir la más sencilla de explicar.

9. No utilizar `scipy.optimize.linprog` para sustituir la implementación de los algoritmos.

10. Cuando aparezca una posible mejora que no sea necesaria para la entrega, registrarla en `Posibles mejoras futuras` y continuar con el alcance actual.

---

# 2. Versiones previstas

```text
v0.1  Planeación y diseño
v0.2  Interfaz gráfica básica
v0.3  Método gráfico
v0.4  Simplex de maximización
v0.5  Integración y pruebas manuales
v1.0  Primera entrega

v1.1  Simplex de minimización
v2.0  Entrega final
```

---

# 3. Fase 0 - Planeación y diseño
## Versión v0.1

### Objetivo

Definir el proyecto antes de programar.

### Tareas

- [x] Definir alcance.
- [x] Definir primera y segunda entrega.
- [x] Definir tecnologías.
- [x] Definir restricciones del proyecto.
- [x] Revisar taller resuelto del profesor.
- [x] Preparar historias de usuario.
- [x] Diseñar arquitectura básica.
- [x] Diseñar diagrama de clases.
- [x] Diseñar diagrama de secuencia del método gráfico.
- [x] Diseñar diagrama de secuencia de Simplex.
- [x] Preparar bosquejo definitivo de interfaz.
- [x] Crear estructura inicial del informe.

### Resultado esperado

Antes de programar deben existir:

- `CONTEXTO.md`
- `REQUISITOS.md`
- `PLAN_DESARROLLO.md`
- diagramas básicos;
- esquema del informe.

### Arquitectura conceptual inicial

```text
Usuario
  |
  v
AplicacionPL
  |
  +--------------------+
  |                    |
  v                    v
ProblemaPL        Selector de método
                       |
                +------+------+
                |             |
                v             v
          MetodoGrafico  MetodoSimplex
                |             |
                +------+------+
                       |
                       v
                Resultados GUI
```

### Clases conceptuales

```text
ProblemaPL
- objetivo
- coeficientes_objetivo
- restricciones

MetodoGrafico
- resolver()
- calcular_intersecciones()
- obtener_vertices_factibles()
- evaluar_objetivo()

MetodoSimplex
- crear_tabla()
- seleccionar_pivote()
- pivotear()
- resolver()

AplicacionPL
- crear_interfaz()
- agregar_restriccion()
- eliminar_restriccion()
- leer_problema()
- resolver()
- mostrar_resultados()
```

No se deben agregar más clases salvo que aporten claridad real.

### Commit sugerido

`docs: definir alcance, requisitos y diseño inicial`

---

# 4. Fase 1 - Esqueleto del programa
## Inicio de v0.2

### Objetivo

Crear un programa que abra correctamente y muestre la estructura principal de la interfaz, sin implementar todavía los algoritmos.

### Implementar

- [x] imports;
- [x] ventana principal;
- [x] título;
- [x] selector de método;
- [x] selector max/min;
- [x] función objetivo;
- [x] dos restricciones iniciales;
- [x] botones `+` y `-`;
- [x] botón `Resolver`;
- [x] botón `Limpiar`;
- [x] zona vacía para resultados.

### Todavía NO implementar

- cálculo de vértices;
- región factible;
- Simplex;
- Matplotlib;
- tablas.

### Prueba de versión

Comprobar manualmente:

- [x] abre la ventana;
- [x] se puede seleccionar método;
- [x] se pueden escribir coeficientes;
- [x] `+` agrega una restricción;
- [x] `-` elimina una restricción;
- [x] `Limpiar` vacía los campos.

### Commit sugerido

`feat: crear interfaz grafica base`

---

# 5. Fase 2 - Captura del modelo
## v0.2

### Objetivo

Convertir los datos escritos en la GUI en una representación interna sencilla.

### Implementar

- [x] clase o estructura `ProblemaPL`;
- [x] función para leer coeficientes;
- [x] almacenamiento de restricciones;
- [x] selección del objetivo;
- [x] impresión temporal del modelo en la zona de resultados.

### Ejemplo de resultado temporal

```text
Max Z = 30X1 + 50X2

s.a.
X1 + 3X2 <= 200
X1 + X2 <= 100
X1, X2 >= 0
```

### Razón

Antes de resolver cualquier algoritmo se debe comprobar que la aplicación entiende correctamente lo que ingresó el usuario.

### Prueba

- [x] Ingresar varios modelos y verificar que el texto mostrado coincida exactamente con los datos.

### Commit sugerido

`feat: capturar y mostrar modelo matematico`

---

# 6. Fase 3 - Método gráfico sin gráfica
## Inicio de v0.3

### Objetivo

Resolver matemáticamente el problema antes de dibujarlo.

### Implementar paso a paso

1. [x] Representar cada frontera como una ecuación.
2. [x] Calcular intersecciones:
   - restricción con restricción;
   - restricción con eje X1;
   - restricción con eje X2;
   - incluir `(0,0)` como candidato cuando corresponda.
3. [x] Guardar puntos candidatos.
4. [x] Eliminar duplicados básicos.
5. [x] Comprobar qué puntos satisfacen todas las restricciones.
6. [x] Obtener vértices factibles.
7. [x] Evaluar:
   `Z = c1*X1 + c2*X2`
8. [x] Elegir máximo o mínimo.

### Herramienta auxiliar

NumPy puede utilizarse para resolver pequeños sistemas de dos ecuaciones.

### Resultado antes de graficar

```text
Vértices factibles:
(0, 0)
(0, 50)
(20, 40)
(60, 0)

Evaluación:
Z(0,0) = ...
...

Solución óptima:
X1 = ...
X2 = ...
Z = ...
```

### Prueba

- [x] Comparar los resultados con ejercicios resueltos manualmente.

### Importante

No avanzar a Matplotlib hasta que los vértices y el valor óptimo sean correctos.

### Commit sugerido

`feat: resolver metodo grafico mediante vertices`

---

# 7. Fase 4 - Gráfica
## Final de v0.3

### Objetivo

Representar visualmente el resultado ya calculado.

### Implementar

- [x] líneas de restricciones;
- [x] ejes X1 y X2;
- [x] límites razonables de gráfica;
- [x] región factible sombreada;
- [x] vértices;
- [x] punto óptimo;
- [x] leyenda sencilla.

### No implementar

- zoom;
- controles avanzados;
- guardar imagen;
- edición interactiva.

### Integración

- [x] La gráfica se muestra embebida en Tkinter mediante Matplotlib.

### Prueba

Comparar visualmente:

- [x] rectas;
- [x] región;
- [x] vértices;
- [x] solución.

### Commit sugerido

`feat: agregar grafica de region factible`

---

# 8. Fase 5 - Preparar Simplex
## Inicio de v0.4

### Objetivo

Construir correctamente la tabla inicial antes de automatizar las iteraciones.

### Restricciones admitidas

```text
Max Z = c1X1 + c2X2

a11X1 + a12X2 <= b1
...
am1X1 + am2X2 <= bm

b >= 0
X1, X2 >= 0
```

### Implementar

1. [x] Detectar cantidad de restricciones.
2. [x] Crear una variable de holgura por restricción:
   `S1`, `S2`, ..., `Sm`.
3. [x] Construir matriz de la tabla.
4. [x] Agregar columna `CR`.
5. [x] Construir fila:
   `Z - c1X1 - c2X2 = 0`.
6. [x] Guardar nombres de variables básicas.

### Tabla conceptual

```text
VB | X1 | X2 | S1 | S2 | ... | CR
S1 |    |    | 1  | 0  | ... |
S2 |    |    | 0  | 1  | ... |
Z  | -c1| -c2| 0  | 0  | ... | 0
```

### Prueba

- [x] Comparar la tabla inicial del programa con una tabla elaborada manualmente.

### Commit sugerido

`feat: construir tabla inicial simplex`

---

# 9. Fase 6 - Una iteración de Simplex
## v0.4

### Objetivo

Implementar una sola iteración correctamente.

### Implementar

1. [x] Seleccionar variable entrante.
2. [x] Identificar columna pivote.
3. [x] Calcular razones válidas:
   `CR / coeficiente positivo de columna pivote`.
4. [x] Elegir la menor razón positiva.
5. [x] Identificar variable saliente.
6. [x] Obtener pivote.
7. [x] Dividir fila pivote por el pivote.
8. [x] Hacer ceros en el resto de la columna.

### Mostrar

```text
Variable entrante: X1
Variable saliente: S2
Elemento pivote: 2
```

Después mostrar la nueva tabla.

### Regla

- [x] No implementar todavía un ciclo completo si una sola iteración no está comprobada.

### Commit sugerido

`feat: implementar iteracion simplex`

---

# 10. Fase 7 - Simplex completo
## Final de v0.4

### Objetivo

Repetir automáticamente las iteraciones hasta la tabla óptima.

### Implementar

- [x] ciclo de iteraciones;
- [x] almacenamiento de cada tabla;
- [x] actualización de variables básicas;
- [x] condición de finalización;
- [x] lectura de solución.

### Convención de finalización

Con la convención usada:

`Z - c1X1 - c2X2 = 0`

el proceso de maximización continúa mientras existan coeficientes negativos relevantes en la fila de `Z`.

### Mostrar al usuario

- [x] tabla inicial;
- [x] datos del pivote;
- [x] tabla de cada iteración;
- [x] solución final.

### Prueba mínima

Usar varios problemas básicos resueltos manualmente.

Un problema de prueba útil, compatible con el Simplex básico, puede ser:

```text
Max Z = 30X1 + 50X2

X1 + 3X2 <= 150
X1 + X2 <= 70

X1, X2 >= 0
```

Resultado esperado:

```text
X1 = 30
X2 = 40
Z = 2900
```

Este modelo corresponde al modelo transformado que aparece en uno de los ejercicios del taller y sirve para comprobar la mecánica de las tablas.

- [x] Resultado comprobado en el programa: `X1 = 30`, `X2 = 40`, `Z = 2900`.

### Commit sugerido

`feat: completar simplex de maximizacion`

---

# 11. Fase 8 - Integración
## v0.5

### Objetivo

Unir ambos métodos sin agregar funciones nuevas.

### Comprobar

- [x] selector de método;
- [x] selector objetivo;
- [x] entradas;
- [x] restricciones dinámicas;
- [x] resultados;
- [x] gráfica;
- [x] tablas Simplex;
- [x] botón limpiar.

### Comportamiento importante

Si:

`Método = Simplex`

entonces:

`Objetivo = Maximizar`

para v1.0.

Puede deshabilitarse temporalmente la opción minimizar.

- [x] Al seleccionar Simplex, el objetivo queda en maximizar y los operadores en
  `<=`.
- [x] Al modificar el formulario, se descartan resultados anteriores.

### Commit sugerido

`refactor: integrar metodos en interfaz principal`

---

# 12. Fase 9 - Pruebas manuales
## v0.5

### Objetivo

Comprobar con ejercicios conocidos.

### Método gráfico

Realizar al menos:

- 2 ejercicios de maximización;
- 2 ejercicios de minimización.

### Simplex

Realizar al menos:

- 3 ejercicios básicos de maximización.

### Para cada prueba registrar

```text
Problema:
Resultado manual:
Resultado del programa:
Coincide: sí/no
Observaciones:
```

### No hacer todavía

No construir una suite compleja de pruebas automatizadas salvo que sobre tiempo.

### Commit sugerido

`test: verificar ejercicios de programacion lineal`

---

# 13. Fase 10 - Informe
## v0.5 -> v1.0

El informe debe avanzar en paralelo, no dejarse completamente para el último día.

### Estructura

1. Título.
2. Autores.
3. Introducción.
4. Referente teórico.
5. Procedimiento.
6. Resultados.
7. Conclusiones.
8. Bibliografía.

### Referente teórico

Explicar de manera breve:

- programación lineal;
- función objetivo;
- restricciones;
- región factible;
- vértices;
- método gráfico;
- método Simplex;
- variables de holgura;
- pivoteo.

### Procedimiento

Documentar:

- análisis;
- historias de usuario;
- arquitectura;
- diagramas;
- interfaz;
- implementación del gráfico;
- implementación de Simplex.

### Resultados

Incluir:

- capturas de la interfaz;
- ejercicios ejecutados;
- gráfica;
- tablas Simplex;
- comparación con resultados manuales.

### Conclusiones

Centrarse en:

- utilidad de los métodos;
- relación entre modelo matemático y programa;
- implementación incremental;
- resultados obtenidos.

---

# 14. Cronograma de esta semana

## Lunes 31 de agosto

Prioridad:

- cerrar documentos de planeación;
- arquitectura;
- diagramas;
- bosquejo de interfaz;
- iniciar v0.2.

Objetivo del día:

**tener una ventana funcional sin algoritmos.**

---

## Martes 1 de septiembre

Prioridad:

- captura de modelo;
- método gráfico sin gráfica;
- verificar vértices.

Objetivo del día:

**método gráfico matemáticamente correcto.**

---

## Miércoles 2 de septiembre

Prioridad:

- Matplotlib;
- integrar gráfica;
- iniciar tabla Simplex;
- implementar primera iteración.

Objetivo del día:

**método gráfico terminado y Simplex encaminado.**

---

## Jueves 3 de septiembre

Prioridad:

- terminar Simplex;
- integrar interfaz;
- probar ejercicios;
- tomar capturas;
- completar informe.

Objetivo del día:

**v0.5 funcional y documentada.**

---

## Viernes 4 de septiembre

Prioridad:

- no desarrollar funcionalidades nuevas;
- corregir errores;
- ejecutar pruebas finales;
- revisar código;
- revisar informe;
- generar PDF del informe;
- preparar archivo comprimido;
- etiquetar v1.0 en GitHub.

Objetivo del día:

**entregar una versión estable.**

---

# 15. Checklist para v1.0

## Diseño

- [x] Historias de usuario terminadas.
- [x] Arquitectura terminada.
- [x] Diagrama de clases terminado.
- [x] Diagramas de secuencia terminados.
- [x] Interfaz coherente con diseño.

## Método gráfico

- [x] Maximiza.
- [x] Minimiza.
- [x] Varias restricciones.
- [x] `<=`.
- [x] `>=`.
- [x] No negatividad.
- [x] Vértices.
- [x] Evaluación de Z.
- [x] Óptimo.
- [x] Gráfica.

## Simplex

- [x] Maximización.
- [x] Dos variables.
- [x] Cantidad variable de restricciones.
- [x] Restricciones `<=`.
- [x] Holguras.
- [x] Tabla inicial.
- [x] Pivoteo.
- [x] Iteraciones.
- [x] Resultado.

## Interfaz

- [x] Selector método.
- [x] Selector objetivo.
- [x] Agregar restricción.
- [x] Eliminar restricción.
- [x] Resolver.
- [x] Limpiar.
- [x] Resultados visibles.

## Informe

- [ ] Título.
- [ ] Autores.
- [ ] Introducción.
- [ ] Referente teórico.
- [ ] Procedimiento.
- [ ] Resultados.
- [ ] Conclusiones.
- [ ] Bibliografía.

## Entrega

- [ ] Código fuente.
- [ ] Informe Word.
- [ ] Informe PDF.
- [ ] Archivo comprimido.
- [ ] Repositorio actualizado.
- [ ] Tag `v1.0`.

---

# 16. Después de la primera entrega

La siguiente etapa comienza solamente después de entregar v1.0.

## v1.1

Investigar e implementar Simplex para minimización según la forma solicitada por el profesor.

No debe mezclarse esta funcionalidad con el desarrollo actual.

## v2.0

- integrar minimización;
- probar;
- complementar informe;
- entregar versión final.
