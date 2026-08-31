"""Calculadora de programación lineal desarrollada de forma incremental.

Versión v0.4: conserva el método gráfico completo y ejecuta una iteración del
método Simplex de maximización. El ciclo completo se incorporará después.
"""

import math
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ProblemaPL:
    """Representa los datos de un problema con dos variables de decisión."""

    def __init__(self, objetivo, coeficientes_objetivo, restricciones):
        self.objetivo = objetivo
        self.coeficientes_objetivo = coeficientes_objetivo
        self.restricciones = restricciones

    @staticmethod
    def formatear_numero(valor):
        """Muestra enteros sin decimal y conserva los decimales necesarios."""
        numero = float(valor)
        if math.isclose(numero, round(numero), abs_tol=1e-9):
            return str(int(round(numero)))
        return f"{valor:.10g}"

    @classmethod
    def _formatear_expresion(cls, coeficiente_x1, coeficiente_x2):
        """Construye una expresión legible con X1 y X2."""
        primer_termino = f"{cls.formatear_numero(coeficiente_x1)}X1"
        signo = "+" if coeficiente_x2 >= 0 else "-"
        segundo_coeficiente = cls.formatear_numero(abs(coeficiente_x2))
        return f"{primer_termino} {signo} {segundo_coeficiente}X2"

    def formatear_modelo(self):
        """Devuelve el modelo matemático como texto."""
        tipo_objetivo = "Max" if self.objetivo == "Maximizar" else "Min"
        c1, c2 = self.coeficientes_objetivo
        lineas = [
            f"{tipo_objetivo} Z = {self._formatear_expresion(c1, c2)}",
            "",
            "s.a.",
        ]

        for a1, a2, operador, termino_independiente in self.restricciones:
            expresion = self._formatear_expresion(a1, a2)
            valor_b = self.formatear_numero(termino_independiente)
            lineas.append(f"{expresion} {operador} {valor_b}")

        lineas.extend(["", "X1, X2 >= 0"])
        return "\n".join(lineas)


class MetodoGrafico:
    """Resuelve problemas de dos variables mediante sus vértices factibles."""

    TOLERANCIA = 1e-7

    def resolver(self, problema):
        """Calcula vértices, evaluaciones y solución óptima."""
        candidatos = self.calcular_intersecciones(problema)
        vertices = self.obtener_vertices_factibles(problema, candidatos)

        if not vertices:
            raise ValueError(
                "No se encontraron vértices factibles para el modelo ingresado."
            )

        evaluaciones = self.evaluar_objetivo(problema, vertices)
        if problema.objetivo == "Maximizar":
            punto_optimo, valor_optimo = max(
                evaluaciones, key=lambda evaluacion: evaluacion[1]
            )
        else:
            punto_optimo, valor_optimo = min(
                evaluaciones, key=lambda evaluacion: evaluacion[1]
            )

        return {
            "candidatos": candidatos,
            "vertices": vertices,
            "evaluaciones": evaluaciones,
            "punto_optimo": punto_optimo,
            "valor_optimo": valor_optimo,
        }

    def calcular_intersecciones(self, problema):
        """Genera intersecciones entre fronteras y con ambos ejes."""
        candidatos = [(0.0, 0.0)]

        for a1, a2, _operador, termino_independiente in problema.restricciones:
            if abs(a1) > self.TOLERANCIA:
                candidatos.append((termino_independiente / a1, 0.0))
            if abs(a2) > self.TOLERANCIA:
                candidatos.append((0.0, termino_independiente / a2))

        for indice, primera in enumerate(problema.restricciones):
            for segunda in problema.restricciones[indice + 1 :]:
                interseccion = self._interseccion_dos_rectas(primera, segunda)
                if interseccion is not None:
                    candidatos.append(interseccion)

        return candidatos

    def _interseccion_dos_rectas(self, primera, segunda):
        """Resuelve un sistema de dos fronteras mediante determinantes."""
        a1, a2, _operador_1, b1 = primera
        c1, c2, _operador_2, b2 = segunda
        determinante = a1 * c2 - a2 * c1

        if abs(determinante) <= self.TOLERANCIA:
            return None

        x1 = (b1 * c2 - a2 * b2) / determinante
        x2 = (a1 * b2 - b1 * c1) / determinante
        return x1, x2

    def obtener_vertices_factibles(self, problema, candidatos):
        """Conserva puntos que cumplen restricciones y no negatividad."""
        vertices = []

        for x1, x2 in candidatos:
            punto = (
                0.0 if abs(x1) <= self.TOLERANCIA else x1,
                0.0 if abs(x2) <= self.TOLERANCIA else x2,
            )
            if not self._es_factible(problema, punto):
                continue
            if self._punto_repetido(punto, vertices):
                continue
            vertices.append(punto)

        return sorted(vertices, key=lambda punto: (punto[0], punto[1]))

    def _es_factible(self, problema, punto):
        """Comprueba todas las desigualdades para un punto candidato."""
        x1, x2 = punto
        if x1 < -self.TOLERANCIA or x2 < -self.TOLERANCIA:
            return False

        for a1, a2, operador, termino_independiente in problema.restricciones:
            lado_izquierdo = a1 * x1 + a2 * x2
            if operador == "<=" and lado_izquierdo > termino_independiente + self.TOLERANCIA:
                return False
            if operador == ">=" and lado_izquierdo < termino_independiente - self.TOLERANCIA:
                return False
        return True

    def _punto_repetido(self, punto, vertices):
        """Evita mostrar varias veces una misma intersección."""
        return any(
            abs(punto[0] - existente[0]) <= self.TOLERANCIA
            and abs(punto[1] - existente[1]) <= self.TOLERANCIA
            for existente in vertices
        )

    @staticmethod
    def evaluar_objetivo(problema, vertices):
        """Evalúa la función objetivo en cada vértice factible."""
        c1, c2 = problema.coeficientes_objetivo
        return [(punto, c1 * punto[0] + c2 * punto[1]) for punto in vertices]

    @staticmethod
    def ordenar_vertices(vertices):
        """Ordena los vértices alrededor de su centro para formar el polígono."""
        centro_x = sum(punto[0] for punto in vertices) / len(vertices)
        centro_y = sum(punto[1] for punto in vertices) / len(vertices)
        return sorted(
            vertices,
            key=lambda punto: math.atan2(punto[1] - centro_y, punto[0] - centro_x),
        )

    def calcular_limites_grafica(self, problema, vertices):
        """Obtiene límites positivos que permiten ver rectas y región factible."""
        valores_x = [punto[0] for punto in vertices if punto[0] >= 0]
        valores_y = [punto[1] for punto in vertices if punto[1] >= 0]

        for a1, a2, _operador, termino_independiente in problema.restricciones:
            if abs(a1) > self.TOLERANCIA:
                corte_x = termino_independiente / a1
                if corte_x > 0:
                    valores_x.append(corte_x)
            if abs(a2) > self.TOLERANCIA:
                corte_y = termino_independiente / a2
                if corte_y > 0:
                    valores_y.append(corte_y)

        limite_x = max(valores_x, default=1.0)
        limite_y = max(valores_y, default=1.0)
        return max(limite_x * 1.15, 1.0), max(limite_y * 1.15, 1.0)


class MetodoSimplex:
    """Construye las tablas del método Simplex de maximización."""

    TOLERANCIA = 1e-9
    MAX_ITERACIONES = 100

    def crear_tabla_inicial(self, problema):
        """Agrega holguras y crea la tabla correspondiente al modelo."""
        if problema.objetivo != "Maximizar":
            raise ValueError("Simplex v1.0 solo admite problemas de maximización.")
        if not problema.restricciones:
            raise ValueError("Simplex requiere al menos una restricción.")

        cantidad_restricciones = len(problema.restricciones)
        nombres_holguras = [
            f"S{indice}" for indice in range(1, cantidad_restricciones + 1)
        ]
        columnas = ["X1", "X2", *nombres_holguras, "CR"]
        variables_basicas = []
        tabla = []

        for indice, restriccion in enumerate(problema.restricciones):
            a1, a2, operador, termino_independiente = restriccion
            if operador != "<=":
                raise ValueError("Simplex v1.0 solo admite restricciones <=.")
            if termino_independiente < 0:
                raise ValueError("Simplex v1.0 requiere términos independientes b >= 0.")

            holguras = [0.0] * cantidad_restricciones
            holguras[indice] = 1.0
            tabla.append([a1, a2, *holguras, termino_independiente])
            variables_basicas.append(nombres_holguras[indice])

        c1, c2 = problema.coeficientes_objetivo
        fila_z = [-c1, -c2, *([0.0] * cantidad_restricciones), 0.0]
        tabla.append(fila_z)
        variables_basicas.append("Z")

        return {
            "columnas": columnas,
            "variables_basicas": variables_basicas,
            "tabla": tabla,
        }

    def resolver(self, problema):
        """Repite el pivoteo hasta obtener la tabla óptima."""
        tabla_inicial = self.crear_tabla_inicial(problema)
        estado_actual = tabla_inicial
        iteraciones = []

        while not self.es_optima(estado_actual):
            if len(iteraciones) >= self.MAX_ITERACIONES:
                raise ValueError(
                    "Se alcanzó el límite preventivo de iteraciones de Simplex."
                )
            estado_actual = self.realizar_iteracion(estado_actual)
            iteraciones.append(estado_actual)

        return {
            "tabla_inicial": tabla_inicial,
            "iteraciones": iteraciones,
            "solucion": self.leer_solucion(estado_actual),
        }

    def es_optima(self, estado_tabla):
        """Comprueba que la fila Z ya no contenga coeficientes negativos."""
        return all(
            coeficiente >= -self.TOLERANCIA
            for coeficiente in estado_tabla["tabla"][-1][:-1]
        )

    def leer_solucion(self, estado_tabla):
        """Lee X1, X2 y Z desde las variables básicas de la tabla final."""
        solucion = {"X1": 0.0, "X2": 0.0}
        for variable, fila in zip(
            estado_tabla["variables_basicas"][:-1], estado_tabla["tabla"][:-1]
        ):
            if variable in solucion:
                solucion[variable] = fila[-1]

        solucion["Z"] = estado_tabla["tabla"][-1][-1]
        return {
            nombre: self._normalizar_valor(valor)
            for nombre, valor in solucion.items()
        }

    def _normalizar_valor(self, valor):
        """Limpia ceros y enteros afectados por redondeo de punto flotante."""
        if abs(valor) <= self.TOLERANCIA:
            return 0.0
        entero_cercano = round(valor)
        if math.isclose(valor, entero_cercano, abs_tol=self.TOLERANCIA):
            return float(entero_cercano)
        return valor

    def realizar_iteracion(self, estado_tabla):
        """Ejecuta una iteración y conserva los datos que explican el pivoteo."""
        columna_pivote = self.seleccionar_columna_pivote(estado_tabla)
        fila_pivote, razones = self.seleccionar_fila_pivote(
            estado_tabla, columna_pivote
        )

        variable_entrante = estado_tabla["columnas"][columna_pivote]
        variable_saliente = estado_tabla["variables_basicas"][fila_pivote]
        pivote = estado_tabla["tabla"][fila_pivote][columna_pivote]
        nuevo_estado = self.pivotear(estado_tabla, fila_pivote, columna_pivote)
        nuevo_estado.update(
            {
                "variable_entrante": variable_entrante,
                "variable_saliente": variable_saliente,
                "pivote": pivote,
                "fila_pivote": fila_pivote,
                "columna_pivote": columna_pivote,
                "razones": razones,
                "variables_basicas_anteriores": estado_tabla[
                    "variables_basicas"
                ].copy(),
            }
        )
        return nuevo_estado

    def seleccionar_columna_pivote(self, estado_tabla):
        """Elige el coeficiente más negativo de la fila Z."""
        fila_z = estado_tabla["tabla"][-1]
        coeficientes = fila_z[:-1]
        valor_menor = min(coeficientes)

        if valor_menor >= -self.TOLERANCIA:
            raise ValueError("La tabla ya cumple la condición de optimalidad.")
        return coeficientes.index(valor_menor)

    def seleccionar_fila_pivote(self, estado_tabla, columna_pivote):
        """Calcula CR/coeficiente y elige la menor razón no negativa."""
        razones = []
        for fila in estado_tabla["tabla"][:-1]:
            coeficiente = fila[columna_pivote]
            if coeficiente > self.TOLERANCIA:
                razon = fila[-1] / coeficiente
                razones.append(0.0 if abs(razon) <= self.TOLERANCIA else razon)
            else:
                razones.append(None)

        razones_validas = [
            (indice, razon)
            for indice, razon in enumerate(razones)
            if razon is not None and razon >= -self.TOLERANCIA
        ]
        if not razones_validas:
            raise ValueError("No existe una razón válida para seleccionar la fila pivote.")

        fila_pivote, _razon = min(razones_validas, key=lambda dato: dato[1])
        return fila_pivote, razones

    def pivotear(self, estado_tabla, fila_pivote, columna_pivote):
        """Convierte el pivote en uno y hace ceros en el resto de su columna."""
        tabla_original = estado_tabla["tabla"]
        pivote = tabla_original[fila_pivote][columna_pivote]
        if abs(pivote) <= self.TOLERANCIA:
            raise ValueError("El elemento pivote no puede ser cero.")

        fila_normalizada = [valor / pivote for valor in tabla_original[fila_pivote]]
        nueva_tabla = []

        for indice, fila in enumerate(tabla_original):
            if indice == fila_pivote:
                nueva_fila = fila_normalizada.copy()
            else:
                factor = fila[columna_pivote]
                nueva_fila = [
                    valor - factor * valor_pivote
                    for valor, valor_pivote in zip(fila, fila_normalizada)
                ]

            nueva_tabla.append(
                [
                    0.0 if abs(valor) <= self.TOLERANCIA else valor
                    for valor in nueva_fila
                ]
            )

        variables_basicas = estado_tabla["variables_basicas"].copy()
        variables_basicas[fila_pivote] = estado_tabla["columnas"][columna_pivote]
        return {
            "columnas": estado_tabla["columnas"].copy(),
            "variables_basicas": variables_basicas,
            "tabla": nueva_tabla,
        }


class AplicacionPL:
    """Construye y controla la interfaz gráfica principal."""

    METODO_GRAFICO = "Método gráfico"
    METODO_SIMPLEX = "Método Simplex"

    def __init__(self, ventana):
        self.ventana = ventana
        self.filas_restricciones = []
        self.metodo_grafico = MetodoGrafico()
        self.metodo_simplex = MetodoSimplex()
        self.problema_actual = None
        self.resultado_actual = None

        self.metodo_var = tk.StringVar(value=self.METODO_GRAFICO)
        self.objetivo_var = tk.StringVar(value="Maximizar")
        self.coeficiente_x1_var = tk.StringVar()
        self.coeficiente_x2_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="Listo para ingresar un problema.")

        self._configurar_ventana()
        self._configurar_estilos()
        self._crear_interfaz()

        self.agregar_restriccion()
        self.agregar_restriccion()
        self._actualizar_estado_metodo()
        self.coeficiente_x1_var.trace_add("write", self._al_modificar_datos)
        self.coeficiente_x2_var.trace_add("write", self._al_modificar_datos)

    def _configurar_ventana(self):
        """Define el título y el tamaño inicial de la ventana."""
        self.ventana.title("Calculadora de Programación Lineal")
        self.ventana.geometry("1120x720")
        self.ventana.minsize(920, 620)

    def _configurar_estilos(self):
        """Aplica una presentación sencilla a los controles."""
        estilo = ttk.Style()
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 18, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10))
        estilo.configure("Seccion.TLabelframe.Label", font=("Segoe UI", 10, "bold"))
        estilo.configure("Accion.TButton", padding=(14, 8))
        estilo.configure("Circular.TButton", font=("Segoe UI", 13, "bold"), padding=(10, 3))

    def _crear_interfaz(self):
        """Crea las secciones principales de la aplicación."""
        contenedor = ttk.Frame(self.ventana, padding=18)
        contenedor.grid(row=0, column=0, sticky="nsew")

        self.ventana.rowconfigure(0, weight=1)
        self.ventana.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)

        encabezado = ttk.Frame(contenedor)
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))

        ttk.Label(
            encabezado,
            text="Calculadora de Programación Lineal",
            style="Titulo.TLabel",
        ).pack()
        ttk.Label(
            encabezado,
            text="Método gráfico y Simplex para problemas con X1 y X2",
            style="Subtitulo.TLabel",
        ).pack(pady=(4, 0))

        self._crear_panel_entrada(contenedor)
        self._crear_panel_salida(contenedor)

        ttk.Separator(contenedor, orient="horizontal").grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(14, 8)
        )
        ttk.Label(contenedor, textvariable=self.estado_var).grid(
            row=4, column=0, columnspan=2, sticky="w"
        )

    def _crear_panel_entrada(self, contenedor):
        """Crea los controles para ingresar el problema."""
        panel = ttk.Frame(contenedor, padding=(0, 0, 12, 0))
        panel.grid(row=2, column=0, sticky="nsew")
        panel.columnconfigure(0, weight=1)

        seleccion = ttk.LabelFrame(panel, text="Configuración", padding=12)
        seleccion.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        seleccion.columnconfigure(1, weight=1)
        seleccion.columnconfigure(3, weight=1)

        ttk.Label(seleccion, text="Método:").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.metodo_combo = ttk.Combobox(
            seleccion,
            textvariable=self.metodo_var,
            values=(self.METODO_GRAFICO, self.METODO_SIMPLEX),
            state="readonly",
            width=20,
        )
        self.metodo_combo.grid(row=0, column=1, sticky="ew", padx=(0, 16))
        self.metodo_combo.bind("<<ComboboxSelected>>", self._actualizar_estado_metodo)

        ttk.Label(seleccion, text="Objetivo:").grid(row=0, column=2, sticky="w", padx=(0, 8))
        self.objetivo_combo = ttk.Combobox(
            seleccion,
            textvariable=self.objetivo_var,
            values=("Maximizar", "Minimizar"),
            state="readonly",
            width=14,
        )
        self.objetivo_combo.grid(row=0, column=3, sticky="ew")
        self.objetivo_combo.bind("<<ComboboxSelected>>", self._al_modificar_datos)

        funcion = ttk.LabelFrame(panel, text="Función objetivo", padding=12)
        funcion.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        ttk.Label(funcion, text="Z =").grid(row=0, column=0, padx=(0, 6))
        ttk.Entry(funcion, textvariable=self.coeficiente_x1_var, width=10).grid(
            row=0, column=1
        )
        ttk.Label(funcion, text="X1  +").grid(row=0, column=2, padx=6)
        ttk.Entry(funcion, textvariable=self.coeficiente_x2_var, width=10).grid(
            row=0, column=3
        )
        ttk.Label(funcion, text="X2").grid(row=0, column=4, padx=(6, 0))

        restricciones = ttk.LabelFrame(panel, text="Restricciones", padding=12)
        restricciones.grid(row=2, column=0, sticky="nsew", pady=(0, 12))
        restricciones.columnconfigure(0, weight=1)
        panel.rowconfigure(2, weight=1)

        self.contenedor_restricciones = ttk.Frame(restricciones)
        self.contenedor_restricciones.grid(row=0, column=0, sticky="new")

        controles_filas = ttk.Frame(restricciones)
        controles_filas.grid(row=1, column=0, pady=(12, 0))
        ttk.Button(
            controles_filas,
            text="+",
            width=3,
            style="Circular.TButton",
            command=self.agregar_restriccion,
        ).grid(row=0, column=0, padx=5)
        ttk.Button(
            controles_filas,
            text="-",
            width=3,
            style="Circular.TButton",
            command=self.eliminar_restriccion,
        ).grid(row=0, column=1, padx=5)

        acciones = ttk.Frame(panel)
        acciones.grid(row=3, column=0, pady=(0, 4))
        ttk.Button(
            acciones,
            text="Resolver",
            style="Accion.TButton",
            command=self.resolver,
        ).grid(row=0, column=0, padx=6)
        ttk.Button(
            acciones,
            text="Limpiar",
            style="Accion.TButton",
            command=self.limpiar,
        ).grid(row=0, column=1, padx=6)

    def _crear_panel_salida(self, contenedor):
        """Reserva las zonas donde se mostrarán resultados y gráficas."""
        panel = ttk.Frame(contenedor, padding=(12, 0, 0, 0))
        panel.grid(row=2, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        resultados = ttk.LabelFrame(panel, text="Procedimiento y resultados", padding=10)
        resultados.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        resultados.rowconfigure(0, weight=1)
        resultados.columnconfigure(0, weight=1)

        self.texto_resultados = tk.Text(
            resultados,
            height=12,
            wrap="none",
            state="disabled",
            font=("Consolas", 10),
        )
        self.texto_resultados.grid(row=0, column=0, sticky="nsew")
        desplazamiento_vertical = ttk.Scrollbar(
            resultados,
            orient="vertical",
            command=self.texto_resultados.yview,
        )
        desplazamiento_vertical.grid(row=0, column=1, sticky="ns")
        desplazamiento_horizontal = ttk.Scrollbar(
            resultados,
            orient="horizontal",
            command=self.texto_resultados.xview,
        )
        desplazamiento_horizontal.grid(row=1, column=0, sticky="ew")
        self.texto_resultados.configure(
            yscrollcommand=desplazamiento_vertical.set,
            xscrollcommand=desplazamiento_horizontal.set,
        )

        self.marco_grafica = ttk.LabelFrame(panel, text="Gráfica", padding=10)
        self.marco_grafica.grid(row=1, column=0, sticky="nsew")
        self.marco_grafica.rowconfigure(0, weight=1)
        self.marco_grafica.columnconfigure(0, weight=1)
        self.etiqueta_grafica = ttk.Label(
            self.marco_grafica,
            text="La gráfica aparecerá al resolver un modelo gráfico.",
            anchor="center",
        )
        self.etiqueta_grafica.grid(row=0, column=0, sticky="nsew")
        self.canvas_grafica = None
        self.figura_grafica = None

    def agregar_restriccion(self):
        """Agrega una fila vacía al formulario de restricciones."""
        numero = len(self.filas_restricciones) + 1
        fila = ttk.Frame(self.contenedor_restricciones)
        fila.grid(row=numero - 1, column=0, sticky="w", pady=4)

        coeficiente_x1 = tk.StringVar()
        coeficiente_x2 = tk.StringVar()
        operador = tk.StringVar(value="<=")
        termino_independiente = tk.StringVar()

        etiqueta = ttk.Label(fila, text=f"{numero}.", width=3)
        etiqueta.grid(row=0, column=0, padx=(0, 4))
        ttk.Entry(fila, textvariable=coeficiente_x1, width=8).grid(row=0, column=1)
        ttk.Label(fila, text="X1 +").grid(row=0, column=2, padx=4)
        ttk.Entry(fila, textvariable=coeficiente_x2, width=8).grid(row=0, column=3)
        ttk.Label(fila, text="X2").grid(row=0, column=4, padx=4)
        operador_combo = ttk.Combobox(
            fila,
            textvariable=operador,
            values=("<=", ">="),
            state="readonly",
            width=5,
        )
        operador_combo.grid(row=0, column=5, padx=4)
        operador_combo.bind("<<ComboboxSelected>>", self._al_modificar_datos)
        ttk.Entry(fila, textvariable=termino_independiente, width=9).grid(
            row=0, column=6
        )

        coeficiente_x1.trace_add("write", self._al_modificar_datos)
        coeficiente_x2.trace_add("write", self._al_modificar_datos)
        termino_independiente.trace_add("write", self._al_modificar_datos)

        self.filas_restricciones.append(
            {
                "marco": fila,
                "etiqueta": etiqueta,
                "coeficiente_x1": coeficiente_x1,
                "coeficiente_x2": coeficiente_x2,
                "operador": operador,
                "operador_combo": operador_combo,
                "termino_independiente": termino_independiente,
            }
        )
        self._actualizar_operadores()
        self._descartar_resultado_actual()
        self.estado_var.set(f"Restricciones actuales: {len(self.filas_restricciones)}.")

    def eliminar_restriccion(self):
        """Elimina la última restricción y conserva al menos una fila."""
        if len(self.filas_restricciones) == 1:
            self.estado_var.set("Debe conservar al menos una restricción.")
            return

        self._eliminar_ultima_restriccion()
        self._descartar_resultado_actual()
        self.estado_var.set(f"Restricciones actuales: {len(self.filas_restricciones)}.")

    def _eliminar_ultima_restriccion(self):
        """Retira la última fila sin comprobar el mínimo permitido."""
        fila = self.filas_restricciones.pop()
        fila["marco"].destroy()

    def _actualizar_estado_metodo(self, _evento=None):
        """Ajusta objetivo y operadores al método seleccionado."""
        self._descartar_resultado_actual()
        if self.metodo_var.get() == self.METODO_SIMPLEX:
            self.objetivo_var.set("Maximizar")
            self.objetivo_combo.configure(state="disabled")
            self.estado_var.set("Simplex v1.0 admite solamente maximización y restricciones <=.")
            self._limpiar_grafica("Simplex no utiliza representación gráfica.")
        else:
            self.objetivo_combo.configure(state="readonly")
            self.estado_var.set("El método gráfico admite maximización y minimización.")
            self._limpiar_grafica()

        self._actualizar_operadores()

    def _al_modificar_datos(self, *_args):
        """Descarta una solución que ya no corresponde con el formulario."""
        if not hasattr(self, "texto_resultados"):
            return
        self._descartar_resultado_actual()
        self.estado_var.set("Datos modificados. Pulse Resolver para actualizar el resultado.")

    def _descartar_resultado_actual(self):
        """Limpia resultados y gráfica sin modificar los campos de entrada."""
        if not hasattr(self, "texto_resultados"):
            return
        self.problema_actual = None
        self.resultado_actual = None
        self._mostrar_resultado("")
        self._limpiar_grafica()

    def _actualizar_operadores(self):
        """Habilita o bloquea los operadores según el método."""
        es_simplex = self.metodo_var.get() == self.METODO_SIMPLEX
        for fila in self.filas_restricciones:
            if es_simplex:
                fila["operador"].set("<=")
                fila["operador_combo"].configure(state="disabled")
            else:
                fila["operador_combo"].configure(state="readonly")

    @staticmethod
    def _convertir_numero(texto, nombre_campo):
        """Convierte una entrada a número y produce un error fácil de entender."""
        texto_limpio = texto.strip().replace(",", ".")
        if not texto_limpio:
            raise ValueError(f"Ingrese {nombre_campo}.")

        try:
            numero = float(texto_limpio)
        except ValueError as error:
            raise ValueError(f"El valor de {nombre_campo} debe ser numérico.") from error

        if not math.isfinite(numero):
            raise ValueError(f"El valor de {nombre_campo} debe ser un número finito.")
        return numero

    def leer_problema(self):
        """Convierte las entradas visibles en un objeto ProblemaPL."""
        coeficiente_x1 = self._convertir_numero(
            self.coeficiente_x1_var.get(),
            "el coeficiente de X1 en la función objetivo",
        )
        coeficiente_x2 = self._convertir_numero(
            self.coeficiente_x2_var.get(),
            "el coeficiente de X2 en la función objetivo",
        )

        restricciones = []
        for numero, fila in enumerate(self.filas_restricciones, start=1):
            a1 = self._convertir_numero(
                fila["coeficiente_x1"].get(),
                f"el coeficiente de X1 en la restricción {numero}",
            )
            a2 = self._convertir_numero(
                fila["coeficiente_x2"].get(),
                f"el coeficiente de X2 en la restricción {numero}",
            )
            termino_independiente = self._convertir_numero(
                fila["termino_independiente"].get(),
                f"el término independiente de la restricción {numero}",
            )
            operador = fila["operador"].get()

            if operador not in ("<=", ">="):
                raise ValueError(f"Seleccione un operador válido en la restricción {numero}.")
            if self.metodo_var.get() == self.METODO_SIMPLEX and termino_independiente < 0:
                raise ValueError(
                    f"Simplex v1.0 requiere b >= 0 en la restricción {numero}."
                )

            restricciones.append((a1, a2, operador, termino_independiente))

        return ProblemaPL(
            objetivo=self.objetivo_var.get(),
            coeficientes_objetivo=(coeficiente_x1, coeficiente_x2),
            restricciones=restricciones,
        )

    def resolver(self):
        """Lee el modelo y ejecuta el método disponible en esta versión."""
        try:
            self.problema_actual = self.leer_problema()
        except ValueError as error:
            self.problema_actual = None
            self.resultado_actual = None
            self._limpiar_grafica()
            self._mostrar_resultado(f"No se pudo construir el modelo.\n\n{error}")
            self.estado_var.set("Revise los datos indicados en el panel de resultados.")
            return

        metodo = self.metodo_var.get()
        if metodo == self.METODO_GRAFICO:
            try:
                self.resultado_actual = self.metodo_grafico.resolver(
                    self.problema_actual
                )
            except ValueError as error:
                self.resultado_actual = None
                self._limpiar_grafica()
                self._mostrar_resultado(
                    f"Modelo ingresado\n----------------\n"
                    f"{self.problema_actual.formatear_modelo()}\n\n{error}"
                )
                self.estado_var.set("No fue posible resolver el modelo ingresado.")
                return

            texto = self._formatear_resultado_grafico()
            self._mostrar_grafica()
            self.estado_var.set("Método gráfico resuelto mediante vértices.")
        else:
            self._limpiar_grafica("Simplex no utiliza representación gráfica.")
            try:
                self.resultado_actual = self.metodo_simplex.resolver(
                    self.problema_actual
                )
            except ValueError as error:
                self.resultado_actual = None
                self._mostrar_resultado(
                    f"Modelo ingresado\n----------------\n"
                    f"{self.problema_actual.formatear_modelo()}\n\n{error}"
                )
                self.estado_var.set("No fue posible resolver el modelo con Simplex.")
                return

            texto = self._formatear_resultado_simplex()
            self.estado_var.set("Simplex completado y solución final obtenida.")

        self._mostrar_resultado(texto)

    def _formatear_resultado_simplex(self):
        """Prepara todas las iteraciones y la solución para la interfaz."""
        tabla_inicial = self.resultado_actual["tabla_inicial"]
        lineas = [
            "Método seleccionado: Método Simplex",
            "",
            "Modelo ingresado",
            "----------------",
            self.problema_actual.formatear_modelo(),
            "",
            "Tabla inicial",
            "-------------",
            self._formatear_tabla_simplex(tabla_inicial),
        ]

        for numero, iteracion in enumerate(
            self.resultado_actual["iteraciones"], start=1
        ):
            lineas_razones = []
            for variable, razon in zip(
                iteracion["variables_basicas_anteriores"][:-1],
                iteracion["razones"],
            ):
                texto_razon = (
                    "no válida"
                    if razon is None
                    else ProblemaPL.formatear_numero(razon)
                )
                lineas_razones.append(f"{variable}: {texto_razon}")

            pivote = ProblemaPL.formatear_numero(iteracion["pivote"])
            lineas.extend(
                [
                    "",
                    f"Iteración {numero} - selección del pivote",
                    "------------------------------------",
                    f"Variable entrante: {iteracion['variable_entrante']}",
                    "Razones:",
                    *lineas_razones,
                    f"Variable saliente: {iteracion['variable_saliente']}",
                    f"Elemento pivote: {pivote}",
                    "",
                    f"Tabla de la iteración {numero}",
                    "------------------------",
                    self._formatear_tabla_simplex(iteracion),
                ]
            )

        if not self.resultado_actual["iteraciones"]:
            lineas.extend(["", "La tabla inicial ya cumple la condición de optimalidad."])

        solucion = self.resultado_actual["solucion"]
        lineas.extend(
            [
                "",
                "Solución final",
                "--------------",
                f"X1 = {ProblemaPL.formatear_numero(solucion['X1'])}",
                f"X2 = {ProblemaPL.formatear_numero(solucion['X2'])}",
                f"Z  = {ProblemaPL.formatear_numero(solucion['Z'])}",
            ]
        )
        return "\n".join(lineas)

    @staticmethod
    def _formatear_tabla_simplex(resultado):
        """Convierte una tabla numérica en columnas alineadas."""
        encabezados = ["VB", *resultado["columnas"]]
        filas = []

        for variable_basica, valores in zip(
            resultado["variables_basicas"], resultado["tabla"]
        ):
            fila = [
                variable_basica,
                *(ProblemaPL.formatear_numero(valor) for valor in valores),
            ]
            filas.append(fila)

        anchos = []
        for indice, encabezado in enumerate(encabezados):
            ancho = max(len(encabezado), *(len(fila[indice]) for fila in filas))
            anchos.append(ancho)

        def formatear_fila(fila):
            return " | ".join(
                valor.rjust(anchos[indice]) for indice, valor in enumerate(fila)
            )

        separador = "-+-".join("-" * ancho for ancho in anchos)
        lineas = [formatear_fila(encabezados), separador]
        lineas.extend(formatear_fila(fila) for fila in filas)
        return "\n".join(lineas)

    def _mostrar_grafica(self):
        """Dibuja e integra la gráfica estática del resultado actual."""
        self._limpiar_grafica()
        self.etiqueta_grafica.grid_remove()

        figura = Figure(figsize=(5.2, 3.6), dpi=100)
        eje = figura.add_subplot(111)
        limite_x, limite_y = self.metodo_grafico.calcular_limites_grafica(
            self.problema_actual,
            self.resultado_actual["vertices"],
        )
        valores_x = [limite_x * indice / 300 for indice in range(301)]
        colores_restricciones = (
            "#1f77b4",
            "#ff7f0e",
            "#9467bd",
            "#2ca02c",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
        )

        for indice, restriccion in enumerate(
            self.problema_actual.restricciones, start=1
        ):
            a1, a2, _operador, termino_independiente = restriccion
            color = colores_restricciones[(indice - 1) % len(colores_restricciones)]
            if abs(a2) > self.metodo_grafico.TOLERANCIA:
                valores_y = [
                    (termino_independiente - a1 * x1) / a2 for x1 in valores_x
                ]
                eje.plot(
                    valores_x,
                    valores_y,
                    color=color,
                    linewidth=1.4,
                    label=f"R{indice}",
                )
            elif abs(a1) > self.metodo_grafico.TOLERANCIA:
                eje.axvline(
                    termino_independiente / a1,
                    color=color,
                    linewidth=1.4,
                    label=f"R{indice}",
                )

        vertices = self.resultado_actual["vertices"]
        if len(vertices) >= 3:
            vertices_ordenados = self.metodo_grafico.ordenar_vertices(vertices)
            region_x = [punto[0] for punto in vertices_ordenados]
            region_y = [punto[1] for punto in vertices_ordenados]
            eje.fill(
                region_x,
                region_y,
                color="#8bc34a",
                alpha=0.28,
                label="Región factible",
                zorder=1,
            )

        vertices_x = [punto[0] for punto in vertices]
        vertices_y = [punto[1] for punto in vertices]
        eje.scatter(
            vertices_x,
            vertices_y,
            color="#1565c0",
            s=30,
            label="Vértices",
            zorder=3,
        )

        for indice, (x1, x2) in enumerate(vertices, start=1):
            eje.annotate(
                f"V{indice}",
                (x1, x2),
                xytext=(4, 5),
                textcoords="offset points",
                fontsize=8,
            )

        x1_optimo, x2_optimo = self.resultado_actual["punto_optimo"]
        eje.scatter(
            [x1_optimo],
            [x2_optimo],
            color="#d32f2f",
            edgecolors="white",
            marker="*",
            s=180,
            linewidths=0.7,
            label="Solución óptima",
            zorder=4,
        )

        eje.set_xlim(0, limite_x)
        eje.set_ylim(0, limite_y)
        eje.set_xlabel("X1")
        eje.set_ylabel("X2")
        eje.set_title(f"Método gráfico - {self.problema_actual.objetivo}")
        eje.grid(True, alpha=0.25)
        eje.legend(loc="best", fontsize=7)
        figura.tight_layout()

        self.figura_grafica = figura
        self.canvas_grafica = FigureCanvasTkAgg(figura, master=self.marco_grafica)
        self.canvas_grafica.draw()
        self.canvas_grafica.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def _limpiar_grafica(self, mensaje="La gráfica aparecerá al resolver un modelo gráfico."):
        """Retira la figura anterior y recupera el texto de espera."""
        if self.canvas_grafica is not None:
            self.canvas_grafica.get_tk_widget().destroy()
            self.canvas_grafica = None
        if self.figura_grafica is not None:
            self.figura_grafica.clear()
            self.figura_grafica = None

        self.etiqueta_grafica.configure(text=mensaje)
        self.etiqueta_grafica.grid()

    def _formatear_resultado_grafico(self):
        """Prepara el procedimiento del método gráfico para la interfaz."""
        lineas = [
            "Método seleccionado: Método gráfico",
            "",
            "Modelo ingresado",
            "----------------",
            self.problema_actual.formatear_modelo(),
            "",
            "Vértices factibles:",
        ]

        for indice, vertice in enumerate(self.resultado_actual["vertices"], start=1):
            x1, x2 = vertice
            punto = self._formatear_punto(x1, x2)
            lineas.append(f"V{indice} = {punto}")

        lineas.extend(["", "Evaluación de la función objetivo:"])
        for indice, (_vertice, valor_z) in enumerate(
            self.resultado_actual["evaluaciones"], start=1
        ):
            valor = ProblemaPL.formatear_numero(valor_z)
            lineas.append(f"Z(V{indice}) = {valor}")

        x1_optimo, x2_optimo = self.resultado_actual["punto_optimo"]
        valor_optimo = self.resultado_actual["valor_optimo"]
        lineas.extend(
            [
                "",
                "Solución óptima:",
                f"X1 = {ProblemaPL.formatear_numero(x1_optimo)}",
                f"X2 = {ProblemaPL.formatear_numero(x2_optimo)}",
                f"Z  = {ProblemaPL.formatear_numero(valor_optimo)}",
                "",
                "La representación gráfica se incorporará en el siguiente incremento.",
            ]
        )
        return "\n".join(lineas)

    @staticmethod
    def _formatear_punto(x1, x2):
        """Convierte un par de coordenadas en texto legible."""
        valor_x1 = ProblemaPL.formatear_numero(x1)
        valor_x2 = ProblemaPL.formatear_numero(x2)
        return f"({valor_x1}, {valor_x2})"

    def limpiar(self):
        """Restablece el formulario a su estado inicial."""
        self.problema_actual = None
        self.resultado_actual = None
        self.metodo_var.set(self.METODO_GRAFICO)
        self.objetivo_var.set("Maximizar")
        self.coeficiente_x1_var.set("")
        self.coeficiente_x2_var.set("")

        while len(self.filas_restricciones) > 2:
            self._eliminar_ultima_restriccion()
        while len(self.filas_restricciones) < 2:
            self.agregar_restriccion()

        for fila in self.filas_restricciones:
            fila["coeficiente_x1"].set("")
            fila["coeficiente_x2"].set("")
            fila["operador"].set("<=")
            fila["termino_independiente"].set("")

        self._actualizar_estado_metodo()
        self._mostrar_resultado("")
        self._limpiar_grafica()
        self.estado_var.set("Formulario limpio.")

    def _mostrar_resultado(self, texto):
        """Escribe texto en el panel de resultados sin permitir su edición."""
        self.texto_resultados.configure(state="normal")
        self.texto_resultados.delete("1.0", tk.END)
        self.texto_resultados.insert("1.0", texto)
        self.texto_resultados.configure(state="disabled")


def main():
    """Inicia la aplicación de escritorio."""
    ventana = tk.Tk()
    AplicacionPL(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
