# ESTRUCTURA INICIAL DEL INFORME
## Working Paper - Calculadora de Programacion Lineal

**Estado:** esquema de v0.1

**Autor:** Santiago Andres Walteros Corredor

**Formato final previsto:** Word y PDF con plantilla Working Paper de IEEE

Este archivo organiza el contenido que se redactara durante el desarrollo. No es
todavia el informe final y no debe contener resultados que aun no se hayan
obtenido.

---

## Datos de portada pendientes

- Titulo definitivo.
- Nombre de la institucion.
- Programa academico.
- Asignatura.
- Docente.
- Correo institucional, si la plantilla lo exige.
- Fecha de entrega.

Titulo provisional:

> Diseno e implementacion de una calculadora de programacion lineal mediante los
> metodos grafico y Simplex

---

## Resumen

Redactar al finalizar una sintesis breve que incluya:

- problema abordado;
- objetivo de la aplicacion;
- metodos implementados;
- tecnologias utilizadas;
- resultados principales.

No incluir resultados numericos hasta completar las pruebas de v0.5.

## Palabras clave

Programacion lineal, metodo grafico, metodo Simplex, optimizacion, Python.

---

## 1. Introduccion

Desarrollar:

- importancia de la optimizacion en la toma de decisiones;
- utilidad de la programacion lineal;
- necesidad de representar el procedimiento y no solo el resultado;
- objetivo general del laboratorio;
- alcance de la primera entrega.

Extension prevista: entre tres y cinco parrafos breves.

---

## 2. Referente teorico

### 2.1 Programacion lineal

- Definicion.
- Variables de decision.
- Funcion objetivo.
- Restricciones.
- Condiciones de no negatividad.

### 2.2 Region factible y vertices

- Interpretacion geometrica.
- Intersecciones.
- Factibilidad.
- Evaluacion del objetivo en puntos extremos.

### 2.3 Metodo grafico

- Alcance para dos variables.
- Procedimiento de maximizacion y minimizacion.
- Ventajas y limitaciones.

### 2.4 Metodo Simplex

- Forma estandar utilizada.
- Variables de holgura.
- Tabla inicial.
- Variable entrante y saliente.
- Elemento pivote.
- Operaciones elementales y condicion de parada.

Las fuentes se citaran con el estilo bibliografico solicitado por la plantilla.

---

## 3. Procedimiento

### 3.1 Analisis del problema

- Alcance funcional.
- Historias de usuario.
- Restricciones de la primera version.

### 3.2 Diseno del sistema

- Arquitectura basica.
- Diagrama de clases.
- Secuencias del metodo grafico y Simplex.
- Bosquejo de interfaz.

### 3.3 Tecnologias

- Python.
- Tkinter.
- NumPy como apoyo numerico.
- Matplotlib para la representacion grafica.

### 3.4 Implementacion incremental

Describir cada version despues de verificarla:

| Version | Contenido | Evidencia pendiente |
|---|---|---|
| v0.1 | Planeacion y diseno | Diagramas y documentos |
| v0.2 | Interfaz y captura del modelo | Captura del formulario |
| v0.3 | Metodo grafico | Vertices y grafica |
| v0.4 | Simplex de maximizacion | Tablas de iteracion |
| v0.5 | Integracion y pruebas | Comparacion de ejercicios |
| v1.0 | Primera entrega | Codigo e informe final |

### 3.5 Metodo grafico implementado

Procedimiento matemático implementado en el primer incremento de v0.3:

- generación de candidatos mediante intersecciones entre restricciones y ejes;
- solución de sistemas de dos ecuaciones mediante determinantes;
- comprobación de restricciones y condiciones de no negatividad;
- eliminación de puntos repetidos por tolerancia numérica;
- evaluación de la función objetivo en los vértices factibles;
- selección del máximo o mínimo solicitado.

Representación visual implementada en el cierre de v0.3:

- trazado de las fronteras de cada restricción;
- sombreado del polígono formado por los vértices factibles;
- identificación de vértices y solución óptima;
- límites automáticos, ejes, cuadrícula y leyenda;
- integración de la figura estática dentro de la interfaz Tkinter.

### 3.6 Simplex implementado

Primer incremento de v0.4 implementado:

- validación de maximización, restricciones `<=` y términos independientes no
  negativos;
- creación de una variable de holgura por restricción;
- construcción de columnas `X1`, `X2`, `S1...Sm` y `CR`;
- registro de las variables básicas iniciales;
- construcción de la fila `Z - c1X1 - c2X2 = 0`;
- presentación alineada de la tabla dentro de la interfaz.

Pendiente para completar v0.4:

- selección de pivotes;
- operaciones por filas;
- almacenamiento de iteraciones;
- lectura de la solución.

---

## 4. Resultados

Esta seccion se completara con evidencia real de v0.5.

### 4.1 Pruebas del metodo grafico

Incluir dos ejercicios de maximizacion y dos de minimizacion.

| Caso | Resultado manual | Resultado del programa | Coincide |
|---|---:|---:|---|
| Grafico max 1 | Pendiente | Pendiente | Pendiente |
| Grafico max 2 | Pendiente | Pendiente | Pendiente |
| Grafico min 1 | Pendiente | Pendiente | Pendiente |
| Grafico min 2 | Pendiente | Pendiente | Pendiente |

### 4.2 Pruebas del metodo Simplex

Incluir tres ejercicios compatibles con el alcance de v1.0.

| Caso | Resultado manual | Resultado del programa | Coincide |
|---|---:|---:|---|
| Simplex max 1 | Pendiente | Pendiente | Pendiente |
| Simplex max 2 | Pendiente | Pendiente | Pendiente |
| Simplex max 3 | Pendiente | Pendiente | Pendiente |

### 4.3 Evidencias graficas pendientes

- Captura de la interfaz principal.
- Captura de una region factible.
- Captura de los vertices evaluados.
- Captura de una tabla inicial de Simplex.
- Captura de una iteracion y de la solucion final.

Cada figura debera incluir numero, titulo y explicacion breve.

---

## 5. Conclusiones

Redactar al terminar las pruebas. Las conclusiones deberan responder:

- que se aprendio sobre el modelado matematico;
- como se relacionan los vertices con el optimo;
- como funciona el pivoteo en Simplex;
- que ventajas tuvo el desarrollo incremental;
- cuales son las limitaciones reales de v1.0.

No presentar funcionalidades futuras como si ya estuvieran implementadas.

---

## Bibliografia

Agregar unicamente fuentes consultadas y citadas en el texto. Priorizar:

- material de la asignatura;
- libros academicos de investigacion de operaciones;
- documentacion oficial de Python, Tkinter, NumPy y Matplotlib cuando se cite la
  implementacion.

---

## Control de avance del informe

- [x] Estructura inicial definida.
- [ ] Datos institucionales completos.
- [ ] Introduccion redactada.
- [ ] Referente teorico redactado y citado.
- [ ] Procedimiento actualizado con la implementacion real.
- [ ] Resultados y capturas incorporados.
- [ ] Conclusiones redactadas.
- [ ] Bibliografia revisada.
- [ ] Documento adaptado a Word con plantilla IEEE.
- [ ] PDF final revisado visualmente.
