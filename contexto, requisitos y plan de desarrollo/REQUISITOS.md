# REQUISITOS DEL PROYECTO
## Calculadora de Programación Lineal

---

## 1. Alcance de esta especificación

Este documento define los requisitos de la **primera entrega**.

La meta es implementar solamente lo necesario para presentar una aplicación sencilla, funcional y explicable.

---

# 2. Historias de usuario

## HU-01 - Seleccionar método

> Como estudiante, quiero seleccionar el método gráfico o el método Simplex para resolver el problema mediante el procedimiento correspondiente.

---

## HU-02 - Seleccionar el objetivo

> Como estudiante, quiero indicar si el problema busca maximizar o minimizar para que el programa determine correctamente la solución óptima.

Nota:

- Método gráfico: maximizar o minimizar.
- Simplex v1.0: solamente maximizar.

---

## HU-03 - Ingresar función objetivo

> Como estudiante, quiero ingresar los coeficientes de X1 y X2 de la función objetivo para representar el problema de programación lineal.

Formato conceptual:

`Z = c1*X1 + c2*X2`

---

## HU-04 - Ingresar restricciones

> Como estudiante, quiero ingresar las restricciones del problema para construir el modelo matemático que será resuelto.

Cada restricción tendrá:

- coeficiente de `X1`;
- coeficiente de `X2`;
- operador;
- término independiente.

---

## HU-05 - Agregar o eliminar restricciones

> Como estudiante, quiero agregar o eliminar restricciones para adaptar la aplicación a problemas con diferente cantidad de condiciones.

---

## HU-06 - Resolver mediante método gráfico

> Como estudiante, quiero resolver un problema de dos variables mediante el método gráfico para visualizar la región factible y conocer su solución óptima.

---

## HU-07 - Visualizar procedimiento gráfico

> Como estudiante, quiero observar los vértices y la evaluación de la función objetivo para comprender cómo se obtuvo la solución del método gráfico.

---

## HU-08 - Resolver mediante Simplex

> Como estudiante, quiero resolver un problema de maximización mediante el método Simplex para obtener la solución óptima utilizando tablas iterativas.

---

## HU-09 - Visualizar iteraciones de Simplex

> Como estudiante, quiero observar las tablas de cada iteración del método Simplex para comprender el procedimiento utilizado por el programa.

---

## HU-10 - Limpiar el formulario

> Como estudiante, quiero limpiar los datos actuales para ingresar un nuevo problema sin reiniciar la aplicación.

---

# 3. Requisitos funcionales

## RF-01

La aplicación debe ejecutarse como programa de escritorio en Python.

## RF-02

La aplicación debe trabajar con exactamente dos variables de decisión: `X1` y `X2`.

## RF-03

El usuario debe poder seleccionar entre:

- Método gráfico.
- Método Simplex.

## RF-04

Para método gráfico el usuario debe poder seleccionar:

- Maximizar.
- Minimizar.

## RF-05

Para Simplex en la primera entrega solo se permitirá:

- Maximizar.

## RF-06

El usuario debe poder ingresar los dos coeficientes de la función objetivo.

## RF-07

El usuario debe poder ingresar una cantidad variable de restricciones.

## RF-08

La interfaz debe permitir agregar una restricción.

## RF-09

La interfaz debe permitir eliminar una restricción.

## RF-10

En método gráfico las restricciones podrán utilizar:

- `<=`
- `>=`

## RF-11

El método gráfico debe considerar implícitamente:

- `X1 >= 0`
- `X2 >= 0`

## RF-12

El método gráfico debe determinar los vértices factibles necesarios para resolver el problema.

## RF-13

El método gráfico debe evaluar la función objetivo en cada vértice factible.

## RF-14

El método gráfico debe seleccionar el vértice con mejor valor de `Z` según se maximice o minimice.

## RF-15

El método gráfico debe mostrar una gráfica estática con:

- restricciones;
- región factible;
- vértices;
- solución óptima.

## RF-16

Simplex v1.0 debe aceptar solamente restricciones `<=`.

## RF-17

Simplex v1.0 asumirá términos independientes `b >= 0`.

## RF-18

Simplex debe añadir automáticamente las variables de holgura necesarias.

## RF-19

Simplex debe construir una tabla inicial.

## RF-20

La fila inicial de la función objetivo seguirá la convención:

`Z - c1*X1 - c2*X2 = 0`

## RF-21

Simplex debe determinar la columna pivote.

## RF-22

Simplex debe determinar la fila pivote mediante las razones correspondientes.

## RF-23

Simplex debe convertir el elemento pivote en `1`.

## RF-24

Simplex debe convertir en `0` los demás elementos de la columna pivote.

## RF-25

Simplex debe repetir el procedimiento hasta llegar a la tabla óptima para los casos normales contemplados.

## RF-26

Simplex debe mostrar cada tabla generada.

## RF-27

Simplex debe mostrar, como mínimo:

- variable entrante;
- variable saliente;
- elemento pivote;
- tabla resultante.

## RF-28

Al finalizar Simplex se deben mostrar:

- `X1`;
- `X2`;
- valor óptimo de `Z`.

## RF-29

La aplicación debe incluir un botón `Resolver`.

## RF-30

La aplicación debe incluir un botón `Limpiar`.

---

# 4. Requisitos no funcionales

## RNF-01 - Simplicidad

El código debe privilegiar soluciones sencillas sobre implementaciones sofisticadas.

## RNF-02 - Legibilidad

Las funciones, variables y clases deben tener nombres descriptivos.

## RNF-03 - Modularidad

Aunque todo el proyecto se entregue en un archivo `.py`, las responsabilidades deben estar separadas mediante funciones y/o clases.

## RNF-04 - Explicabilidad

El estudiante debe poder seguir el flujo del algoritmo y explicar sus pasos.

## RNF-05 - Dependencias

Las librerías deben utilizarse como apoyo.

No se debe utilizar una función que resuelva automáticamente el método completo como reemplazo de la implementación.

## RNF-06 - Interfaz

La interfaz será sencilla, limpia y mínimamente decorada.

## RNF-07 - Resultados

Los resultados se mostrarán dentro de la misma aplicación.

## RNF-08 - Gráfica

La gráfica será estática.

## RNF-09 - Compatibilidad del código

Se evitarán dependencias innecesarias para facilitar la ejecución del programa en otro equipo.

---

# 5. Entradas

## Método gráfico

El usuario proporcionará:

- objetivo: max/min;
- `c1`;
- `c2`;
- para cada restricción:
  - `a1`;
  - `a2`;
  - operador `<=` o `>=`;
  - `b`.

## Simplex v1.0

El usuario proporcionará:

- objetivo: max;
- `c1`;
- `c2`;
- para cada restricción:
  - `a1`;
  - `a2`;
  - `b`.

Todas las restricciones se interpretarán como:

`a1*X1 + a2*X2 <= b`

---

# 6. Salidas

## Método gráfico

Mostrar:

```text
Modelo

Vértices factibles:
V1 = (...)
V2 = (...)
...

Evaluación:
Z(V1) = ...
Z(V2) = ...
...

Solución óptima:
X1 = ...
X2 = ...
Z  = ...
```

Y una gráfica.

## Método Simplex

Mostrar algo conceptualmente similar a:

```text
Tabla inicial

Variable entrante: X1
Variable saliente: S2
Pivote: ...

Iteración 1
[tabla]

Variable entrante: X2
Variable saliente: S1
Pivote: ...

Iteración 2
[tabla]

Solución:
X1 = ...
X2 = ...
Z = ...
```

La representación exacta se decidirá durante la implementación buscando que sea fácil de leer en Tkinter.

---

# 7. Casos que se usarán

Las pruebas manuales se realizarán únicamente con ejercicios compatibles con el alcance.

Para Simplex se utilizarán modelos con:

- dos variables;
- restricciones `<=`;
- `b >= 0`;
- solución normal.

No se utilizarán en las pruebas de v1.0 problemas que exijan:

- Gran M;
- dos fases;
- variables artificiales;
- Simplex dual;
- detección de degeneración;
- restricciones `>=` directas;
- restricciones `=`.

---

# 8. Posibles mejoras futuras

Estas ideas no pertenecen a la primera entrega:

- Simplex de minimización.
- Más de dos variables.
- Gran M.
- Dos fases.
- Restricciones `>=` en Simplex.
- Restricciones `=`.
- Casos no acotados.
- Casos infactibles.
- Soluciones múltiples.
- Degeneración.
- Transformación automática de límites mínimos.
- Uso de fracciones exactas.
- Exportar resultados.
- Guardar ejercicios.
- Historial.
- Validaciones avanzadas.
- Pruebas automatizadas.
- Temas visuales.
- Más opciones de gráficos.

---

# 9. Criterio interno de terminado para v1.0

Aunque el profesor no exigió criterios de aceptación formales, internamente la primera entrega se considerará lista cuando:

- la interfaz abra correctamente;
- se puedan agregar y eliminar restricciones;
- el método gráfico resuelva al menos varios ejercicios manuales conocidos de max y min;
- la gráfica corresponda con los resultados;
- Simplex max genere correctamente sus iteraciones para ejercicios básicos;
- los resultados coincidan con cálculos realizados manualmente;
- todo esté contenido en un solo `.py`;
- el código sea comprensible;
- estén preparados los diagramas;
- estén redactadas las historias de usuario;
- el informe tenga todas las secciones solicitadas;
- el repositorio muestre el avance por versiones.
