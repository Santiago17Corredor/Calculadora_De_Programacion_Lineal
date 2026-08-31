# Calculadora de Programación Lineal

Aplicación de escritorio en Python para construir y resolver problemas de
programación lineal con dos variables de decisión.

La primera entrega contempla:

- método gráfico para maximización y minimización;
- método Simplex para maximización;
- interfaz gráfica con Tkinter;
- visualización del procedimiento y los resultados.

El proyecto se desarrolla de forma incremental. La versión actual es `v0.5`,
con el método gráfico y Simplex de maximización integrados en la misma interfaz.

En esta versión, el botón `Resolver` valida las entradas, muestra el modelo,
calcula los vértices factibles y selecciona el máximo o mínimo mediante el método
gráfico. Para Simplex agrega variables de holgura y muestra la tabla inicial; el
pivoteo selecciona variables entrantes y salientes, calcula razones, conserva
cada tabla y muestra los valores finales de `X1`, `X2` y `Z`.

Cuando se modifica el formulario, la aplicación descarta automáticamente el
resultado anterior para evitar mostrar una solución que ya no corresponde con
los datos visibles.

La gráfica presenta las restricciones, la región factible, los vértices y la
solución óptima dentro de la misma ventana.

## Dependencias

- Python 3.
- Tkinter.
- Matplotlib.

Matplotlib puede instalarse con:

```text
python -m pip install matplotlib
```

## Ejecución

```text
python programacion_lineal.py
```

## Documentacion

- [Contexto](contexto%2C%20requisitos%20y%20plan%20de%20desarrollo/CONTEXTO.md)
- [Requisitos](contexto%2C%20requisitos%20y%20plan%20de%20desarrollo/REQUISITOS.md)
- [Plan de desarrollo](contexto%2C%20requisitos%20y%20plan%20de%20desarrollo/PLAN_DESARROLLO.md)
- [Diseño del sistema](contexto%2C%20requisitos%20y%20plan%20de%20desarrollo/DISENO.md)
- [Estructura del informe](contexto%2C%20requisitos%20y%20plan%20de%20desarrollo/ESTRUCTURA_INFORME.md)
- [Pruebas manuales](contexto%2C%20requisitos%20y%20plan%20de%20desarrollo/PRUEBAS_MANUALES.md)

## Informe de la primera entrega

- [Documento en Word](output/document/Informe_Calculadora_Programacion_Lineal.docx)
- [Documento en PDF](output/pdf/Informe_Calculadora_Programacion_Lineal.pdf)

**Autor:** Santiago Andrés Walteros Corredor
