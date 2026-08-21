# ===================================================
# PROYECTO UNIFICADO 1
# CRUD CON TKINTER + SQLITE
# ===================================================

# ===================================================
# DECLARAR VARIABLES Y LIBRERIAS
# ===================================================

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from pathlib import Path

# ===================================================
# RUTA DEL PROYECTO
# ===================================================

BASE_DIR = Path(__file__).resolve().parent

# Base de datos en la misma carpeta del programa
RUTA_BDDD = BASE_DIR / "BaseJURM.db"

# Icono en la misma carpeta del programa
RUTA_ICONO = BASE_DIR / "images.ico"

# ===================================================
# VENTANA PRINCIPAL
# ===================================================

raiz = Tk()
raiz.title("Proyecto Unificado 1 - CRUD")

# ===================================================
# TAMAÑO DE LA VENTANA
# ===================================================

ancho = 1100
alto = 650

raiz.geometry(f"{ancho}x{alto}")
raiz.resizable(False, False)

# ===================================================
# ICONO DE LA VENTANA
# ===================================================

if RUTA_ICONO.exists():
    try:
        raiz.iconbitmap(str(RUTA_ICONO))
    except Exception as e:
        print("No se pudo cargar el icono:", e)
else:
    print("Advertencia: no se encontró el icono:")
    print(RUTA_ICONO)

# ===================================================
# VARIABLES TKINTER
# ===================================================

miId = StringVar()
miNombre = StringVar()
miPass = StringVar()
miApellido = StringVar()
miDireccion = StringVar()

# ===================================================
# FUNCIONES BBDD Y CONEXION
# ===================================================

def conexionBBDD():
    conexion = sqlite3.connect(str(RUTA_BDDD))
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TBL_USUARIOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE_USUARIO VARCHAR(50),
            PASSWORD VARCHAR(50),
            APELLIDO VARCHAR(50),
            DIRECCION VARCHAR(100),
            COMENTARIOS VARCHAR(255)
        )
    """)

    conexion.commit()
    conexion.close()

# ===================================================
# VALIDAR CAMPOS
# ===================================================

def validarCampos():
    if miNombre.get().strip() == "":
        messagebox.showwarning(
            "Validación",
            "Ingrese el nombre"
        )
        return False

    if miPass.get().strip() == "":
        messagebox.showwarning(
            "Validación",
            "Ingrese la contraseña"
        )
        return False

    if miApellido.get().strip() == "":
        messagebox.showwarning(
            "Validación",
            "Ingrese el apellido"
        )
        return False

    if miDireccion.get().strip() == "":
        messagebox.showwarning(
            "Validación",
            "Ingrese la dirección"
        )
        return False

    return True

# ===================================================
# VALIDAR ID
# ===================================================

def validarID():
    if miId.get().strip() == "":
        messagebox.showwarning(
            "Validación",
            "Ingrese un ID"
        )
        return False

    if not miId.get().isdigit():
        messagebox.showwarning(
            "Validación",
            "El ID debe ser numérico"
        )
        return False

    return True

# ===================================================
# LIMPIAR CAMPOS
# ===================================================

def limpiarCampos():
    miId.set("")
    miNombre.set("")
    miPass.set("")
    miApellido.set("")
    miDireccion.set("")

    textComentario.delete(
        "1.0",
        END
    )

# ===================================================
# CARGAR DATOS EN LA TABLA
# ===================================================

def cargarDatos():
    # Limpiar la tabla
    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = sqlite3.connect(str(RUTA_BDDD))
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            ID,
            NOMBRE_USUARIO,
            PASSWORD,
            APELLIDO,
            DIRECCION,
            COMENTARIOS
        FROM TBL_USUARIOS
        ORDER BY ID
        """
    )

    registros = cursor.fetchall()

    for registro in registros:
        tabla.insert(
            "",
            END,
            values=registro
        )

    conexion.close()

# ===================================================
# CREAR REGISTRO
# ===================================================

def crear():
    if not validarCampos():
        return

    conexion = sqlite3.connect(str(RUTA_BDDD))
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO TBL_USUARIOS
        (
            NOMBRE_USUARIO,
            PASSWORD,
            APELLIDO,
            DIRECCION,
            COMENTARIOS
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        miNombre.get().strip(),
        miPass.get().strip(),
        miApellido.get().strip(),
        miDireccion.get().strip(),
        textComentario.get("1.0", END).strip()
    ))

    conexion.commit()
    conexion.close()

    messagebox.showinfo(
        "BBDD",
        "Registro guardado correctamente"
    )

    limpiarCampos()
    cargarDatos()

# ===================================================
# LEER / CONSULTAR REGISTRO
# ===================================================

def leer():
    if not validarID():
        return

    conexion = sqlite3.connect(str(RUTA_BDDD))
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM TBL_USUARIOS
        WHERE ID = ?
        """,
        (miId.get(),)
    )

    usuario = cursor.fetchone()
    conexion.close()

    if usuario:
        miNombre.set(usuario[1])
        miPass.set(usuario[2])
        miApellido.set(usuario[3])
        miDireccion.set(usuario[4])

        textComentario.delete(
            "1.0",
            END
        )

        textComentario.insert(
            "1.0",
            usuario[5]
        )
    else:
        messagebox.showwarning(
            "Consulta",
            "No existe un registro con ese ID"
        )

# ===================================================
# ACTUALIZAR REGISTRO
# ===================================================

def actualizar():
    if not validarID():
        return

    if not validarCampos():
        return

    conexion = sqlite3.connect(str(RUTA_BDDD))
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE TBL_USUARIOS
        SET
            NOMBRE_USUARIO = ?,
            PASSWORD = ?,
            APELLIDO = ?,
            DIRECCION = ?,
            COMENTARIOS = ?
        WHERE ID = ?
    """, (
        miNombre.get().strip(),
        miPass.get().strip(),
        miApellido.get().strip(),
        miDireccion.get().strip(),
        textComentario.get("1.0", END).strip(),
        miId.get()
    ))

    conexion.commit()
    registros_actualizados = cursor.rowcount
    conexion.close()

    if registros_actualizados > 0:
        messagebox.showinfo(
            "Actualizar",
            "Registro actualizado correctamente"
        )
    else:
        messagebox.showwarning(
            "Actualizar",
            "No existe el ID"
        )

    cargarDatos()
    limpiarCampos()

# ===================================================
# ELIMINAR REGISTRO
# ===================================================

def eliminar():
    if not validarID():
        return

    respuesta = messagebox.askyesno(
        "Eliminar",
        "¿Desea eliminar este registro?"
    )

    if not respuesta:
        return

    conexion = sqlite3.connect(str(RUTA_BDDD))
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM TBL_USUARIOS
        WHERE ID = ?
        """,
        (miId.get(),)
    )

    conexion.commit()
    registros_eliminados = cursor.rowcount
    conexion.close()

    if registros_eliminados > 0:
        messagebox.showinfo(
            "Eliminar",
            "Registro eliminado correctamente"
        )
    else:
        messagebox.showwarning(
            "Eliminar",
            "No existe el ID"
        )

    cargarDatos()
    limpiarCampos()

# ===================================================
# SELECCIONAR REGISTRO DE LA TABLA
# ===================================================

def seleccionarRegistro(event):
    item = tabla.focus()

    if item == "":
        return

    datos = tabla.item(item)["values"]

    if not datos:
        return

    miId.set(datos[0])
    miNombre.set(datos[1])
    miPass.set(datos[2])
    miApellido.set(datos[3])
    miDireccion.set(datos[4])

    textComentario.delete(
        "1.0",
        END
    )

    textComentario.insert(
        "1.0",
        datos[5]
    )

# ===================================================
# SALIR DE LA APLICACION
# ===================================================

def salirAplicacion():
    valor = messagebox.askyesno(
        "Salir",
        "¿Desea salir de la aplicación?"
    )

    if valor:
        raiz.destroy()

# ===================================================
# MENU
# ===================================================

barraMenu = Menu(raiz)
raiz.config(menu=barraMenu)

# ===================================================
# OPCIONES DEL MENU
# ===================================================

menuArchivo = Menu(
    barraMenu,
    tearoff=0
)

menuArchivo.add_command(
    label="Limpiar",
    command=limpiarCampos
)

menuArchivo.add_separator()

menuArchivo.add_command(
    label="Salir",
    command=salirAplicacion
)

barraMenu.add_cascade(
    label="Archivo",
    menu=menuArchivo
)

menuCrud = Menu(
    barraMenu,
    tearoff=0
)

menuCrud.add_command(
    label="Crear",
    command=crear
)

menuCrud.add_command(
    label="Consultar",
    command=leer
)

menuCrud.add_command(
    label="Actualizar",
    command=actualizar
)

menuCrud.add_command(
    label="Eliminar",
    command=eliminar
)

barraMenu.add_cascade(
    label="CRUD",
    menu=menuCrud
)

# ===================================================
# ETIQUETAS Y CAMPOS
# ===================================================

Label(
    raiz,
    text="ID:"
).place(
    x=30,
    y=40
)

Entry(
    raiz,
    textvariable=miId,
    width=15
).place(
    x=130,
    y=40
)

Label(
    raiz,
    text="Nombre:"
).place(
    x=30,
    y=80
)

Entry(
    raiz,
    textvariable=miNombre,
    width=35
).place(
    x=130,
    y=80
)

Label(
    raiz,
    text="Contraseña:"
).place(
    x=30,
    y=120
)

Entry(
    raiz,
    textvariable=miPass,
    width=35,
    show="*"
).place(
    x=130,
    y=120
)

Label(
    raiz,
    text="Apellido:"
).place(
    x=30,
    y=160
)

Entry(
    raiz,
    textvariable=miApellido,
    width=35
).place(
    x=130,
    y=160
)

Label(
    raiz,
    text="Dirección:"
).place(
    x=30,
    y=200
)

Entry(
    raiz,
    textvariable=miDireccion,
    width=35
).place(
    x=130,
    y=200
)

Label(
    raiz,
    text="Comentarios:"
).place(
    x=30,
    y=240
)

textComentario = Text(
    raiz,
    width=35,
    height=6
)

textComentario.place(
    x=130,
    y=240
)

# ===================================================
# BOTONES
# ===================================================

Button(
    raiz,
    text="Crear",
    width=12,
    command=crear
).place(
    x=30,
    y=370
)

Button(
    raiz,
    text="Consultar",
    width=12,
    command=leer
).place(
    x=140,
    y=370
)

Button(
    raiz,
    text="Actualizar",
    width=12,
    command=actualizar
).place(
    x=250,
    y=370
)

Button(
    raiz,
    text="Eliminar",
    width=12,
    command=eliminar
).place(
    x=360,
    y=370
)

Button(
    raiz,
    text="Limpiar",
    width=12,
    command=limpiarCampos
).place(
    x=470,
    y=370
)

Button(
    raiz,
    text="Salir",
    width=12,
    command=salirAplicacion
).place(
    x=580,
    y=370
)

# ===================================================
# TABLA
# ===================================================

columnas = (
    "ID",
    "NOMBRE_USUARIO",
    "PASSWORD",
    "APELLIDO",
    "DIRECCION",
    "COMENTARIOS"
)

tabla = ttk.Treeview(
    raiz,
    columns=columnas,
    show="headings",
    height=10
)

tabla.heading(
    "ID",
    text="ID"
)

tabla.heading(
    "NOMBRE_USUARIO",
    text="Nombre"
)

tabla.heading(
    "PASSWORD",
    text="Password"
)

tabla.heading(
    "APELLIDO",
    text="Apellido"
)

tabla.heading(
    "DIRECCION",
    text="Dirección"
)

tabla.heading(
    "COMENTARIOS",
    text="Comentarios"
)

tabla.column(
    "ID",
    width=50
)

tabla.column(
    "NOMBRE_USUARIO",
    width=140
)

tabla.column(
    "PASSWORD",
    width=100
)

tabla.column(
    "APELLIDO",
    width=120
)

tabla.column(
    "DIRECCION",
    width=160
)

tabla.column(
    "COMENTARIOS",
    width=220
)

tabla.place(
    x=30,
    y=430
)

# ===================================================
# SCROLLBAR
# ===================================================

scrollTabla = Scrollbar(
    raiz,
    orient=VERTICAL,
    command=tabla.yview
)

scrollTabla.place(
    x=1020,
    y=430,
    height=225
)

tabla.configure(
    yscrollcommand=scrollTabla.set
)

# ===================================================
# EVENTO DE SELECCION
# ===================================================

tabla.bind(
    "<ButtonRelease-1>",
    seleccionarRegistro
)

# ===================================================
# INICIAR BASE DE DATOS
# ===================================================

conexionBBDD()

# ===================================================
# CARGAR DATOS
# ===================================================

cargarDatos()

# ===================================================
# EJECUTAR APLICACION
# ===================================================

raiz.mainloop()