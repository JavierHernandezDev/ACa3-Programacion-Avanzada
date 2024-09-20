import sqlite3
# Importamos la extencion para la base de datos y creamos la base de datos y la tabla
def conectar():
    conn = sqlite3.connect('libreria.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            anio INTEGER NOT NULL,
            isbn TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
# Importamos las librerias necesarias para la interfaz grafica
from tkinter import *
from tkinter import messagebox
# Creamos las funciones para insertar, listar, actualizar y eliminar los libros
def insertar(titulo, autor, anio, isbn):
    conn = sqlite3.connect('libreria.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO libros VALUES (NULL, ?, ?, ?, ?)", (titulo, autor, anio, isbn))
    conn.commit()
    conn.close()
    listar()

def listar():
    conn = sqlite3.connect('libreria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM libros")
    registros = cursor.fetchall()
    conn.close()
    list_libros.delete(0, END)
    for registro in registros:
        list_libros.insert(END, registro)

def actualizar(id, titulo, autor, anio, isbn):
    conn = sqlite3.connect('libreria.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE libros SET titulo=?, autor=?, anio=?, isbn=? WHERE id=?", (titulo, autor, anio, isbn, id))
    conn.commit()
    conn.close()
    listar()

def eliminar(id):
    conn = sqlite3.connect('libreria.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM libros WHERE id=?", (id,))
    conn.commit()
    conn.close()
    listar()

def agregar_libro():
    if titulo_texto.get() and autor_texto.get() and anio_texto.get() and isbn_texto.get():
        insertar(titulo_texto.get(), autor_texto.get(), anio_texto.get(), isbn_texto.get())
        limpiar_campos()
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

def seleccionar_libro(event):
    global libro_seleccionado
    indice = list_libros.curselection()
    if indice:
        libro_seleccionado = list_libros.get(indice)
        entrada_titulo.delete(0, END)
        entrada_titulo.insert(END, libro_seleccionado[1])
        entrada_autor.delete(0, END)
        entrada_autor.insert(END, libro_seleccionado[2])
        entrada_anio.delete(0, END)
        entrada_anio.insert(END, libro_seleccionado[3])
        entrada_isbn.delete(0, END)
        entrada_isbn.insert(END, libro_seleccionado[4])

def actualizar_libro():
    if libro_seleccionado:
        actualizar(libro_seleccionado[0], titulo_texto.get(), autor_texto.get(), anio_texto.get(), isbn_texto.get())
        limpiar_campos()
    else:
        messagebox.showwarning("Advertencia", "Seleccione un libro para actualizar.")

def eliminar_libro():
    if libro_seleccionado:
        eliminar(libro_seleccionado[0])
        limpiar_campos()
    else:
        messagebox.showwarning("Advertencia", "Seleccione un libro para eliminar.")

def limpiar_campos():
    entrada_titulo.delete(0, END)
    entrada_autor.delete(0, END)
    entrada_anio.delete(0, END)
    entrada_isbn.delete(0, END)

conectar()
# Creamos la interfaz grafica
ventana = Tk()
ventana.title("LibreríaApp")

# Etiquetas
label_titulo = Label(ventana, text="Título")
label_titulo.grid(row=0, column=0)

label_autor = Label(ventana, text="Autor/es")
label_autor.grid(row=0, column=2)

label_anio = Label(ventana, text="Año")
label_anio.grid(row=1, column=0)

label_isbn = Label(ventana, text="ISBN")
label_isbn.grid(row=1, column=2)

# Entradas
titulo_texto = StringVar()
entrada_titulo = Entry(ventana, textvariable=titulo_texto)
entrada_titulo.grid(row=0, column=1)

autor_texto = StringVar()
entrada_autor = Entry(ventana, textvariable=autor_texto)
entrada_autor.grid(row=0, column=3)

anio_texto = StringVar()
entrada_anio = Entry(ventana, textvariable=anio_texto)
entrada_anio.grid(row=1, column=1)

isbn_texto = StringVar()
entrada_isbn = Entry(ventana, textvariable=isbn_texto)
entrada_isbn.grid(row=1, column=3)

# Listbox y Scrollbar
list_libros = Listbox(ventana, height=8, width=50)
list_libros.grid(row=2, column=0, rowspan=6, columnspan=2)

scrollbar = Scrollbar(ventana)
scrollbar.grid(row=2, column=2, rowspan=6)

list_libros.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=list_libros.yview)

list_libros.bind('<<ListboxSelect>>', seleccionar_libro)

# Botones
boton_agregar = Button(ventana, text="Agregar libro", width=12, command=agregar_libro)
boton_agregar.grid(row=2, column=3)

boton_actualizar = Button(ventana, text="Actualizar", width=12, command=actualizar_libro)
boton_actualizar.grid(row=3, column=3)

boton_eliminar = Button(ventana, text="Eliminar", width=12, command=eliminar_libro)
boton_eliminar.grid(row=4, column=3)

boton_cerrar = Button(ventana, text="Cerrar", width=12, command=ventana.destroy)
boton_cerrar.grid(row=5, column=3)

listar()
ventana.mainloop()