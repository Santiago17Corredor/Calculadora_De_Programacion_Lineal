# CONTEXTO DEL PROYECTO
## Calculadora de Programación Lineal - Laboratorio de Optimización

**Fecha límite primera entrega:** viernes 4 de septiembre de 2026  
**Modalidad:** trabajo individual  
**Lenguaje:** Python  
**Tipo de aplicación:** aplicación de escritorio con interfaz gráfica  
**Repositorio:** GitHub, trabajando sobre una rama principal y avanzando por versiones.

---

## 1. Objetivo general del laboratorio

Diseñar y desarrollar un programa en Python que permita construir y resolver modelos matemáticos de programación lineal.

La primera entrega debe incluir:

- Método gráfico para problemas de **maximización y minimización**.
- Método Simplex para problemas de **maximización**.
- Interfaz gráfica de escritorio.
- Diseño previo sencillo del sistema.
- Historias de usuario.
- Diagramas básicos de diseño.
- Informe técnico en formato **Working Paper de IEEE**.

Una semana después se complementará el proyecto con:

- Método Simplex para problemas de **minimización**.
- Complemento correspondiente del informe.

---

## 2. Filosofía del proyecto

El proyecto debe ser:

- Sencillo.
- Funcional.
- Fácil de explicar.
- Fácil de leer.
- Modular aunque se entregue en un solo archivo `.py`.
- Desarrollado paso a paso.
- Construido por versiones en GitHub.
- Sin funcionalidades innecesarias para la primera entrega.

La prioridad es que el estudiante pueda comprender y explicar el código, no construir una calculadora profesional o cubrir todos los casos posibles de programación lineal.

---

## 3. Restricciones generales del alcance

La aplicación trabajará únicamente con dos variables de decisión:

- `X1`
- `X2`

Se asumen siempre las condiciones de no negatividad:

- `X1 >= 0`
- `X2 >= 0`

La cantidad de restricciones será elegida por el usuario.

---

## 4. Método gráfico

### Alcance

El método gráfico deberá resolver:

- Maximización.
- Minimización.
- Dos variables de decisión.
- Cantidad variable de restricciones.
- Restricciones con operadores:
  - `<=`
  - `>=`

No se implementarán restricciones de igualdad en la primera versión.

### Procedimiento que debe representar el programa

1. Construir las rectas correspondientes a las restricciones.
2. Graficar las restricciones.
3. Determinar la región factible.
4. Encontrar los vértices relevantes de la región factible.
5. Evaluar la función objetivo en los vértices.
6. Comparar los valores obtenidos.
7. Seleccionar el valor máximo o mínimo según el objetivo.
8. Mostrar la solución óptima.

### Salida esperada

La aplicación debe mostrar de forma sencilla:

- Modelo ingresado.
- Vértices encontrados.
- Evaluación de la función objetivo en cada vértice.
- Solución óptima.
- Valor óptimo de `Z`.
- Gráfica estática con:
  - restricciones;
  - región factible;
  - vértices;
  - punto óptimo.

No se requiere zoom, exportación ni interacción avanzada con la gráfica.

---

## 5. Método Simplex - primera entrega

### Alcance

La primera entrega implementará solamente Simplex para **maximización**.

Para mantener el algoritmo básico, el programa aceptará problemas de la forma:

```text
Max Z = c1*X1 + c2*X2

s.a.

a11*X1 + a12*X2 <= b1
a21*X1 + a22*X2 <= b2
...
am1*X1 + am2*X2 <= bm

X1, X2 >= 0
```

Para esta versión se trabajará con:

- Dos variables de decisión.
- Cantidad variable de restricciones.
- Restricciones `<=`.
- Términos independientes `b >= 0`.
- Variables de holgura.
- Casos académicos normales con solución convencional.

### Convención observada en el taller del profesor

El taller resuelto del profesor muestra el Simplex mediante tablas.

La lógica que se debe intentar conservar visualmente es:

1. Escribir la función objetivo en la forma:

   `Z - c1*X1 - c2*X2 = 0`

2. Agregar variables de holgura a las restricciones `<=`.

3. Construir una tabla con columnas semejantes a:

   - `VB` - variable básica;
   - variables de decisión;
   - variables de holgura;
   - `CR` - columna de resultados.

4. En la fila de `Z`, los coeficientes de las variables de decisión aparecen inicialmente negativos para problemas de maximización.

5. Seleccionar la columna pivote a partir de la fila `Z`.

6. Calcular las razones necesarias para determinar la fila pivote.

7. Convertir el pivote en `1`.

8. Hacer ceros en el resto de su columna mediante operaciones elementales por filas.

9. Repetir hasta llegar a una tabla óptima.

10. Leer los valores de las variables básicas y el valor final de `Z`.

### Observación importante sobre el taller

En los ejercicios del profesor aparecen condiciones adicionales como límites mínimos o relaciones entre variables. En esos casos el procedimiento manual realiza sustituciones antes de aplicar Simplex, por ejemplo:

- `X1 = 20 + Y1`
- `X2 = 10 + Y2`
- `X2 = X1 + Y`
- `X2 = 4X1 + Y`

Estas transformaciones forman parte del procedimiento mostrado en el taller, pero **no se incluirán en la primera versión automática del programa**.

La versión inicial recibirá directamente problemas ya compatibles con el Simplex básico indicado anteriormente. Automatizar esas transformaciones se considera una posible mejora futura.

---

## 6. Casos especiales fuera del alcance inicial

La primera entrega no pretende resolver automáticamente:

- Problemas no acotados.
- Problemas sin solución factible.
- Soluciones múltiples.
- Degeneración.
- Restricciones `=` en Simplex.
- Restricciones `>=` en Simplex.
- Gran M.
- Método de dos fases.
- Simplex dual.
- Variables artificiales.
- Transformaciones automáticas de límites mínimos.
- Más de dos variables de decisión.
- Validaciones avanzadas.
- Fracciones exactas.
- Exportación a PDF, Excel o archivos externos.
- Persistencia de problemas.
- Historial de ejercicios.

Los ejercicios usados para demostrar el programa serán casos normales y compatibles con el alcance definido.

---

## 7. Interfaz gráfica

La interfaz será limpia, sencilla y mínimamente decorada.

Se usará **Tkinter** por ser una opción simple e incluida normalmente con Python.

La pantalla principal deberá permitir:

1. Seleccionar método:
   - Método gráfico.
   - Método Simplex.

2. Seleccionar objetivo:
   - Maximizar.
   - Minimizar.

   En la primera entrega, si se selecciona Simplex se permitirá solamente maximizar.

3. Ingresar coeficientes de:

   `Z = [ ] X1 + [ ] X2`

4. Ingresar restricciones:

   `[ ] X1 + [ ] X2 [<= / >=] [ ]`

5. Agregar restricciones con un botón `+`.

6. Eliminar restricciones con un botón `-`.

7. Ejecutar con un botón `Resolver`.

8. Limpiar el formulario.

9. Mostrar procedimiento y resultados en la misma aplicación.

10. Mostrar la gráfica cuando se utilice el método gráfico.

La interfaz de referencia suministrada por el estudiante sirve solamente como inspiración visual y no necesita copiarse exactamente.

---

## 8. Librerías

### Tkinter

Uso:

- interfaz gráfica;
- botones;
- cuadros de entrada;
- listas desplegables;
- panel de resultados.

### NumPy

Uso permitido:

- arreglos;
- operaciones numéricas;
- apoyo con matrices y cálculos repetitivos.

NumPy será una herramienta auxiliar y no sustituirá la lógica de los métodos.

### Matplotlib

Uso:

- graficar restricciones;
- sombrear región factible;
- mostrar vértices y solución óptima.

### SciPy

Aunque el material del laboratorio menciona `scipy.optimize.linprog`, **no se utilizará como motor principal de solución**, porque resolvería directamente el problema y ocultaría la implementación del método.

Podría utilizarse posteriormente únicamente para verificación, pero no forma parte del diseño inicial.

---

## 9. Organización del código

Aunque la implementación final estará contenida en un solo archivo:

`programacion_lineal.py`

el código debe estar dividido lógicamente por responsabilidades.

Diseño conceptual inicial:

```text
AplicacionPL
    |
    +--> ProblemaPL
    |
    +--> MetodoGrafico
    |
    +--> MetodoSimplex
```

Responsabilidades:

### `ProblemaPL`

Representa los datos del problema:

- tipo de objetivo;
- coeficientes de la función objetivo;
- restricciones;
- operadores;
- términos independientes.

### `MetodoGrafico`

Responsable de:

- calcular intersecciones;
- comprobar vértices;
- evaluar la función objetivo;
- seleccionar el óptimo;
- preparar la información de la gráfica.

### `MetodoSimplex`

Responsable de:

- construir la tabla inicial;
- agregar holguras;
- seleccionar pivotes;
- hacer operaciones por filas;
- guardar las iteraciones;
- obtener la solución final.

### `AplicacionPL`

Responsable de:

- construir la interfaz;
- leer entradas;
- seleccionar el método;
- llamar al algoritmo correspondiente;
- mostrar procedimiento, resultados y gráfica.

Este diseño podrá simplificarse si durante la implementación alguna clase no aporta claridad. El objetivo del UML es representar una arquitectura comprensible, no obligar a sobrecargar el código con POO innecesaria.

---

## 10. Diseño requerido

Para la primera entrega se prepararán como mínimo:

- Arquitectura básica.
- Diagrama de clases.
- Diagrama de secuencia.
- Historias de usuario.

Los diagramas deben ser pequeños y fáciles de explicar.

---

## 11. Informe

El informe seguirá el formato **Working Paper de IEEE** y deberá contener como mínimo:

1. Título de la práctica.
2. Autores.
3. Introducción.
4. Referente teórico.
5. Procedimiento.
6. Resultados.
7. Conclusiones.
8. Bibliografía.

La evidencia final de la práctica será un archivo comprimido que contenga:

- código fuente;
- informe técnico.

El documento debe reflejar tanto la implementación técnica como la comprensión teórica de los métodos.

El informe se elaborará inicialmente en Word y posteriormente podrá convertirse a PDF.

---

## 12. Entregas

### Primera entrega - v1.0

Incluye:

- diseño;
- historias de usuario;
- interfaz;
- método gráfico max/min;
- Simplex max;
- resultados;
- informe hasta ese punto.

**Fecha:** viernes 4 de septiembre de 2026.

### Segunda entrega - v2.0

Incluye:

- Simplex de minimización;
- ajustes necesarios;
- complemento del informe.

---

## 13. Principio de trabajo con ChatGPT Desktop

ChatGPT Desktop debe trabajar de manera incremental.

Regla principal:

> Trabajar únicamente en la fase indicada. No generar toda la aplicación de una vez. Antes de avanzar de versión, comprobar que la versión actual funciona y que el estudiante comprende lo realizado.

Además:

- explicar antes de complicar;
- priorizar código sencillo;
- evitar funcionalidades que no pertenezcan a la versión actual;
- no introducir librerías que resuelvan todo el algoritmo;
- conservar un único archivo `.py`;
- realizar cambios pequeños y verificables;
- preparar commits por versión.

---

## 14. Referencias internas del proyecto

Material base suministrado:

- Enunciado/información del laboratorio.
- Imagen de referencia de interfaz.
- `Actividad N°2 - Taller Programación Lineal (1).pdf`, con ejercicios resueltos manualmente mediante método gráfico y Simplex siguiendo el estilo usado en clase.

Este documento de contexto debe mantenerse estable. Los cambios de alcance posteriores deben registrarse explícitamente antes de modificar el programa.
