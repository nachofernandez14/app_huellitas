from customtkinter import *
import customtkinter
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sqlite3
from tkinter import messagebox
from tkinter import PhotoImage
from manejo_db import baseDeDatos
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import time
import subprocess
import math


carpeta_principal = os.path.dirname(__file__)
##.Desktop\Proyecto final programacion
carpeta_imagenes = os.path.join(carpeta_principal, ("img"))
##.Desktop\Proyecto final programacion\img

gris_oscuro = '#3E3E3E'
gris_claro = '#DEDEDE'
verde_claro = '#02FA66'
verde_oscuro = '#058A3B'
verde_pastel = '#CDFFD4'
verde_intermedio = '#2CBE79'
azul = '#4B69FF'
azul_oscuro= '#1F3175'
gris_intermedio = '#777777'

#Creamos un clase articulo y proveedor para asi simplificar el codigo
class Articulo():
	def __init__(self, nombre, id_categoria, id_proveedor, precio_costo, precio_venta, cantidad):
		self.nombre = nombre
		self.id_categoria = id_categoria
		self.id_proveedor = id_proveedor
		self.precio_costo = precio_costo
		self.precio_venta = precio_venta
		self.cantidad = cantidad
class Proveedor():
	def __init__(self, nombre, telefono):
		self.nombre = nombre 
		self.telefono = telefono


def ventana_principal(usuario):
	ventana_p = CTk()
	ventana_p.geometry("1366x768")
	ventana_p.title("Huellitas Sistema")
	ventana_p.iconbitmap(os.path.join(carpeta_imagenes, "huellitas.ico"))
	
	fuente_default = CTkFont(family="Ebrima", size=14, weight="bold")
	fuente_titulos = CTkFont(family='Dubai', size=18, weight="bold")
	fuente_ventas = CTkFont(family="Agency FB", size=22, weight="bold")
	fuente_bienvenida = CTkFont(family='Bahnschrift Light', size=40, weight='bold')

	
	frame_menu = CTkFrame(ventana_p, fg_color=verde_claro)
	frame_menu.pack(side=LEFT, fill=Y)
	frame_fondo = CTkFrame(ventana_p)
	frame_fondo.pack(fill=BOTH, expand=True)

	##Creamos los frames para todas las secciones
	frame_articulos = CTkFrame(ventana_p, fg_color=gris_claro)
	frame_contenido_articulos = CTkFrame(frame_articulos, corner_radius=0, fg_color=verde_pastel)
	frame_categorias = CTkFrame(ventana_p, fg_color=gris_claro)
	frame_contenido_categorias = CTkFrame(frame_categorias, corner_radius=0, fg_color=verde_pastel)
	frame_proveedores = CTkFrame(ventana_p, fg_color=gris_claro)
	frame_contenido_proveedores = CTkFrame(frame_proveedores, corner_radius=0, fg_color=verde_pastel)
	frame_ventas = CTkFrame(ventana_p, fg_color=gris_claro)
	#Creamos la base de datos

	base_de_datos = baseDeDatos()

	def block_event(event):
			return 'break'


	def borrar_frames():
		frame_fondo.pack_forget()
		frame_articulos.pack_forget()
		frame_contenido_articulos.pack_forget()
		frame_categorias.pack_forget()
		frame_contenido_categorias.pack_forget()
		frame_proveedores.pack_forget()
		frame_contenido_proveedores.pack_forget()
		frame_ventas.pack_forget()

	
	def articulos():
		borrar_frames()

		label_modificar_articulo = CTkLabel(frame_articulos, text="Para modificar un articulo haga click sobre él en la tabla", text_color=gris_oscuro, font=fuente_default)
		label_eliminar_articulo = CTkLabel(frame_articulos, text="Para dar de baja un articulo haga click sobre él en la tabla", text_color=gris_oscuro, font=fuente_default)

		def listar_articulos():
			for item in lista_articulos.get_children():
				lista_articulos.delete(item)
			articulos = []
			articulos = base_de_datos.listarArticulos()
			for articulo in articulos:
				id = articulo[0]
				nombre = articulo[1]
				categoria = articulo[2]
				proveedor = articulo[3]
				precio_costo = articulo[4]
				precio_venta = articulo[5]
				cantidad = articulo[6]
				lista_articulos.insert("", "end", text=id, values=(nombre, categoria, proveedor, precio_costo, precio_venta, cantidad))

		def actualizar_entrada_articulos(*args):
			articulos = []
			articulos = base_de_datos.listarArticulos()
			buscador = entry_busqueda_articulos.get().lower()
			
			lista_articulos.delete(*lista_articulos.get_children())

			for articulo in articulos:
				nombre_articulo1 = articulo[1].lower()
				if nombre_articulo1.startswith(buscador):
					lista_articulos.insert("", END, text=articulo[0], values=(articulo[1],articulo[2], articulo[3], articulo[4], articulo[5], articulo[6]))
			if(buscador== ""):
				listar_articulos()

		def menu_articulos():
			frame_contenido_articulos.pack_forget()
			label_eliminar_articulo.place_forget()
			global frame_top_articulos, label_busqueda, entry_busqueda_articulos, boton_manipular_articulos, lista_articulos, boton_busqueda
			if 'modMenuArticulos' not in globals():
				global modMenuArticulos
				modMenuArticulos = True
				frame_top_articulos = CTkFrame(frame_articulos, fg_color=verde_oscuro, corner_radius=0)
				label_busqueda = CTkLabel(frame_top_articulos, text="Buscar articulo:", font=fuente_default, text_color='white')
				entry_busqueda_articulos = CTkEntry(frame_top_articulos, font=fuente_default)
				boton_busqueda = CTkButton(frame_top_articulos, text="Buscar", fg_color=verde_claro, text_color=gris_oscuro, font=fuente_default)
				opciones = ['Crear articulo','Modificar articulo','Eliminar articulo']
				boton_manipular_articulos = CTkOptionMenu(frame_top_articulos, values=opciones, command=seleccion, font=fuente_default)
				

				lista_articulos = ttk.Treeview(frame_articulos)
				lista_articulos["columns"]= ("nombre", "categoria", "proveedor", "precio_costo", "precio_venta", "cantidad")
				lista_articulos.column("#0", anchor="center", width=30)
				lista_articulos.column("nombre", anchor="center", width=150)
				lista_articulos.column("categoria", anchor="center", width=100)
				lista_articulos.column("proveedor", anchor="center", width=100)
				lista_articulos.column("precio_costo", anchor="center", width=100)
				lista_articulos.column("precio_venta", anchor="center", width=100)
				lista_articulos.column("cantidad", anchor="center", width=60)

				lista_articulos.heading("#0", text="ID", anchor="center")
				lista_articulos.heading("nombre", text="Nombre", anchor="center")
				lista_articulos.heading("categoria", text="Categoria", anchor="center")
				lista_articulos.heading("proveedor", text="Proveedor", anchor="center")
				lista_articulos.heading("precio_costo", text="Precio de costo", anchor="center")
				lista_articulos.heading("precio_venta", text="Precio de venta", anchor="center")
				lista_articulos.heading("cantidad", text="Cantidad", anchor="center")
				

				
			
			
			frame_articulos.pack(fill=BOTH, expand=True)
			frame_top_articulos.pack(side=TOP, fill=X, ipady=12)
			label_busqueda.pack(side=LEFT, padx=(20,0))
			entry_busqueda_articulos.pack(side=LEFT)
			entry_busqueda_articulos.bind("<KeyRelease>", actualizar_entrada_articulos)
			boton_busqueda.pack(side=LEFT, padx=4)
			boton_manipular_articulos.pack(side=RIGHT, padx=20)
			boton_manipular_articulos.configure(state='normal')
			boton_manipular_articulos.set("Seleccion una opcion")
			lista_articulos.pack(side=LEFT,padx=20, ipady=200, ipadx=100)
			lista_articulos.bind("<Button-1>", block_event)
			listar_articulos()
			


		

		def ocultar_widgets_articulos():
			for widget in frame_contenido_articulos.winfo_children():
				widget.pack_forget()
			frame_contenido_articulos.pack_forget()


		if 'modFramesArticulos' not in globals():	
			global modFramesArticulos, boton_volver_articulos, entry_nombre, entry_categoria_articulo, entry_proveedor_articulos, entry_precio_costo, entry_precio_venta, entry_cantidad
			modFramesArticulos = True
			boton_volver_articulos = CTkButton(frame_contenido_articulos, text="Volver", command=lambda: [menu_articulos(), boton_manipular_articulos.configure(state='normal')], font=fuente_default)
			entry_nombre = CTkEntry(frame_contenido_articulos, font=fuente_default, width=250)
			categorias = []
			categorias = base_de_datos.listarCategorias()
			nombre_categoria = [categoria[1] for categoria in categorias]
			entry_categoria_articulo = CTkOptionMenu(frame_contenido_articulos, values=nombre_categoria, font=fuente_default, width=250)
			entry_categoria_articulo.set("Seleccione la categoria")
			proveedores = []
			proveedores = base_de_datos.listarProveedores()
			nombre_proveedor = [prooved[1] for prooved in proveedores]
			entry_proveedor_articulos = CTkOptionMenu(frame_contenido_articulos, values = nombre_proveedor, font=fuente_default, width=250)
			entry_proveedor_articulos.set("Seleccione el proveedor")
			entry_precio_costo = CTkEntry(frame_contenido_articulos, font=fuente_default, width=250)
			entry_precio_venta = CTkEntry(frame_contenido_articulos, font=fuente_default, width=250)
			entry_cantidad = CTkEntry(frame_contenido_articulos, font=fuente_default, width=250)
			entry_estado = CTkOptionMenu(frame_contenido_articulos, font=fuente_default, width=250, values=('Activo', 'Innactivo'))
			

		def seleccion(opcion):
			global label_error
			ocultar_widgets_articulos()
			if(opcion == 'Crear articulo'):
				label_modificar_articulo.place_forget()
				label_eliminar_articulo.place_forget()
				boton_manipular_articulos.configure(state='disabled')
				lista_articulos.bind("<Button-1>", block_event)
				if 'label_error' not in globals():
					label_error = CTkLabel(frame_contenido_articulos, text="Por favor ingrese todos los datos para crear \n el producto correctamente", text_color="red")
				label_error.pack_forget()
				if not frame_contenido_articulos.winfo_ismapped():
					def guardar_articulo():
						nombre = entry_nombre.get()
						id_categoria = entry_categoria_articulo.get()
						id_proveedor = entry_proveedor_articulos.get()
						precio_costo = entry_precio_costo.get()
						precio_venta = entry_precio_venta.get()
						cantidad = entry_cantidad.get()
						if(nombre != "" and id_categoria != "" and id_proveedor != "" and precio_costo != "" and precio_venta != "" and cantidad != ""):
							validacion = True
							articulos = []
							articulos = base_de_datos.listarArticulos()
							for articulo in articulos:
								nombre_e = articulo[1]
								if (nombre == nombre_e):
									messagebox.showwarning(message="Error, ya hay un articulo con ese nombre", title="Error")
									validacion = False
									break
							if (validacion == True):
								articulo = Articulo(nombre, id_categoria, id_proveedor,precio_costo,precio_venta,cantidad)
								base_de_datos.insertArticulo(articulo)
								listar_articulos()
								label_error.pack_forget()
								#Borramos los entrys si todo salio bien
								entry_nombre.delete(0, END)
								entry_precio_costo.delete(0, END)
								entry_precio_venta.delete(0, END)
								entry_cantidad.delete(0,END)
						else:
							label_error.pack(pady=20)
					global label_crear_articulo, boton_guardar
					if 'modCrearArticulo' not in globals():
						global modCrearArticulo
						modCrearArticulo = True
						label_crear_articulo = CTkLabel(frame_contenido_articulos, text="Ingrese los datos del producto", font=fuente_titulos, text_color=verde_intermedio)
						boton_guardar = CTkButton(frame_contenido_articulos, text="Guardar producto", command=guardar_articulo, font=fuente_default)

					frame_contenido_articulos.pack(side=RIGHT, fill=Y,ipadx=20)
					label_crear_articulo.pack(pady=10)
					entry_nombre.pack(pady=10)
					entry_categoria_articulo.pack()
					entry_proveedor_articulos.pack(pady=10)
					entry_precio_costo.pack()
					entry_precio_venta.pack(pady=10)
					entry_cantidad.pack()
					entry_nombre.delete(0, END)
					#Borramos cada vez que tocamos el boton
					entry_precio_costo.delete(0, END)
					entry_precio_venta.delete(0, END)
					entry_cantidad.delete(0,END)

					entry_nombre.configure(placeholder_text="Ingrese el nombre")
					entry_categoria_articulo.set("Seleccione la categoria")
					entry_proveedor_articulos.set("Seleccione el proveedor")
					entry_precio_costo.configure(placeholder_text="Ingrese el precio de costo")
					entry_precio_venta.configure(placeholder_text="Ingrese el precio de venta")
					entry_cantidad.configure(placeholder_text="Ingrese la cantidad en stock")

					
					boton_guardar.pack(pady=20)
					boton_volver_articulos.pack()
			elif(opcion == 'Modificar articulo'):
				label_eliminar_articulo.place_forget()
				articulos = []
				articulos = base_de_datos.listarArticulos()
				if(len(articulos)>0):
					label_modificar_articulo.place(x=180, y=60)
					label_eliminar_articulo.place_forget()
					lista_articulos.unbind("<Button-1>")
					def modificar_articulo():
						##OBTENEMOS EL ID DEL ARTICULO
						seleccion = lista_articulos.selection()
						index = seleccion
						id_articulo = lista_articulos.item(index, 'text')
						#OBETENEMOS LOS DATOS DEL ARTICULO
						values = lista_articulos.item(seleccion)["values"]
						
						nombre = entry_nombre.get()
						categoria = entry_categoria_articulo.get()
						proveedor = entry_proveedor_articulos.get()
						precio_costo = entry_precio_costo.get()
						precio_venta = entry_precio_venta.get()
						cantidad = entry_cantidad.get()
						if(nombre != "" and categoria != "" and proveedor != "" and precio_costo != "" and precio_venta != "" and cantidad != ""):
							if(nombre == values[0] and categoria == values[1] and proveedor == values[2] and int(precio_costo) == values[3] and int(precio_venta) == values[4] and int(cantidad) == values[5]):
								messagebox.showwarning(message="Error, no puede modificar el articulo con los mismos datos existentes, debe haber algun campo diferente para que se modifique", title="Sistema huellitas")
							else:
								articulo = Articulo(nombre, categoria, proveedor, precio_costo, precio_venta, cantidad)
								base_de_datos.actualizarArticulo(articulo, id_articulo)
								listar_articulos()				
						else:
							messagebox.showwarning(message="Porfavor complete todos los campos para modificar el articulo correctamente", title="Sistema huellitas")
				elif(len(articulos)==0):
					boton_manipular_articulos.set("Seleccion una opcion")
					messagebox.showwarning(message="Error, no hay ningun articulo en la base de datos", title="Sistema huellitas")
				def verificar_seleccion_articulo(evento):
					label_modificar_articulo.place_forget()
					boton_manipular_articulos.configure(state='disabled')
					seleccion = lista_articulos.selection()
					index = seleccion
					valores = lista_articulos.item(index, 'values')
					global boton_modificar_articulo, label_modificar, label_nombre_articulo, label_categoria_producto, label_proveedor_producto, label_precio_costo, label_precio_venta, label_cantidad_producto
					if 'modModificarArticulo' not in globals():
						boton_modificar_articulo = CTkButton(frame_contenido_articulos, text= "Modificar articulo", command=modificar_articulo, font=fuente_default)
						label_modificar = CTkLabel(frame_contenido_articulos, text="Ingrese los nuevos datos del articulo", font=fuente_titulos, text_color=verde_intermedio)
						label_nombre_articulo = CTkLabel(frame_contenido_articulos, text="Nombre:",font=fuente_default, text_color=gris_oscuro)
						label_categoria_producto = CTkLabel(frame_contenido_articulos, text="Categoria:", font=fuente_default, text_color=gris_oscuro)
						label_proveedor_producto = CTkLabel(frame_contenido_articulos, text="Proveedor:", font=fuente_default, text_color=gris_oscuro)
						label_precio_costo = CTkLabel(frame_contenido_articulos, text="Precio costo:", font=fuente_default, text_color=gris_oscuro)
						label_precio_venta = CTkLabel(frame_contenido_articulos, text="Precio venta:", font=fuente_default, text_color=gris_oscuro)
						label_cantidad_producto = CTkLabel(frame_contenido_articulos, text="Cantidad:", font=fuente_default, text_color=gris_oscuro)
						global modModificarArticulo
						modModificarArticulo = True

					frame_contenido_articulos.pack(side=RIGHT, fill=Y, ipadx=20)
					label_modificar.pack(pady=10)
					label_nombre_articulo.pack(anchor=NW,padx=35)
					entry_nombre.pack(pady=(0,7))
					entry_nombre.delete(0, END)
					label_categoria_producto.pack(anchor=NW, padx=35)
					entry_categoria_articulo.pack(pady=(0,7))
					label_proveedor_producto.pack(anchor=NW, padx=35)
					entry_proveedor_articulos.pack(pady=(0,7))
					label_precio_costo.pack(anchor=NW, padx=35)
					entry_precio_costo.pack(pady=(0,7))
					entry_precio_costo.delete(0, END)
					label_precio_venta.pack(anchor=NW, padx=35)
					entry_precio_venta.pack(pady=(0,7))
					entry_precio_venta.delete(0, END)
					label_cantidad_producto.pack(anchor=NW, padx=35)
					entry_cantidad.pack(pady=(0,7))
					entry_cantidad.delete(0, END)
					if (len(valores) >1):
						entry_nombre.insert(0, valores[0])
						entry_categoria_articulo.set(valores[1])
						entry_proveedor_articulos.set(valores[2])
						entry_precio_costo.insert(0, valores[3])
						entry_precio_venta.insert(0, valores[4])
						entry_cantidad.insert(0, valores[5])
					boton_modificar_articulo.pack(pady=10)
					boton_volver_articulos.pack()

				lista_articulos.bind("<<TreeviewSelect>>", verificar_seleccion_articulo)
			elif(opcion == 'Eliminar articulo'):
				label_modificar_articulo.place_forget()
				label_eliminar_articulo.place_forget()
				articulos = []
				articulos = base_de_datos.listarArticulos()
				if(len(articulos)>0):
					label_eliminar_articulo.place(x=110, y=60)
					lista_articulos.unbind("<Button-1>")
				elif(len(articulos)==0):
					boton_manipular_articulos.set("Seleccione una opcion")
					messagebox.showwarning(message="Error, no hay ningun articulo en la base de datos", title="Sistema huellitas")
				def verificar_seleccion_articulo2(evento):
					seleccion = lista_articulos.selection()
					index = seleccion 
					valores = lista_articulos.item(index, 'values')
					lista_articulos.unbind("<<TreeviewSelect>>")
					respuesta = messagebox.askyesno("Huellitas sistema", "Desea darle de baja a " + valores[0] +"?")
					if(respuesta == True):
						seleccion = lista_articulos.selection()
						index = seleccion
						id_articulo = lista_articulos.item(index, 'text')
						base_de_datos.darDeBajaArticulo(id_articulo)
						label_eliminar_articulo.place(x=110, y=60)
						listar_articulos()
					elif(respuesta == False):
						lista_articulos.bind("<<TreeviewSelect>>", verificar_seleccion_articulo2)

				lista_articulos.bind("<<TreeviewSelect>>", verificar_seleccion_articulo2)

			

		if not frame_articulos.winfo_ismapped():
			menu_articulos()


	boton_articulos = CTkButton(frame_menu, text="Articulos", fg_color=verde_claro, text_color=gris_oscuro, font=fuente_default, command=articulos)
	boton_articulos.pack(ipady=6)


	def categorias():
		label_modificar_categoria = CTkLabel(frame_categorias, text="Para modificar una categoria haga click sobre él en la tabla", text_color=azul, font=fuente_default)
		label_eliminar_categoria = CTkLabel(frame_categorias, text="Para dar de baja una categoria haga click sobre él en la tabla", text_color='red', font=fuente_default)


		borrar_frames()
		def listarCategorias():
			for item in lista_categorias.get_children():
				lista_categorias.delete(item)
			categorias = []
			categorias = base_de_datos.listarCategorias()
			for categoria in categorias:	
				id = categoria[0]
				nombre = categoria[1]
				lista_categorias.insert("", "end", text=id, values=(nombre,))


		

		def actualizar_entrada_categorias(*args):
			categorias = []
			categorias = base_de_datos.listarCategorias()
			buscador = entry_busqueda_categoria.get().lower()
			
			lista_categorias.delete(*lista_categorias.get_children())

			for categoria in categorias:
				nombre_categoria1 = categoria[1].lower()
				if nombre_categoria1.startswith(buscador):
					lista_categorias.insert("", END, text=categoria[0], values=categoria[1])
			if(buscador== ""):
				listarCategorias()
			
			

		def menu_categorias():
			ocultar_widgets_categorias()
			frame_contenido_categorias.pack_forget()
			label_modificar_categoria.place_forget()
			
			global label_busqueda, entry_busqueda_categoria, boton_manipular_categorias, lista_categorias, frame_top_categorias, entrada
			if 'modCategorias' not in globals():
				global modCategorias 
				modCategorias = True
				frame_top_categorias = CTkFrame(frame_categorias, corner_radius=0, fg_color=verde_oscuro)
				label_busqueda = CTkLabel(frame_top_categorias, text="Buscar categoria:", font=fuente_default, text_color='white')
				entry_busqueda_categoria = CTkEntry(frame_top_categorias, font=fuente_default)				
				opciones = ['Crear categoria','Modificar categoria','Eliminar categoria']
				boton_manipular_categorias = CTkOptionMenu(frame_top_categorias, values=opciones,font=fuente_default, command=seleccion_categoria)
				lista_categorias = ttk.Treeview(frame_categorias, columns=('categoria'))
				lista_categorias.column("#0", anchor="center", width=60)
				lista_categorias.column("categoria", anchor="center", width=500)
				lista_categorias.heading("#0", text="ID", anchor="center")
				lista_categorias.heading("categoria", text="Categoria", anchor="center")
				
			frame_categorias.pack(fill=BOTH, expand=True)
			frame_top_categorias.pack(side=TOP, fill=X, ipady=12)
			label_busqueda.pack(side=LEFT, padx=(20,0))
			entry_busqueda_categoria.pack(side=LEFT)
			entry_busqueda_categoria.delete(0, END)
			entry_busqueda_categoria.bind("<KeyRelease>", actualizar_entrada_categorias)
			boton_manipular_categorias.pack(side=RIGHT, padx=20)
			boton_manipular_categorias.configure(state='normal')
			boton_manipular_categorias.set("Seleccione una opcion")
			lista_categorias.pack(side=LEFT,padx=20, ipady=200)
			lista_categorias.bind("<Button-1>", block_event)
			listarCategorias()

				
		def ocultar_widgets_categorias():
			for widget in frame_contenido_categorias.winfo_children():
				widget.pack_forget()

		if 'modFramesContenido' not in globals():
			global modFramesContenido, entry_categoria, boton_volver_categorias	
			modFramesContenido = True
			entry_categoria = CTkEntry(frame_contenido_categorias, font=fuente_default, width=200)
			boton_volver_categorias= CTkButton(frame_contenido_categorias, text="Volver", command=lambda: [menu_categorias(), boton_manipular_categorias.configure(state='normal')])	

		def seleccion_categoria(opcion):
			if(opcion == 'Crear categoria'):
				
				label_modificar_categoria.place_forget()
				label_eliminar_categoria.place_forget()
				boton_manipular_categorias.configure(state='disabled')
				lista_categorias.bind("<Button-1>", block_event)  
				global label_error_categoria
				if 'label_error_categoria' not in globals():
					label_error_categoria = CTkLabel(frame_contenido_categorias, text="Por favor ingrese todos los datos para \n crear el proveedor correctamente", text_color="red")
				label_error_categoria.pack_forget()
				
				def crear_categoria():
					print("estamos adentro del crear categoria")
					categoria= entry_categoria.get()
					if (categoria != ""):
						validacion = True
						categorias = []
						categorias = base_de_datos.listarCategorias()
						for categ in categorias:
							nombre_e = categ[1]
							if (nombre_e == categoria):
								messagebox.showwarning(message="Error, ya existe una categoria igual", title="Error")
								validacion = False
						if (validacion == True):
							base_de_datos.insertCategoria(categoria)
							listarCategorias()
							menu_categorias()
							boton_manipular_categorias.configure(state='normal')
							label_error_categoria.pack_forget()
					else:
						label_error_categoria.pack(ipady=10)
				boton_crear_categoria = CTkButton(frame_contenido_categorias, text="Crear categoria", command=crear_categoria)
					
				frame_contenido_categorias.pack(side=RIGHT, fill=Y,ipadx=20)
				entry_categoria.pack(pady=10)
				boton_crear_categoria.pack(pady=10)
				boton_volver_categorias.pack()
				#CODIGO PARA BORRAR TODO CADA VEZ QUE TOCAMOS EL BOTON
				entry_categoria.delete(0, END)
				entry_categoria.configure(placeholder_text="Ingrese la categoria a crear")
			elif(opcion == 'Modificar categoria'):
				ocultar_widgets_categorias()
				categorias = []
				categorias = base_de_datos.listarCategorias()
				if(len(categorias)>0):
					label_modificar_categoria.place(x=110, y=60)
					lista_categorias.unbind("<Button-1>")
					def modificar_categoria():

						entry_busqueda_categoria.delete(0, END)
						##OBTENEMOS EL ID DE LA CATEGORIA
						seleccion = lista_categorias.selection()
						index = seleccion
						id_categoria = lista_categorias.item(index, 'text')
						##OBTENEMOS EL NOMBRE
						values = lista_categorias.item(seleccion)["values"]
						nombre = values[0]
						categoria = entry_categoria.get()
						if(categoria != "" ):
							if(categoria == nombre):
								messagebox.showwarning(message="Error, la categoria ya tiene ese nombre", title="Sistema huellitas")
							else:
								base_de_datos.actualizarCategoria(categoria, id_categoria)	
								listarCategorias()
								frame_contenido_categorias.pack_forget()
						else:
							messagebox.showwarning(message="Porfavor complete todos los campos para modificar la categoria correctamente", title="Sistema huellitas")
				elif(len(categorias) == 0):
					boton_manipular_categorias.set("Seleccione una opcion")
					messagebox.showwarning(message="Error, no hay ninguna categoria en la base de datos", title="Sistema huellitas")

				def verificar_seleccion_categoria(evento):
					label_modificar_categoria.place_forget()
					boton_manipular_categorias.configure(state='disabled')
					seleccion = lista_categorias.selection()
					index = seleccion
					valores = lista_categorias.item(index, 'values')
					
					global boton_modificar_categoria, label_modificar_c
					if 'modModificarCategoria' not in globals():
						boton_modificar_categoria = CTkButton(frame_contenido_categorias, text= "Modificar categoria", command=modificar_categoria)
						label_modificar_c = CTkLabel(frame_contenido_categorias, text="Ingrese el nuevo nombre de la categoria", font=fuente_titulos, text_color=verde_intermedio)
						global modModificarCategoria
						modModificarCategoria = True
					frame_contenido_categorias.pack(side=RIGHT, fill=Y, ipadx=20)
					label_modificar_c.pack(pady=10)
					entry_categoria.pack(pady=10)
					entry_categoria.configure(state="normal")
					entry_categoria.delete(0, END)
					if(len(valores)>0):
						entry_categoria.insert(0, valores[0])
					boton_modificar_categoria.pack(pady=10)
					boton_volver_categorias.pack()

				lista_categorias.bind("<<TreeviewSelect>>", verificar_seleccion_categoria)

				
			elif(opcion == 'Eliminar categoria'):
				label_modificar_categoria.place_forget()
				label_eliminar_categoria.place_forget()
				categorias = []
				categorias = base_de_datos.listarCategorias()
				if(len(categorias)>0):
					label_eliminar_categoria.place(x=110, y=60)
					lista_categorias.unbind("<Button-1>")
				elif(len(categorias) == 0):
					boton_manipular_categorias.set("Seleccione una opcion")
					messagebox.showwarning(message="Error, no hay ninguna categoria en la base de datos", title="Sistema huellitas")
				def verificar_seleccion_categoria2(evento):
					seleccion = lista_categorias.selection()
					index = seleccion
					valores = lista_categorias.item(index, 'values')
					lista_categorias.unbind("<<TreeviewSelect>>")
					respuesta = messagebox.askyesno("Huellitas sistema", "Desea darle de baja a " + valores[0] +"?")
					if(respuesta == True):
						seleccion = lista_categorias.selection()
						index = seleccion
						id_categoria = lista_categorias.item(index, 'text')
						base_de_datos.darDeBajaCategoria(id_categoria)
						label_eliminar_categoria.place(x=110, y=60)
						listarCategorias()
						
					elif(respuesta == False):
						lista_categorias.bind("<<TreeviewSelect>>", verificar_seleccion_categoria2)

				lista_categorias.bind("<<TreeviewSelect>>", verificar_seleccion_categoria2)

		menu_categorias()

	boton_categorias = CTkButton(frame_menu, text="Categorias", fg_color=verde_claro, text_color=gris_oscuro, font=fuente_default, command=categorias)
	boton_categorias.pack(ipady=6)

	def proveedores():
		label_modificar_proveedor = CTkLabel(frame_proveedores, text="Para modificar un proveedor haga click sobre él en la tabla", text_color=azul, font=fuente_default)
		label_eliminar_proveedor = CTkLabel(frame_proveedores, text="Para dar de baja un proveedor haga click sobre él en la tabla", text_color='red', font=fuente_default)

		def listarProveedores():
			for item in lista_proveedores.get_children():
				lista_proveedores.delete(item)
			proveedores = []
			proveedores = base_de_datos.listarProveedores()
			for proveedor in proveedores:
				id = proveedor[0]
				nombre = proveedor[1]
				telefono = proveedor[2]
				lista_proveedores.insert("", "end", text=id, values=(nombre,telefono,))

		def actualizar_entrada_proveedores(*args):
			proveedores = []
			proveedores = base_de_datos.listarProveedores()
			buscador = entry_busqueda_proveedores.get().lower()
			
			lista_proveedores.delete(*lista_proveedores.get_children())

			for proveedor in proveedores:
				nombre_proveedor1 = proveedor[1].lower()
				if nombre_proveedor1.startswith(buscador):
					lista_proveedores.insert("", END, text=proveedor[0], values=(proveedor[1],proveedor[2]))
			if(buscador== ""):
				listarProveedores()

		borrar_frames()

		def menu_proveedores():
			label_modificar_proveedor.place_forget()
			label_eliminar_proveedor.place_forget()
			frame_contenido_proveedores.pack_forget()
			frame_contenido_proveedores.pack_forget()
			global frame_top_proveedores, label_busqueda, entry_busqueda_proveedores, boton_manipular_proveedores, lista_proveedores
			if 'modProveedores' not in globals():
				global modProveedores
				modProveedores = True
				frame_top_proveedores = CTkFrame(frame_proveedores, corner_radius=0, fg_color=verde_oscuro)
				label_busqueda = CTkLabel(frame_top_proveedores, text="Buscar proveedor:", font=fuente_default, text_color='white')
				entry_busqueda_proveedores = CTkEntry(frame_top_proveedores, font=fuente_default)
				opciones = ["Nuevo proveedor", "Modificar proveedor", "Eliminar proveedor"]
				boton_manipular_proveedores = CTkOptionMenu(frame_top_proveedores, values=opciones, command=seleccion_proveedores, font=fuente_default)
				lista_proveedores = ttk.Treeview(frame_proveedores)
				lista_proveedores["columns"]= ("proveedor", "telefono")
				lista_proveedores.column("#0", anchor="center", width=60)
				lista_proveedores.column("proveedor", anchor="center", width=250)
				lista_proveedores.column("telefono", anchor="center", width=250)
				lista_proveedores.heading("#0", text="ID", anchor="center")
				lista_proveedores.heading("proveedor", text="Proveedor", anchor="center")
				lista_proveedores.heading("telefono", text="Telefono", anchor="center")
				
			
			frame_proveedores.pack(fill=BOTH, expand=True)
			frame_top_proveedores.pack(side=TOP, fill=X, ipady=12)
			label_busqueda.pack(side=LEFT, padx=(20,0))
			entry_busqueda_proveedores.pack(side=LEFT)
			entry_busqueda_proveedores.bind("<KeyRelease>", actualizar_entrada_proveedores)
			boton_manipular_proveedores.pack(side=RIGHT, padx=20)
			boton_manipular_proveedores.configure(state='normal')
			boton_manipular_proveedores.set("Seleccione una opcion")
			lista_proveedores.pack(side=LEFT,padx=20, ipady=200)
			lista_proveedores.bind("<Button-1>", block_event)
			listarProveedores()

		def ocultar_widgets_proveedores():
			for widget in frame_contenido_proveedores.winfo_children():
				widget.pack_forget()

		if 'modFramesProveedores' not in globals():
			global modFramesProveedores, entry_proveedor, entry_telefono, boton_volver_proveedores
			modFramesProveedores = True
			entry_proveedor = CTkEntry(frame_contenido_proveedores, font=fuente_default, width=200)
			entry_telefono = CTkEntry(frame_contenido_proveedores, font=fuente_default, width=200)
			boton_volver_proveedores= CTkButton(frame_contenido_proveedores, text="Volver", command=lambda: [menu_proveedores(), boton_manipular_proveedores.configure(state='normal')], font=fuente_default)

		def seleccion_proveedores(opcion):
			ocultar_widgets_proveedores()
			global label_error_proveedor
			if (opcion == 'Nuevo proveedor'):
				label_modificar_proveedor.place_forget()
				label_eliminar_proveedor.place_forget()
				boton_manipular_proveedores.configure(state='disabled')
				lista_proveedores.bind("<Button-1>", block_event)
				if 'label_error_proveedor' not in globals():
					label_error_proveedor = CTkLabel(frame_contenido_proveedores, text="Por favor ingrese todos los datos para crear \n el proveedor correctamente", text_color="red")
				label_error_proveedor.pack_forget()
				if not frame_contenido_proveedores.winfo_ismapped():
					def crear_proveedor():
						validacion = True
						nombre = entry_proveedor.get()
						telefono = entry_telefono.get()
						if(nombre != "" and telefono != ""):
							if(telefono.isdigit()==True):
								proveedores = []
								proveedores = base_de_datos.listarProveedores()
								for proveed in proveedores:
									nombre_e = proveed[1]
									if(nombre_e == nombre):
										validacion= False
										messagebox.showwarning(message="Error, ya existe un proveedor con el mismo nombre", title="Error")
								if (validacion == True):
									proveedor = Proveedor(nombre, telefono)
									base_de_datos.insertProveedor(proveedor)
									label_error_proveedor.pack_forget()
									listarProveedores()
							else:
								messagebox.showwarning(message="Error, en el telefono solo se admiten numeros", title="Error")
								
						else:
							label_error_proveedor.pack(pady=20)
					global boton_crear_proveedor, label_crear_proveedor
					if 'modCrearProveedor' not in globals():	
						boton_crear_proveedor = CTkButton(frame_contenido_proveedores, text="Crear proveedor", command=crear_proveedor, font=fuente_default)
						label_crear_proveedor = CTkLabel(frame_contenido_proveedores, text="Ingrese los datos del proveedor", font=fuente_titulos, text_color=verde_intermedio)
						global modCrearProveedor
						modCrearProveedor = True
					frame_contenido_proveedores.pack(side=RIGHT, fill=Y, ipadx=40)
					label_crear_proveedor.pack(pady=10)
					entry_proveedor.pack(pady=(20,10), ipadx=15)
					entry_telefono.pack(ipadx=10)
					boton_crear_proveedor.pack(pady=15)
					boton_volver_proveedores.pack()
					#CODIGO PARA BORRAR TODO CADA VEZ QUE TOCAMOS EL BOTON
					entry_proveedor.delete(0, END)
					entry_telefono.delete(0, END)
					entry_proveedor.configure(placeholder_text="Ingrese el nombre del proveedor")
					entry_telefono.configure(placeholder_text="Ingrese el telefono del proveedor")

			elif(opcion == 'Modificar proveedor'):
				label_modificar_proveedor.place_forget()
				label_eliminar_proveedor.place_forget()
				proveedores = []
				proveedores = base_de_datos.listarProveedores()
				if(len(proveedores)>0):
					label_modificar_proveedor.place(x=90, y=60)
					lista_proveedores.unbind("<Button-1>")
					def modificar_proveedor():
						##OBTENEMOS EL ID DEL PROVEEDOR
						seleccion = lista_proveedores.selection()
						index = seleccion
						id_proveedor = lista_proveedores.item(index, 'text')
						#OBTENEMOS LOS VALORES DEL PROVEEDOR
						values = lista_proveedores.item(seleccion)["values"]
						nombre = entry_proveedor.get()
						telefono = entry_telefono.get()
						if(nombre != "" and telefono !=""):
							if(nombre == values[0] and int(telefono) == values[1]):
								messagebox.showwarning(message="Error, no puede modificar el proveedor con los mismos datos existentes, debe haber algun campo diferente para que se modifique", title="Sistema huellitas")
							else:
								proveedor = Proveedor(nombre, telefono)
								base_de_datos.actualizarProveedor(proveedor, id_proveedor)
								listarProveedores()				
						else:
							messagebox.showwarning(message="Porfavor complete todos los campos para modificar el proveedor correctamente", title="Sistema huellitas")
				elif(len(categorias) == 0):
					boton_manipular_proveedores.set("Seleccione una opcion")
					messagebox.showwarning(message="Error, no hay ningun proveedor en la base de datos", title="Sistema huellitas")
				def verificar_seleccion_proveedor(evento):
					label_modificar_proveedor.place_forget()
					boton_manipular_proveedores.configure(state='disabled')
					seleccion = lista_proveedores.selection()
					index = seleccion
					valores = lista_proveedores.item(index, 'values')
					global boton_modificar_proveedor, label_modificar_p, label_nombre_proveedor, label_telefono_proveedor
					if 'modModificarProveedor' not in globals():
						boton_modificar_proveedor = CTkButton(frame_contenido_proveedores, text="Modificar proveedor", command= modificar_proveedor, font=fuente_default)
						label_modificar_p = CTkLabel(frame_contenido_proveedores, text="Ingrese los nuevos datos del proveedor", font=fuente_titulos, text_color=verde_intermedio)
						label_nombre_proveedor = CTkLabel(frame_contenido_proveedores, text="Nombre:", font=fuente_default, text_color=gris_oscuro)
						label_telefono_proveedor = CTkLabel(frame_contenido_proveedores, text="Telefono:", font=fuente_default, text_color=gris_oscuro)
						global modModificarProveedor
						modModificarProveedor = True
					frame_contenido_proveedores.pack(side=RIGHT, fill=Y, ipadx=20)
					label_modificar_p.pack(pady=10)
					label_nombre_proveedor.pack(anchor=NW,padx=55)
					entry_proveedor.pack(ipadx=17)
					entry_proveedor.delete(0, END)
					label_telefono_proveedor.pack(anchor=NW,padx=55)
					entry_telefono.pack(pady=(0,10), ipadx=17)
					entry_telefono.delete(0, END)
					if (len(valores) >1):
						entry_proveedor.insert(0, valores[0])
						entry_telefono.insert(0, valores[1])
					boton_modificar_proveedor.pack(pady=10,ipadx=5)
					boton_volver_proveedores.pack()

				lista_proveedores.bind("<<TreeviewSelect>>", verificar_seleccion_proveedor)
				
			elif(opcion == "Eliminar proveedor"):
				label_modificar_proveedor.place_forget()
				label_eliminar_proveedor.place_forget()
				proveedores = []
				proveedores = base_de_datos.listarProveedores()
				if(len(proveedores)>0):
					label_eliminar_proveedor.place(x=110, y=60)
					lista_proveedores.unbind("<Button-1>")
				elif(len(proveedores)==0):
					boton_manipular_proveedores.set("Seleccione una opcion")
					messagebox.showwarning(message="Error, no hay ningun proveedor en la base de datos", title="Sistema huellitas")

				def verificar_seleccion_proveedor2(evento):
					
					seleccion = lista_proveedores.selection()
					index = seleccion 
					valores = lista_proveedores.item(index, 'values')
					lista_proveedores.unbind("<<TreeviewSelect>>")
					respuesta = messagebox.askyesno("Huellitas sistema", "Desea darle de baja a " + valores[0] +"?")
					if(respuesta == True):
						seleccion = lista_proveedores.selection()
						index = seleccion
						id_proveedor = lista_proveedores.item(index, 'text')
						base_de_datos.darDeBajaProveedor(id_proveedor)
						label_eliminar_proveedor.place(x=110, y=60)
						listarProveedores()
					elif(respuesta==False):
						lista_proveedores.bind("<<TreeviewSelect>>", verificar_seleccion_proveedor2)
						
					

				lista_proveedores.bind("<<TreeviewSelect>>", verificar_seleccion_proveedor2)

		menu_proveedores()




	boton_proveedores = CTkButton(frame_menu, text="Proveedores", fg_color=verde_claro, text_color=gris_oscuro, font=fuente_default, command=proveedores)
	boton_proveedores.pack(ipady=6)

	def ventas():



		borrar_frames()
		global total
		total = IntVar(value=0)
		carpeta_tickets = "Tickets"
		def menu_ventas():
			global carrito
			carrito =[]
			print(carrito)
			def vender():
				if(len(carrito) != 0):
					
					horaActual = time.strftime("%H%M%S")
					fechaActual = time.strftime("%d-%m-%Y")
					nombreArchivo = os.path.join(carpeta_tickets, f"Ticket_{fechaActual}_{horaActual}.pdf")
					nuevoPdf= canvas.Canvas(nombreArchivo,pagesize=A4)
					nuevoPdf.line(20, 820, 570, 820)
					nuevoPdf.line(20, 20, 570, 20)
					nuevoPdf.line(20, 720, 570, 720)
					#Lineas Y
					nuevoPdf.line(20, 20, 20, 820)
					nuevoPdf.line(570, 20, 570, 820)
					nuevoPdf.line(480, 720, 480, 820)

					nuevoPdf.setFont("Times-Roman", 20)
					nuevoPdf.drawString(50,780, "Ticket")
					nuevoPdf.setFont("Times-Roman", 20)
					nuevoPdf.drawString(100, 750, fechaActual)
					y=600
					for articulo in carrito:
						
						nuevoPdf.drawString(50, y, str(articulo[0] ))
						nuevoPdf.drawString(480, y, str(articulo[1] ))
						y-=20
						nuevoPdf.drawString(410, 80, "Total: $" + str(total.get()))
					nuevoPdf.save()
					subprocess.Popen(nombreArchivo, shell=True)
				else:
					messagebox.showwarning(message="No hay ningun articulo en el carrito", title="Sistema huellitas")
			
			global label_vender, frame_busqueda, frame_articulos, frame_carrito, entry_busqueda, boton_vender, label_total, label_total_precio, frame_carrito_articulos, frame_carrito_total,label_articulo,label_precio,label_cantidad,label_total,label_total_precio,boton_vender, label_busqueda
			if 'modVentas' not in globals():
				global modVentas
				modVentas = True
				frame_busqueda= CTkFrame(frame_ventas, fg_color='white', corner_radius=10, height=80)
				label_busqueda = CTkLabel(frame_busqueda, text="Buscar articulo", font=fuente_default)
				entry_busqueda = CTkEntry(frame_busqueda, font=fuente_default)

				label_articulos= CTkLabel(frame_ventas, text="ARTICULOS", font=fuente_ventas, text_color=verde_oscuro)
				frame_articulos = CTkFrame(frame_ventas, fg_color='white', corner_radius=10)
				

				#SECCION CARRITO
				label_carrito = CTkLabel(frame_ventas, text="CARRITO", font=fuente_ventas, text_color=verde_oscuro)
				frame_carrito = CTkFrame(frame_ventas, fg_color='white', corner_radius=10, width=380, height=650)

				frame_carrito_articulos = CTkFrame(frame_carrito, fg_color='white', width=380,height=550)
				label_articulo = CTkLabel(frame_carrito_articulos, text="Articulo", font = fuente_default)
				label_precio = CTkLabel(frame_carrito_articulos, text="Precio", font=fuente_default)
				label_cantidad = CTkLabel(frame_carrito_articulos, text="Cantidad", font=fuente_default)
				

				frame_carrito_total = CTkFrame(frame_carrito,fg_color='white',width=380, height=100)

				label_total = CTkLabel(frame_carrito_total, text="Total: ", font=fuente_default)
				label_total_precio = CTkLabel(frame_carrito_total, font=fuente_default, text=f"${total.get()}")
				boton_vender = CTkButton(frame_carrito_total, text="Vender", font=fuente_default, command=vender)

				
			frame_ventas.pack(fill=BOTH, expand=True)
			frame_busqueda.pack(side=TOP,anchor="nw", ipadx=525,ipady=15, padx=20, pady=20)
			label_busqueda.pack(side=LEFT, padx=(15,5))
			entry_busqueda.pack(side=LEFT)
			label_articulos.place(x=350, y=80)
			frame_articulos.pack(side=LEFT,padx=20, ipady=220)
			frame_articulos.pack_propagate(False)


			label_carrito.place(x=990,y=80)
			frame_carrito.pack_propagate(False)
			frame_carrito.pack(side=RIGHT, padx=20)

			frame_carrito_articulos.pack()
			label_articulo.grid(row=0,column=0, ipadx=60)
			label_precio.grid(row=0,column=1, ipadx=20)
			label_cantidad.grid(row=0, column=2, ipadx=20)

			frame_carrito_total.pack(side=BOTTOM)
			label_total.grid(row=0, column=0,ipadx=40)
			label_total_precio.grid(row=0,column=3,ipadx=50)
			boton_vender.grid(row=1,column=2,pady=(10,10))
			
			

			articulos = []
			articulos = base_de_datos.listarPyNArticulos()
			global columna_actual, fila_actual, columna1, fila1
			columna_actual = 0
			fila_actual = 0
			columna1 = 0
			fila1 = 0

			

			def agregar_al_carrito(art):
				global carrito
				carrito.append(art)
				global fila1
				fila1 += 1
				global total, cantidad
				nombre = art[0]
				precio = art[1]
				label_nombre= CTkLabel(frame_carrito_articulos, text=nombre)
				label_monto = CTkLabel(frame_carrito_articulos, text=precio)

				def opcion_seleccionada(opcion):
					cantidad = int(opcion_cantidad.get()) 
					if(cantidad>1):
						precio = art[1] * cantidad
						label_monto.configure(text=precio)
						total.set(total.get() + precio - art[1])
						label_total_precio.configure(text=f"${total.get()}")
				
				opciones = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
				opcion_cantidad = CTkOptionMenu(frame_carrito_articulos, values=opciones, font=fuente_default, width=10, command=opcion_seleccionada)
				label_nombre.grid(row=fila1, column=0, pady=5)
				label_monto.grid(row=fila1, column=1, pady=5)
				opcion_cantidad.grid(row=fila1, column=2, pady=5)


				total.set(total.get() + precio)
				label_total_precio.configure(text=f"${total.get()}")

			
			for articulo in articulos:
				informacion = articulo[0] + "\n" + "$" + str(articulo[1])
				label_articulo = CTkLabel(frame_articulos, text=informacion, text_color=gris_oscuro)
				label_articulo.grid(row = fila_actual * 2, column = columna_actual, padx=5, pady=2)

				boton_agregar_carrito = CTkButton(frame_articulos, text="Agregar al carrito", command=lambda art=articulo: agregar_al_carrito(art))
				boton_agregar_carrito.grid(row = fila_actual * 2 + 1, column = columna_actual, padx=5, pady=2)
				columna_actual = columna_actual + 1
				if (columna_actual == 5):
					columna_actual = 0
					fila_actual += 1


		menu_ventas()

		

	boton_ventas = CTkButton(frame_menu, text="Ventas", fg_color=verde_claro, text_color=gris_oscuro, font=fuente_default, command=ventas)
	boton_ventas.pack(ipady=6)

	usuario= CTkLabel(frame_menu, text=usuario, font=fuente_default)
	usuario.pack(side=BOTTOM, pady=(0,20))

	bienvenida = usuario.cget("text")
	"""
	global imagenLogo1
	ruta_logo = (os.path.join(carpeta_imagenes, "huellitasLogo.png"))
	imagen_pil = Image.open(ruta_logo)
	imagenLogo1 = CTkImage(light_image=imagen_pil, size=(200,200))
	"""
	label_bienvenida = CTkLabel(frame_fondo, text="¡Bienvenido " + bienvenida + "!", font=fuente_bienvenida)
	label_bienvenida.pack(pady=50)
	##label_logo = CTkLabel(frame_fondo, image=imagenLogo1, text="")
	ventana_p.mainloop()
