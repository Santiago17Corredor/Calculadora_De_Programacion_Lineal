"""Interfaz inicial de la calculadora de programación lineal.

Version v0.2: esta etapa contiene solamente el esqueleto visual. Los metodos
gráfico y Simplex se incorporarán de forma incremental en versiones posteriores.
"""

import tkinter as tk
from tkinter import ttk


class AplicacionPL:
    """Construye y controla la interfaz gráfica principal."""

    METODO_GRAFICO = "Método gráfico"
    METODO_SIMPLEX = "Método Simplex"

    def __init__(self, ventana):
        self.ventana = ventana
        self.filas_restricciones = []

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
            wrap="word",
            state="disabled",
            font=("Consolas", 10),
        )
        self.texto_resultados.grid(row=0, column=0, sticky="nsew")

        grafica = ttk.LabelFrame(panel, text="Grafica", padding=10)
        grafica.grid(row=1, column=0, sticky="nsew")
        grafica.rowconfigure(0, weight=1)
        grafica.columnconfigure(0, weight=1)
        ttk.Label(
            grafica,
            text="La gráfica se incorporará en v0.3.",
            anchor="center",
        ).grid(row=0, column=0, sticky="nsew")

    def agregar_restriccion(self):
        """Agrega una fila vacia al formulario de restricciones."""
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
        ttk.Entry(fila, textvariable=termino_independiente, width=9).grid(
            row=0, column=6
        )

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
        self.estado_var.set(f"Restricciones actuales: {len(self.filas_restricciones)}.")

    def eliminar_restriccion(self):
        """Elimina la ultima restriccion y conserva al menos una fila."""
        if len(self.filas_restricciones) == 1:
            self.estado_var.set("Debe conservar al menos una restricción.")
            return

        self._eliminar_ultima_restriccion()
        self.estado_var.set(f"Restricciones actuales: {len(self.filas_restricciones)}.")

    def _eliminar_ultima_restriccion(self):
        """Retira la ultima fila sin comprobar el minimo permitido."""
        fila = self.filas_restricciones.pop()
        fila["marco"].destroy()

    def _actualizar_estado_metodo(self, _evento=None):
        """Ajusta objetivo y operadores al metodo seleccionado."""
        if self.metodo_var.get() == self.METODO_SIMPLEX:
            self.objetivo_var.set("Maximizar")
            self.objetivo_combo.configure(state="disabled")
            self.estado_var.set("Simplex v1.0 admite solamente maximización y restricciones <=.")
        else:
            self.objetivo_combo.configure(state="readonly")
            self.estado_var.set("El método gráfico admite maximización y minimización.")

        self._actualizar_operadores()

    def _actualizar_operadores(self):
        """Habilita o bloquea los operadores segun el metodo."""
        es_simplex = self.metodo_var.get() == self.METODO_SIMPLEX
        for fila in self.filas_restricciones:
            if es_simplex:
                fila["operador"].set("<=")
                fila["operador_combo"].configure(state="disabled")
            else:
                fila["operador_combo"].configure(state="readonly")

    def resolver(self):
        """Informa el alcance actual del boton Resolver."""
        self._mostrar_resultado(
            "Interfaz v0.2 lista.\n\n"
            "La lectura del modelo se implementará en el siguiente incremento "
            "y los algoritmos se agregarán en sus fases correspondientes."
        )
        self.estado_var.set("Esqueleto visual comprobado; aún no se realizan cálculos.")

    def limpiar(self):
        """Restablece el formulario a su estado inicial."""
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
