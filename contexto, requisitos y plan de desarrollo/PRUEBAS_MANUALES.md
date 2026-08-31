# Pruebas manuales de v0.5

Fecha de verificación: 31 de agosto de 2026.

Estas pruebas se ejecutaron desde la interfaz gráfica de la aplicación. En los
casos del método gráfico también se comprobó que aparecieran la región factible,
los vértices y el punto óptimo. En los casos de Simplex se revisaron las tablas
de cada iteración y la solución final.

Los resultados numéricos se compararon con la solución manual, usando una
tolerancia de `0.000001` para valores decimales.

## G-01 - Maximización por método gráfico

### Problema

```text
Max Z = 30X1 + 50X2

s.a.
X1 + 3X2 <= 150
X1 + X2 <= 70
X1, X2 >= 0
```

- Resultado manual: `X1 = 30`, `X2 = 40`, `Z = 2900`.
- Resultado del programa: `X1 = 30`, `X2 = 40`, `Z = 2900`.
- Coincide: sí.
- Observaciones: se encontraron cuatro vértices factibles y la gráfica señaló
  correctamente el punto óptimo.

## G-02 - Maximización con cotas inferiores

### Problema

```text
Max Z = 30X1 + 50X2

s.a.
X1 + 3X2 <= 200
X1 + X2 <= 100
X1 >= 20
X2 >= 10
X1, X2 >= 0
```

- Resultado manual: `X1 = 50`, `X2 = 50`, `Z = 4000`.
- Resultado del programa: `X1 = 50`, `X2 = 50`, `Z = 4000`.
- Coincide: sí.
- Observaciones: los vértices factibles fueron `(20, 10)`, `(20, 60)`,
  `(50, 50)` y `(90, 10)`.

## G-03 - Minimización con una restricción mayor o igual

### Problema

```text
Min Z = 2X1 + 3X2

s.a.
X1 + X2 >= 4
X1 <= 5
X2 <= 5
X1, X2 >= 0
```

- Resultado manual: `X1 = 4`, `X2 = 0`, `Z = 8`.
- Resultado del programa: `X1 = 4`, `X2 = 0`, `Z = 8`.
- Coincide: sí.
- Observaciones: se encontraron cinco vértices factibles y se seleccionó el
  menor valor de la función objetivo.

## G-04 - Minimización con varias restricciones

### Problema

```text
Min Z = X1 + X2

s.a.
X1 + 2X2 >= 8
3X1 + X2 >= 9
X1 <= 10
X2 <= 10
X1, X2 >= 0
```

- Resultado manual: `X1 = 2`, `X2 = 3`, `Z = 5`.
- Resultado del programa: `X1 = 2`, `X2 = 3`, `Z = 5`.
- Coincide: sí.
- Observaciones: se encontraron seis vértices factibles y el cruce de las dos
  restricciones inferiores produjo la solución óptima.

## S-01 - Simplex con el caso base

### Problema

```text
Max Z = 30X1 + 50X2

s.a.
X1 + 3X2 <= 150
X1 + X2 <= 70
X1, X2 >= 0
```

- Resultado manual: `X1 = 30`, `X2 = 40`, `Z = 2900`.
- Resultado del programa: `X1 = 30`, `X2 = 40`, `Z = 2900`.
- Coincide: sí.
- Observaciones: el método llegó a la solución óptima después de dos
  iteraciones.

## S-02 - Simplex con dos restricciones

### Problema

```text
Max Z = 3X1 + 2X2

s.a.
X1 + X2 <= 4
2X1 + X2 <= 5
X1, X2 >= 0
```

- Resultado manual: `X1 = 1`, `X2 = 3`, `Z = 9`.
- Resultado del programa: `X1 = 1`, `X2 = 3`, `Z = 9`.
- Coincide: sí.
- Observaciones: las tablas mostraron dos pivoteos y conservaron las variables
  de holgura necesarias.

## S-03 - Simplex con tres restricciones

### Problema

```text
Max Z = 3X1 + 5X2

s.a.
X1 <= 4
2X2 <= 12
3X1 + 2X2 <= 18
X1, X2 >= 0
```

- Resultado manual: `X1 = 2`, `X2 = 6`, `Z = 36`.
- Resultado del programa: `X1 = 2`, `X2 = 6`, `Z = 36`.
- Coincide: sí.
- Observaciones: el método procesó tres variables de holgura y alcanzó el
  óptimo después de dos iteraciones.

## Resumen

| Caso | Método | Objetivo | Solución | Coincide |
|---|---|---|---|---|
| G-01 | Gráfico | Maximizar | `(30, 40), Z = 2900` | Sí |
| G-02 | Gráfico | Maximizar | `(50, 50), Z = 4000` | Sí |
| G-03 | Gráfico | Minimizar | `(4, 0), Z = 8` | Sí |
| G-04 | Gráfico | Minimizar | `(2, 3), Z = 5` | Sí |
| S-01 | Simplex | Maximizar | `(30, 40), Z = 2900` | Sí |
| S-02 | Simplex | Maximizar | `(1, 3), Z = 9` | Sí |
| S-03 | Simplex | Maximizar | `(2, 6), Z = 36` | Sí |

Resultado general: **7 de 7 casos coinciden con la solución manual**.
