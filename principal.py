from customtkinter import *
import customtkinter
from tkinter import ttk
from tkinter import Tk, Label
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
from tkcalendar import DateEntry



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
azul = '#0051CD'
azul_oscuro= '#1F3175'
gris_intermedio = '#777777'
gris1 = '#898989'


tema_oscuro = {
	"fondo": "#3E3E3E",
	"texto": "#FFFFFF",
	"texto_boton": "#FFFFFF",
	"placeholder": "#DEDEDE",

}
tema_claro = {
	"fondo": "#DEDEDE",
	"texto": "#FFFFFF",
	"texto_boton": "#FFFFFF",
	"placeholder": "#DEDEDE",

}


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
class Cuenta():
	def __init__(self, fecha, proveedor, saldo, pagos, pedidos):
		self.fecha = fecha
		self.proveedor = proveedor
		self.saldo = saldo
		self.pagos = pagos
		self.pedidos = pedidos


def ventana_principal(usuario):
	

	ventana_p = CTk()
	ventana_p.geometry("1366x768")
	ventana_p.title("Huellitas Sistema")
	ventana_p.iconbitmap(os.path.join(carpeta_imagenes, "huellitas.ico"))
	
	fuente_default = CTkFont(family="Ebrima", size=14, weight="bold")
	fuente_titulos = CTkFont(family='Dubai', size=18, weight="bold")
	fuente_titulos_grandes = CTkFont(family='Dubai', size=28, weight="bold")
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
	frame_configuracion = CTkFrame(ventana_p, corner_radius=0, fg_color=gris_oscuro)
	frame_cuentas = CTkFrame(ventana_p, fg_color=gris_claro)
	frame_contenido_cuentas = CTkFrame(frame_cuentas, fg_color=verde_pastel)
	frame_articulos2 = CTkFrame(frame_ventas, fg_color='white', corner_radius=10, width=800, height=490)


	#Creamos la base de datos
	base_de_datos = baseDeDatos()


	




	style = ttk.Style()
	style.configure("Treeview.Heading", font=fuente_default)

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
		frame_configuracion.pack_forget()
		frame_cuentas.pack_forget()
		frame_contenido_cuentas.pack_forget()


	global usuario1
	usuario1 = usuario

	global imagen_configuracion
	imagen_configuracion = Image.open(os.path.join(carpeta_imagenes, "configuracion.png"))
	imagen_configuracion1 = CTkImage(dark_image=imagen_configuracion, size=(30, 30))

	def configuracion():
		
		borrar_frames()
		##FUNCIONES PARA EFECTOS DE LOS BOTONES
		def on_hover(event, boton):
			boton.configure(text_color="white")  # Más blanco al pasar el mouse

		def on_leave(event,boton):
			boton.configure(text_color=gris_claro) 

		def guardar_apariencia():
			global tema_actual
			opcion = boton_cambiar_tema.get()
			if (opcion == 'Tema claro'):
				customtkinter.set_appearance_mode("Light")
			elif(opcion == 'Tema oscuro'):
				customtkinter.set_appearance_mode("Dark")

			

		def cambiar_apariencia():
			global linea_frame_configuracion, frame_apariencia, label_tema, boton_cambiar_tema, boton_guardar
			if 'modApariencia' not in globals():
				linea_frame_configuracion = CTkFrame(frame_configuracion, width=100, height=2, fg_color=gris_claro)
				frame_apariencia = CTkFrame(frame_configuracion, corner_radius= 0, fg_color=gris_oscuro)
				label_tema = CTkLabel(frame_apariencia, text="Tema", font=fuente_default, text_color='white')
				opciones = ["Tema oscuro", "Tema claro"]
				boton_cambiar_tema = CTkOptionMenu(frame_apariencia, values=opciones, font=fuente_default, fg_color='black', bg_color='black', button_color='black')
				boton_guardar = CTkButton(frame_apariencia,text="Guardar", bg_color='black', font=fuente_default, command=guardar_apariencia)
				
				global modApariencia
				modApariencia = True
			
			linea_frame_configuracion.pack(side=TOP, anchor=NW, padx=20)
			frame_apariencia.pack(fill=BOTH, expand=True)
			label_tema.pack(side=TOP, anchor=NW,padx=20, pady=(20,0))
			boton_cambiar_tema.pack(side=TOP, anchor=NW,padx=20)
			boton_guardar.pack(side=LEFT, anchor=NW, padx=20, pady=20)
		
		def salir():
			 if messagebox.askyesno(message="Seguro que quiere salir?", title="Sistema huellitas"):
			 	ventana_p.destroy()
			 else:
			 	pass
		
		global frame_top_configuracion, frame_labels_top, label_configuracion, boton_apariencia, boton_salir
		if 'modConfiguracion' not in globals():
			frame_top_configuracion = CTkFrame(frame_configuracion, corner_radius=0, fg_color=gris_oscuro)
			frame_labels_top = CTkFrame(frame_configuracion, corner_radius=0, fg_color=gris_oscuro)
			label_configuracion = CTkLabel(frame_top_configuracion, text="Configuración", font=fuente_titulos_grandes, text_color='white')
			boton_apariencia = CTkButton(frame_labels_top, text="Apariencia", font=fuente_titulos, text_color=gris_claro, fg_color="transparent", hover_color=gris1,border_width=0)
			boton_salir= CTkButton(frame_top_configuracion, text="Salir", bg_color='black', font=fuente_default, command=salir, fg_color='red', hover_color='#6D0000')

			global modConfiguracion
			modConfiguracion = True


		frame_configuracion.pack(fill=BOTH, expand=True)
		frame_top_configuracion.pack(side=TOP, fill=X)
		frame_labels_top.pack(side=TOP, fill=X)
		label_configuracion.pack(side=LEFT, padx=20)

		boton_apariencia.bind("<Enter>", lambda e, b=boton_apariencia: on_hover(e, b))
		boton_apariencia.bind("<Leave>", lambda e, b=boton_apariencia: on_leave(e, b))
		boton_apariencia.pack(side=LEFT)

		boton_apariencia.configure(command=cambiar_apariencia())

		boton_salir.pack(side=RIGHT, padx=15)

		


	configuracion = CTkButton(frame_menu, image=imagen_configuracion1,compound='left', text="Configuración", fg_color=verde_claro, text_color=gris_oscuro,font=fuente_default, anchor='w', width=150, height=80, corner_radius=0, command=configuracion)
	configuracion.pack(side=BOTTOM)

	linea_frame2 = CTkFrame(frame_menu, width=120, height=2, fg_color=gris_oscuro)
	linea_frame2.pack(side=BOTTOM)
	
	#Creamos el inicio
	def inicio():
		borrar_frames()
		global usuario1
		if 'modUsuario' not in globals():
			global imagen_fondo
			imagen_fondo = Image.open(os.path.join(carpeta_imagenes, "huellitasLogo.png"))
			imagen_fondo1 = CTkImage(dark_image=imagen_fondo, size=(600, 450))
			global modUsuario

		frame_fondo.pack(fill=BOTH,expand=True)

		
		label_imagen_fondo = CTkLabel(frame_fondo, image=imagen_fondo1, text= "")
		label_imagen_fondo.image = imagen_fondo1  # Mantener la referencia de la imagen
		label_imagen_fondo.pack(padx=50, pady=50)
		label_bienvenida = CTkLabel(frame_fondo, text="¡Bienvenido " + usuario1 + "!", font=fuente_bienvenida)
		label_bienvenida.pack(pady=50)
	
	inicio()
	global imagen_inicio
	imagen_inicio = Image.open(os.path.join(carpeta_imagenes, "inicio.png"))
	imagen_inicio1 = CTkImage(dark_image=imagen_inicio, size=(30, 30))


	boton_inicio = CTkButton(frame_menu,image=imagen_inicio1,compound='left', text="Inicio", fg_color=verde_claro, text_color=gris_oscuro, command=inicio,font=fuente_default, anchor='w', width=150, height=40, corner_radius=0)
	boton_inicio.pack(ipady=6)

	linea_frame = CTkFrame(frame_menu, width=120, height=2, fg_color=gris_oscuro)
	linea_frame.pack()


	def articulos():
		borrar_frames()

		label_modificar_articulo = CTkLabel(frame_articulos, text="Para modificar un articulo haga click sobre él en la tabla", text_color=azul, font=fuente_default)
		label_eliminar_articulo = CTkLabel(frame_articulos, text="Para dar de baja un articulo haga click sobre él en la tabla", text_color=azul, font=fuente_default)
		label_alta_articulo = CTkLabel(frame_articulos, text="Para dar de alta un articulo haga click sobre él en la tabla", text_color=azul, font=fuente_default)

		


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

		def listar_articulos_inactivos():
			for item in lista_articulos.get_children():
				lista_articulos.delete(item)
			articulosInactivos = []
			articulosInactivos = base_de_datos.listarArticulosInactivos()
			for articulo in articulosInactivos:
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
			label_modificar_articulo.place_forget()
			global frame_top_articulos, label_busqueda, entry_busqueda_articulos, boton_manipular_articulos, lista_articulos, boton_busqueda, label_articulos
			if 'modMenuArticulos' not in globals():
				global modMenuArticulos
				modMenuArticulos = True
				frame_top_articulos = CTkFrame(frame_articulos, fg_color=verde_oscuro, corner_radius=0)
				label_busqueda = CTkLabel(frame_top_articulos, text="Buscar articulo:", font=fuente_default, text_color='white')
				entry_busqueda_articulos = CTkEntry(frame_top_articulos, font=fuente_default)
				opciones = ['Crear articulo','Modificar articulo','Eliminar articulo', 'Articulos Inactivos']
				boton_manipular_articulos = CTkOptionMenu(frame_top_articulos, values=opciones, command=seleccion, font=fuente_default)
				label_articulos= CTkLabel(frame_articulos, text="ARTICULOS", text_color='white', bg_color=verde_oscuro, font=fuente_titulos)

				lista_articulos = ttk.Treeview(frame_articulos, height=31)
				lista_articulos["columns"]= ("nombre", "categoria", "proveedor", "precio_costo", "precio_venta", "cantidad")
				lista_articulos.column("#0", anchor="center", width=30)
				lista_articulos.column("nombre", anchor="center", width=180)
				lista_articulos.column("categoria", anchor="center", width=160)
				lista_articulos.column("proveedor", anchor="center", width=130)
				lista_articulos.column("precio_costo", anchor="center", width=130)
				lista_articulos.column("precio_venta", anchor="center", width=130)
				lista_articulos.column("cantidad", anchor="center", width=100)

				lista_articulos.heading("#0", text="ID", anchor="center")
				lista_articulos.heading("nombre", text="Nombre", anchor="center")
				lista_articulos.heading("categoria", text="Categoria", anchor="center")
				lista_articulos.heading("proveedor", text="Proveedor", anchor="center")
				lista_articulos.heading("precio_costo", text="Precio de costo", anchor="center")
				lista_articulos.heading("precio_venta", text="Precio de venta", anchor="center")
				lista_articulos.heading("cantidad", text="Cantidad", anchor="center")
				

				
			
			
			frame_articulos.pack(fill=BOTH, expand=True)
			frame_top_articulos.pack(side=TOP, fill=X, ipady=12)
			label_busqueda.pack(side=LEFT, padx=(20,4))
			entry_busqueda_articulos.pack(side=LEFT)
			entry_busqueda_articulos.bind("<KeyRelease>", actualizar_entrada_articulos)
			boton_manipular_articulos.pack(side=RIGHT, padx=20)
			boton_manipular_articulos.configure(state='normal')
			boton_manipular_articulos.set("Seleccion una opcion")
			label_articulos.place(x=570, y=14)
			lista_articulos.pack(side=LEFT,padx=20)
			lista_articulos.bind("<Button-1>", block_event)
			lista_articulos.unbind("<<TreeviewSelect>>")
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
					categorias = []
					categorias = base_de_datos.listarCategorias()
					nombre_categoria = [categoria[1] for categoria in categorias]
					entry_categoria_articulo.configure(values=nombre_categoria)
					entry_proveedor_articulos.set("Seleccione el proveedor")
					proveedores = []
					proveedores = base_de_datos.listarProveedores()
					nombre_proveedor = [proveedor[1] for proveedor in proveedores]
					entry_proveedor_articulos.configure(values=nombre_proveedor)
					entry_precio_costo.configure(placeholder_text="Ingrese el precio de costo")
					entry_precio_venta.configure(placeholder_text="Ingrese el precio de venta")
					entry_cantidad.configure(placeholder_text="Ingrese la cantidad en stock")

					
					boton_guardar.pack(pady=20)
					boton_volver_articulos.pack()
			elif(opcion == 'Modificar articulo'):
				lista_articulos.bind("<<TreeviewSelect>>")
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
								messagebox.showinfo(message="El articulo fue modificado correctamente", title="Sistema huellitas")
								if frame_contenido_articulos.winfo_ismapped():
									frame_contenido_articulos.pack_forget()
									frame_contenido_articulos.update()
									label_modificar_articulo.place_forget()
									menu_articulos()				
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
					categorias = []
					categorias = base_de_datos.listarCategorias()
					nombre_categoria = [categoria[1] for categoria in categorias]
					entry_categoria_articulo.configure(values=nombre_categoria)
					label_proveedor_producto.pack(anchor=NW, padx=35)
					entry_proveedor_articulos.pack(pady=(0,7))
					proveedores = []
					proveedores = base_de_datos.listarProveedores()
					nombre_proveedor = [proveedor[1] for proveedor in proveedores]
					entry_proveedor_articulos.configure(values=nombre_proveedor)
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
				def dar_de_baja_articulo():
					label_alta_articulo.place_forget()	
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
						menu_articulos()
					def verificar_seleccion_articulo2(evento):
						seleccion = lista_articulos.selection()
						if not seleccion:
							return
						index = seleccion 
						valores = lista_articulos.item(index, 'values')
						if not valores or len(valores) == 0:
							return
						lista_articulos.unbind("<<TreeviewSelect>>")
						respuesta = messagebox.askyesno("Huellitas sistema", "Desea darle de baja a " + valores[0] +"?")
						if(respuesta == True):
							seleccion = lista_articulos.selection()
							index = seleccion
							id_articulo = lista_articulos.item(index, 'text')
							base_de_datos.darDeBajaArticulo(id_articulo)
							label_eliminar_articulo.place_forget()
							menu_articulos()
						elif(respuesta == False):
							lista_articulos.bind("<<TreeviewSelect>>", verificar_seleccion_articulo2)
							label_eliminar_articulo.place_forget()

					lista_articulos.bind("<<TreeviewSelect>>", verificar_seleccion_articulo2)

				if(opcion== 'Eliminar articulo'):
					dar_de_baja_articulo()
			elif(opcion == 'Articulos Inactivos'):
				
				lista_articulos.unbind("<<TreeviewSelect>>")
				listar_articulos_inactivos()

				def dar_de_alta_articulo():
					label_alta_articulo.place_forget()
					label_modificar_articulo.place_forget()
					label_eliminar_articulo.place_forget()
					articulosInactivos = []
					articulosInactivos = base_de_datos.listarArticulosInactivos()
					if(len(articulosInactivos)>0):
						label_alta_articulo.place(x=110, y=60)
						lista_articulos.unbind("<Button-1>")
					elif(len(articulosInactivos) == 0):
						boton_manipular_articulos.set("Seleccione una opcion")
						messagebox.showwarning(message="Error, no hay ningun articulo inactivo en la base de datos", title="Sistema huellitas")
						menu_articulos()
					def verificar_seleccion_articulos3(evento):
						seleccion = lista_articulos.selection()
						if not seleccion:
							return


						index = seleccion
						valores = lista_articulos.item(index, 'values')
						if not valores or len(valores) == 0:
							return

						lista_articulos.unbind("<<TreeviewSelect>>")
						respuesta = messagebox.askyesno("Huellitas sistema", "Desea darle de alta a " + valores[0] +"?")
						if(respuesta == True):
							seleccion = lista_articulos.selection()
							index = seleccion
							id_articulo = lista_articulos.item(index, 'text')
							base_de_datos.darDeAltaArticulo(id_articulo)
							label_alta_articulo.place(x=110, y=60)
							listar_articulos_inactivos()
							dar_de_alta_articulo()
							menu_articulos()
							
						elif(respuesta == False):
							lista_articulos.bind("<<TreeviewSelect>>", verificar_seleccion_articulos3)

					lista_articulos.bind("<<TreeviewSelect>>", verificar_seleccion_articulos3)

				if (opcion == 'Articulos Inactivos'):
					dar_de_alta_articulo()

			

		if not frame_articulos.winfo_ismapped():
			menu_articulos()


	global imagen_articulos
	imagen_articulos = Image.open(os.path.join(carpeta_imagenes, "articulos.png"))
	imagen_articulos1 = CTkImage(dark_image=imagen_articulos, size=(30, 30))


	boton_articulos = CTkButton(frame_menu, image=imagen_articulos1,compound='left', text="Articulos", fg_color=verde_claro, text_color=gris_oscuro, font=fuente_default, command=articulos, anchor='w', width=150, height=40, corner_radius=0)
	boton_articulos.pack(ipady=6)


	def categorias():
		label_modificar_categoria = CTkLabel(frame_categorias, text="Para modificar una categoria haga click sobre ella en la tabla", text_color=azul, font=fuente_default)
		label_eliminar_categoria = CTkLabel(frame_categorias, text="Para dar de baja una categoria haga click sobre ella en la tabla", text_color='red', font=fuente_default)
		label_alta_categoria = CTkLabel(frame_categorias, text="Para dar de alta una categoria haga click sobre ella en la tabla", text_color='green', font=fuente_default)



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

		def listarCategoriasInac():
			for item in lista_categorias.get_children():
				lista_categorias.delete(item)
			categorias = []
			categorias = base_de_datos.listarCategoriasInactivas()
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
			
		def ocultar_widgets_categorias():

			for widget in frame_contenido_categorias.winfo_children():
				try:
					widget.pack_forget()
					widget.place_forget()
					widget.grid_forget()
				except:
					pass


		def menu_categorias():
			ocultar_widgets_categorias()
			frame_contenido_categorias.pack_forget()
			label_modificar_categoria.place_forget()
			
			global label_busqueda, entry_busqueda_categoria, boton_manipular_categorias, lista_categorias, frame_top_categorias, entrada, label_categorias
			if 'modCategorias' not in globals():
				global modCategorias 
				modCategorias = True
				frame_top_categorias = CTkFrame(frame_categorias, corner_radius=0, fg_color=verde_oscuro)
				label_busqueda = CTkLabel(frame_top_categorias, text="Buscar categoria:", font=fuente_default, text_color='white')
				entry_busqueda_categoria = CTkEntry(frame_top_categorias, font=fuente_default)				
				opciones = ['Crear categoria','Modificar categoria','Eliminar categoria', 'Categorias inactivas']
				boton_manipular_categorias = CTkOptionMenu(frame_top_categorias, values=opciones,font=fuente_default, command=seleccion_categoria)
				label_categorias= CTkLabel(frame_categorias, text="CATEGORIAS", text_color='white', bg_color=verde_oscuro, font=fuente_titulos)
				lista_categorias = ttk.Treeview(frame_categorias, columns=('categoria'))
				lista_categorias.column("#0", anchor="center", width=60)
				lista_categorias.column("categoria", anchor="center", width=500)
				lista_categorias.heading("#0", text="ID", anchor="center")
				lista_categorias.heading("categoria", text="Categoria", anchor="center")
				
			frame_categorias.pack(fill=BOTH, expand=True)
			frame_top_categorias.pack(side=TOP, fill=X, ipady=12)
			label_busqueda.pack(side=LEFT, padx=(20,4))
			entry_busqueda_categoria.pack(side=LEFT)
			entry_busqueda_categoria.delete(0, END)
			entry_busqueda_categoria.bind("<KeyRelease>", actualizar_entrada_categorias)
			boton_manipular_categorias.pack(side=RIGHT, padx=20)
			boton_manipular_categorias.configure(state='normal')
			boton_manipular_categorias.set("Seleccione una opcion")
			label_categorias.place(x=570, y=14)
			lista_categorias.pack(side=LEFT,padx=20, ipady=200)
			lista_categorias.bind("<Button-1>", block_event)
			lista_categorias.unbind("<<TreeviewSelect>>")
			listarCategorias()

				
		
		

		if 'modFramesContenido' not in globals():
			global modFramesContenido, entry_categoria, boton_volver_categorias	
			modFramesContenido = True
			entry_categoria = CTkEntry(frame_contenido_categorias, font=fuente_default, width=200)
			boton_volver_categorias= CTkButton(frame_contenido_categorias, text="Volver", command=lambda: [menu_categorias(), boton_manipular_categorias.configure(state='normal')])	

		def seleccion_categoria(opcion):
			ocultar_widgets_categorias()  # Asumo que tenés esta función para limpiar
			global label_error_categoria
			if opcion == 'Crear categoria':
			    label_modificar_categoria.place_forget()
			    label_eliminar_categoria.place_forget()
			    boton_manipular_categorias.configure(state='disabled')
			    lista_categorias.bind("<Button-1>", block_event)
			    if 'label_error_categoria' not in globals():
			    	label_error_categoria = CTkLabel(frame_contenido_categorias, text="Por favor ingrese todos los datos para \n crear la categoria correctamente", text_color="red")
			    label_error_categoria.pack_forget()
			        
			    def crear_categoria():
			        categoria = entry_categoria.get()
			        if categoria != "":
			        	validacion = True
			        	categorias = base_de_datos.listarCategorias()
			        	for categ in categorias:
			        		if categ[1] == categoria:
			        			messagebox.showwarning(message="Error, ya existe una categoria igual", title="Error")
			        			validacion = False
			        			break
			        	if validacion:
			        		base_de_datos.insertCategoria(categoria)
			        		listarCategorias()
			        		menu_categorias()
			        		boton_manipular_categorias.configure(state='normal')
			        		label_error_categoria.pack_forget()
			        else:
			        	label_error_categoria.pack(ipady=10)
			        
			    global boton_crear_categoria, label_crear_categoria
			    if 'modCrearCategoria' not in globals():
			        boton_crear_categoria = CTkButton(frame_contenido_categorias, text="Crear categoria", command=crear_categoria)
			        label_crear_categoria = CTkLabel(frame_contenido_categorias, text="Ingrese el nombre de la categoria", font=fuente_titulos, text_color=verde_intermedio)
			        global modCrearCategoria
			        modCrearCategoria = True
			        
			    # Si entry_categoria no existe, crearla una sola vez
			    global entry_categoria
			    if 'entry_categoria' not in globals():
			        entry_categoria = CTkEntry(frame_contenido_categorias)
			        
			    # Mostrar el frame y widgets
			    frame_contenido_categorias.pack(side=RIGHT, fill=Y, ipadx=20)
			    label_crear_categoria.pack(pady=10)
			    entry_categoria.pack(pady=(20,0))
			    entry_categoria.delete(0, END)
			    
			    boton_crear_categoria.pack(pady=10)
			    boton_volver_categorias.pack()
			        
			    
							
			elif(opcion == 'Modificar categoria'):
				lista_categorias.bind("<<TreeviewSelect>>")
				label_alta_categoria.place_forget()
				label_eliminar_categoria.place_forget()
				ocultar_widgets_categorias()
				frame_contenido_categorias.pack_forget()
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
							elif(categoria == 'Ingrese la cateogira'):
								messagebox.showwarning(message="Error, ingrese una categoria válida", title="Sistema huellitas")
							elif(categoria!= nombre):
								base_de_datos.actualizarCategoria(categoria, id_categoria)	
								listarCategorias()
								boton_manipular_categorias.configure(state='normal')
								messagebox.showinfo(message="La categoria fue modificada correctamente", title="Sistema huellitas")
								if frame_contenido_categorias.winfo_ismapped():
									frame_contenido_categorias.pack_forget()
									frame_contenido_categorias.update()
									label_modificar_categoria.place_forget()
									menu_categorias()

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
				listarCategorias()
				def dar_de_baja_categoria():
					label_alta_categoria.place_forget()
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
						menu_categorias()
					def verificar_seleccion_categoria2(evento):
						seleccion = lista_categorias.selection()
						if not seleccion:
							return


						index = seleccion
						valores = lista_categorias.item(index, 'values')
						if not valores or len(valores) == 0:
							return

						lista_categorias.unbind("<<TreeviewSelect>>")
						respuesta = messagebox.askyesno("Huellitas sistema", "Desea darle de baja a " + valores[0] +"?")
						if(respuesta == True):
							seleccion = lista_categorias.selection()
							index = seleccion
							id_categoria = lista_categorias.item(index, 'text')
							base_de_datos.darDeBajaCategoria(id_categoria)
							label_eliminar_categoria.place_forget()
							menu_categorias()

							
						elif(respuesta == False):
							lista_categorias.bind("<<TreeviewSelect>>", verificar_seleccion_categoria2)
							label_eliminar_categoria.place_forget()

					lista_categorias.bind("<<TreeviewSelect>>", verificar_seleccion_categoria2)

				if (opcion == 'Eliminar categoria'):
					dar_de_baja_categoria()

				

			elif(opcion == 'Categorias inactivas'):
				lista_categorias.unbind("<<TreeviewSelect>>")
				listarCategoriasInac()

				def dar_de_alta_categoria():
					label_alta_categoria.place_forget()
					label_modificar_categoria.place_forget()
					label_eliminar_categoria.place_forget()
					categoriasInactivas = []
					categoriasInactivas = base_de_datos.listarCategoriasInactivas()
					if(len(categoriasInactivas)>0):
						label_alta_categoria.place(x=110, y=60)
						lista_categorias.unbind("<Button-1>")
					elif(len(categoriasInactivas) == 0):
						boton_manipular_categorias.set("Seleccione una opcion")
						messagebox.showwarning(message="Error, no hay ninguna categoria inactiva en la base de datos", title="Sistema huellitas")
						menu_categorias()
					def verificar_seleccion_categoria3(evento):
						seleccion = lista_categorias.selection()
						if not seleccion:
							return


						index = seleccion
						valores = lista_categorias.item(index, 'values')
						if not valores or len(valores) == 0:
							return

						lista_categorias.unbind("<<TreeviewSelect>>")
						respuesta = messagebox.askyesno("Huellitas sistema", "Desea darle de alta a " + valores[0] +"?")
						if(respuesta == True):
							seleccion = lista_categorias.selection()
							index = seleccion
							id_categoria = lista_categorias.item(index, 'text')
							base_de_datos.darDeAltaCategoria(id_categoria)
							label_alta_categoria.place_forget()
							menu_categorias()

							
						elif(respuesta == False):
							lista_categorias.bind("<<TreeviewSelect>>", verificar_seleccion_categoria3)

					lista_categorias.bind("<<TreeviewSelect>>", verificar_seleccion_categoria3)

				if (opcion == 'Categorias inactivas'):
					dar_de_alta_categoria()

		menu_categorias()

	global imagen_categorias
	imagen_categorias = Image.open(os.path.join(carpeta_imagenes, "categorias.png"))
	imagen_categorias1 = CTkImage(dark_image=imagen_categorias, size=(30, 30))

	boton_categorias = CTkButton(frame_menu, image=imagen_categorias1, compound='left', text="Categorias", fg_color=verde_claro, text_color=gris_oscuro, font=fuente_default, command=categorias, anchor='w', width=150, height=40, corner_radius=0)
	boton_categorias.pack(ipady=6)

	def proveedores():
		label_modificar_proveedor = CTkLabel(frame_proveedores, text="Para modificar un proveedor haga click sobre él en la tabla", text_color=azul, font=fuente_default)
		label_eliminar_proveedor = CTkLabel(frame_proveedores, text="Para dar de baja un proveedor haga click sobre él en la tabla", text_color='red', font=fuente_default)
		label_alta_proveedor = CTkLabel(frame_proveedores, text="Para dar de alta un proveedor haga click sobre él en la tabla", text_color='green', font=fuente_default)

		label_modificar_cuenta = CTkLabel(frame_cuentas, text="Para modificar una cuenta haga click sobre ella en la tabla", text_color=azul, font=fuente_default)
		label_eliminar_cuenta = CTkLabel(frame_cuentas, text="Para eliminar una cuenta haga click sobre ella en la tabla", text_color='red', font=fuente_default)

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

		def listarCuentas():
			for item in lista_cuentas.get_children():
				lista_cuentas.delete(item)
			cuentas = []
			cuentas = base_de_datos.listarCuentas()
			for cuenta in cuentas:
				id = cuenta[0]
				fecha = cuenta[1]
				proveedor = cuenta[2]
				saldo = cuenta[3]
				pagos = cuenta[4]
				pedidos = cuenta[5]
				lista_cuentas.insert("", "end", text=id, values=(fecha, proveedor, pagos, pedidos, saldo))

		def listarProveedoresInac():
			for item in lista_proveedores.get_children():
				lista_proveedores.delete(item)
			proveedores = []
			proveedores = base_de_datos.listarProveedoresInactivos()
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

		def ocultar_widgets_proveedores():
			for widget in frame_contenido_proveedores.winfo_children():
				widget.pack_forget()

		def cuentas_proveedores():
			ocultar_widgets_cuentas()
			frame_proveedores.pack_forget()
			frame_contenido_cuentas.pack_forget()
			frame_cuentas.pack(fill=BOTH, expand=True)
			label_modificar_cuenta.place_forget()
			label_eliminar_cuenta.place_forget()

			def listarCuentasProv(proveedor):
				prov = proveedor 
				for item in lista_cuentas.get_children():
					lista_cuentas.delete(item)
				cuentas = []
				cuentas = base_de_datos.listarCuentasPorProveedor(prov)
				for cuenta in cuentas:
					id = cuenta[0]
					fecha = cuenta[1]
					proveedor = cuenta[2]
					saldo = cuenta[3]
					pagos = cuenta[4]
					pedidos = cuenta[5]
					lista_cuentas.insert("", "end", text=id, values=(fecha, proveedor, pagos, pedidos, saldo))
				if(len(cuentas) == 0):
					messagebox.showwarning(message="Error, no hay ninguna cuenta registrada a este proveedor", title="Error")

			def borrar_filtros_cuentas():
				
				for widget in lista_cuentas.winfo_children():
					widget.destroy()
				listarCuentas()
				boton_proveedores_cuentas.set("Seleccione un proveedor")
				

			global frame_top_cuentas, boton_volver_prov, boton_proveedores_cuentas, lista_cuentas, boton_manipular_cuentas, lista_cuentas, boton_proveedores_cuentas, label_prov, label_cuentas, linea_cuentas, boton_borrar_filtros_c
			if 'modCuentas' not in globals():
				global modCuentas
				modCuentas = True
				frame_top_cuentas = CTkFrame(frame_cuentas, corner_radius=0, fg_color=verde_oscuro)
				opciones_cuentas = ["Nueva cuenta", "Modificar cuentas", "Eliminar cuentas"]
				boton_manipular_cuentas = CTkOptionMenu(frame_top_cuentas, values=opciones_cuentas, font=fuente_default, command=seleccion_cuentas)
				boton_volver_prov = CTkButton(frame_top_cuentas, text="Volver", font=fuente_default, command=menu_proveedores, fg_color=azul, hover_color=azul_oscuro)
				boton_borrar_filtros_c = CTkButton(frame_top_cuentas, text="Borrar filtro", font=fuente_default, command=borrar_filtros_cuentas)
				proveedores = []
				proveedores = base_de_datos.listarProveedores()
				nombre_proveedor = [prooved[1] for prooved in proveedores]
				label_prov = CTkLabel(frame_cuentas, text="Proveedor: ", font=fuente_default)
				boton_proveedores_cuentas = CTkOptionMenu(frame_cuentas, values=nombre_proveedor, font=fuente_default, command=listarCuentasProv)
				label_cuentas= CTkLabel(frame_cuentas, text="CUENTAS", text_color='white', bg_color=verde_oscuro, font=fuente_titulos)
				linea_cuentas = CTkFrame(frame_top_cuentas, height=25, width=3)
				lista_cuentas = ttk.Treeview(frame_cuentas)
				lista_cuentas["columns"] = ("fecha", "proveedor","pagos" ,"pedidos" ,"saldo")
				lista_cuentas.column("#0", anchor="center", width=100)
				lista_cuentas.column("fecha", anchor="center", width=120)
				lista_cuentas.column("proveedor", anchor="center", width=160)
				lista_cuentas.column("pagos", anchor="center", width=150)
				lista_cuentas.column("pedidos", anchor="center", width=150)
				lista_cuentas.column("saldo", anchor="center", width=150)
				lista_cuentas.heading("#0", text="N° Cuenta", anchor="center")
				lista_cuentas.heading("fecha", text="Fecha", anchor="center")
				lista_cuentas.heading("proveedor", text="Proveedor", anchor="center")
				lista_cuentas.heading("pagos", text="Pagos", anchor="center")
				lista_cuentas.heading("pedidos", text="Pedidos", anchor="center")
				lista_cuentas.heading("saldo", text="Saldo", anchor="center")

			frame_cuentas.pack(fill=BOTH, expand=True)
			frame_top_cuentas.pack(side=TOP, fill=X, ipady=12)
			boton_manipular_cuentas.pack(side=RIGHT, padx=10)
			linea_cuentas.pack(side=RIGHT, padx=15)
			boton_borrar_filtros_c.pack(side=LEFT,padx=20)
			boton_manipular_cuentas.configure(state='normal')
			boton_manipular_cuentas.set("Seleccione una opcion")
			boton_volver_prov.pack(side=RIGHT, padx=20)
			
			label_prov.place(x=22, y=60)
			boton_proveedores_cuentas.place(x=110, y=60)
			proveedores = []
			proveedores = base_de_datos.listarProveedores()
			nombre_proveedor = [prooved[1] for prooved in proveedores]
			boton_proveedores_cuentas.configure(values=nombre_proveedor)
			label_cuentas.place(x=570, y=14)
			lista_cuentas.pack(side=LEFT,padx=20, ipady=200)
			lista_cuentas.unbind("<<TreeviewSelect>>")
			listarCuentas()
		def ocultar_widgets_cuentas():
			for widget in frame_contenido_cuentas.winfo_children():
				widget.pack_forget()

		if 'modFramesCuentas' not in globals():
			global modFramesCuentas, entry_fecha, entry_proveedores_cuentas, entry_pagos, entry_pedidos, entry_saldo , label_error_cuenta
			modFramesCuentas = True
			proveedores = []
			proveedores = base_de_datos.listarProveedores()
			nombre_proveedor = [prooved[1] for prooved in proveedores]
			entry_proveedores_cuentas = CTkOptionMenu(frame_contenido_cuentas, values=nombre_proveedor, font=fuente_default)
			entry_fecha = DateEntry(frame_contenido_cuentas, date_pattern='dd/mm/yy', font=fuente_default)
			entry_pagos = CTkEntry(frame_contenido_cuentas, font=fuente_default, width=200)
			entry_pedidos = CTkEntry(frame_contenido_cuentas, font=fuente_default, width=200)
			entry_saldo = CTkEntry(frame_contenido_cuentas, font=fuente_default, width=200)
			label_error_cuenta = CTkLabel(frame_contenido_cuentas, text="Por favor ingrese todos los datos para cargar \n la cuenta correctamente", text_color="red")

			label_proveedores_c = CTkLabel(frame_contenido_cuentas, font=fuente_default, text="Proveedor:", anchor="e")
			label_fecha_c = CTkLabel(frame_contenido_cuentas, font=fuente_default, text="Fecha:", anchor="e")
			label_pagos_c = CTkLabel(frame_contenido_cuentas, font=fuente_default, text="Pago:", anchor="e")
			label_pedidos_c = CTkLabel(frame_contenido_cuentas, font=fuente_default, text="Pedido:", anchor="e")
			label_saldo_c = CTkLabel(frame_contenido_cuentas, font=fuente_default, text="Saldo:", anchor="e")

			boton_volver_cuentas= CTkButton(frame_contenido_cuentas, text="Volver", command=lambda: [cuentas_proveedores(), boton_manipular_cuentas.configure(state='normal')], font=fuente_default)


		def seleccion_cuentas(opcion):
			ocultar_widgets_cuentas()
			if(opcion == 'Nueva cuenta'):
				label_modificar_cuenta.place_forget()
				label_eliminar_cuenta.place_forget()
				label_error_cuenta.grid_forget()
				boton_manipular_cuentas.configure(state='disabled')
				lista_cuentas.bind("<Button-1>", block_event)

				if not frame_contenido_cuentas.winfo_ismapped():
					def cargar_cuenta():
						fecha = entry_fecha.get()
						proveedor = entry_proveedores_cuentas.get()
						saldo = entry_saldo.get()
						pago = entry_pagos.get()
						pedidos = entry_pedidos.get()

						if (fecha != "" and proveedor !="" and saldo !="" and pago != "" and pedidos != ""):
							cuenta = Cuenta(fecha, proveedor, saldo, pago, pedidos)
							base_de_datos.insertCuenta(cuenta)
							label_error_cuenta.pack_forget()
							listarCuentas()
							cuentas_proveedores()

						else:
							label_error_cuenta.grid(row=8, column=0, columnspan=2, pady=10)

				global boton_crear_cuenta, label_crear_cuenta
				if 'modCrearCuenta' not in globals():	
					boton_crear_cuenta = CTkButton(frame_contenido_cuentas, text="Cargar cuenta", command=cargar_cuenta, font=fuente_default)
					label_crear_cuenta = CTkLabel(frame_contenido_cuentas, text="Ingrese los datos de la cuenta a cargar", font=fuente_default, text_color=verde_intermedio)
					
					global modCrearCuenta
					modCrearCuenta = True

				label_error_cuenta.pack_forget()

				frame_contenido_cuentas.pack(side=RIGHT, fill=Y, ipadx=40)

				label_crear_cuenta.pack()

				label_proveedores_c.pack(anchor=NW, padx=35)
				entry_proveedores_cuentas.pack(ipadx=70, pady=(0,5))
				proveedores = []
				proveedores = base_de_datos.listarProveedores()
				nombre_proveedor = [prooved[1] for prooved in proveedores]
				entry_proveedores_cuentas.configure(values=nombre_proveedor)
				
				label_fecha_c.pack(anchor=NW, padx=35)
				entry_fecha.pack(ipadx=70, pady=(0,5))

				label_pagos_c.pack(anchor=NW, padx=35)
				entry_pagos.pack(ipadx=37, pady=(0,5))

				label_pedidos_c.pack(anchor=NW, padx=35)
				entry_pedidos.pack(ipadx=37, pady=(0,5))

				label_saldo_c.pack(anchor=NW, padx=35)
				entry_saldo.pack(ipadx=37, pady=(0,5))

				boton_crear_cuenta.pack(pady=5)
				boton_volver_cuentas.pack(pady=10)

			
				#CODIGO PARA BORRAR TODO CADA VEZ QUE TOCAMOS EL BOTON
				
				entry_pagos.delete(0, END)
				entry_pedidos.delete(0, END)
				entry_saldo.delete(0, END)

				
				entry_pagos.configure(placeholder_text="Ingrese el pago si es que lo hubo")
				entry_pedidos.configure(placeholder_text="Ingrese el saldo del pedido si es que lo hubo")
				entry_saldo.configure(placeholder_text="Ingrese el saldo total")

			elif(opcion== 'Modificar cuentas'):
				lista_cuentas.bind("<<TreeviewSelect>>")
				label_eliminar_cuenta.place_forget()
				cuentas = []
				cuentas = base_de_datos.listarCuentas()
				if (len(cuentas) > 0):
					label_modificar_cuenta.place(x=400, y=60)
					lista_cuentas.unbind("<Button-1>")
					def modificar_cuenta():
						bandera = False
						##OBTENEMOS EL ID DE LA CUENTA
						seleccion = lista_cuentas.selection()
						index = seleccion
						id_cuenta = lista_cuentas.item(index, 'text')
						#OBTENEMOS LOS VALORES DEL PROVEEDOR
						values = lista_cuentas.item(seleccion)["values"]
						fecha = entry_fecha.get()
						proveedor = entry_proveedores_cuentas.get()
						pagos = entry_pagos.get()
						pedidos = entry_pedidos.get()
						saldo = entry_saldo.get()
						if(fecha != "" and proveedor !="" and pagos !="" and pedidos !="" and saldo !=""):
							
							for cuenta in cuentas:
								
								if(fecha == cuenta[1] and proveedor == cuenta[2] and int(saldo) == cuenta[3] and int(pagos) == cuenta[4] and int(pedidos) == cuenta[5]):
									messagebox.showwarning(message="Error, no puede modificar la cuenta con los mismos datos existentes, debe haber algun campo diferente para que se modifique", title="Sistema huellitas")
									bandera = True
							if(bandera == False):
								cuenta = Cuenta(fecha, proveedor, saldo, pagos, pedidos)
								base_de_datos.actualizarCuenta(cuenta, id_cuenta)
								listarCuentas()
								messagebox.showinfo(message="La cuenta fue modificado correctamente", title="Sistema huellitas")
								if frame_contenido_cuentas.winfo_ismapped():
									frame_contenido_cuentas.pack_forget()
									frame_contenido_cuentas.update()
									cuentas_proveedores()			
						else:
							messagebox.showwarning(message="Porfavor complete todos los campos para modificar la cuenta correctamente", title="Sistema huellitas")

				elif(len(cuentas) == 0):
					boton_manipular_cuentas.set("Seleccione una opcion")
					messagebox.showwarning(message="No hay ninguna cuenta  cargada en la base de datos", title="Sistema huellitas")

				def verificar_seleccion_cuenta(evento):
					label_modificar_cuenta.place_forget()
					label_eliminar_cuenta.place_forget()
					boton_manipular_cuentas.configure(state='disabled')
					seleccion = lista_cuentas.selection()
					index = seleccion
					valores = lista_cuentas.item(index, 'values')
					global boton_modificar_cuenta, label_modificar_c
					if 'modModificarCuenta' not in globals():
						boton_modificar_cuenta = CTkButton(frame_contenido_cuentas, text="Modificar cuenta", command= modificar_cuenta, font=fuente_default)
						label_modificar_c = CTkLabel(frame_contenido_cuentas, text="Ingrese los nuevos datos de la cuenta", font=fuente_titulos, text_color=verde_intermedio)
						global modModificarCuenta
						modModificarCuenta = True
					frame_contenido_cuentas.pack(side=RIGHT, fill=Y, ipadx=20)
					label_modificar_c.pack(pady=10)
					
					label_proveedores_c.pack(anchor=NW, padx=35)
					entry_proveedores_cuentas.pack(ipadx=70, pady=(0,5))
					
					label_fecha_c.pack(anchor=NW, padx=35)
					entry_fecha.pack(ipadx=70, pady=(0,5))

					label_pagos_c.pack(anchor=NW, padx=35)
					entry_pagos.pack(ipadx=37, pady=(0,5))
					entry_pagos.delete(0,END)

					label_pedidos_c.pack(anchor=NW, padx=35)
					entry_pedidos.pack(ipadx=37, pady=(0,5))
					entry_pedidos.delete(0,END)

					label_saldo_c.pack(anchor=NW, padx=35)
					entry_saldo.pack(ipadx=37, pady=(0,5))
					entry_saldo.delete(0,END)
					
					if (len(valores) >1):
						entry_fecha.set_date(valores[0])
						entry_proveedores_cuentas.set(valores[1])
						entry_pagos.insert(0, valores[2])
						entry_pedidos.insert(0, valores[3])
						entry_saldo.insert(0, valores[4])

					boton_modificar_cuenta.pack(pady=10,ipadx=5)
					boton_volver_cuentas.pack()

				lista_cuentas.bind("<<TreeviewSelect>>", verificar_seleccion_cuenta)


			elif(opcion== 'Eliminar cuentas'):
				def eliminar_cuenta():
					listarCuentas()
					label_modificar_cuenta.place_forget()
					cuentas = []
					cuentas = base_de_datos.listarCuentas()
					if(len(cuentas)>0):
						label_eliminar_cuenta.place(x=400, y=60)
						lista_cuentas.unbind("<Button-1>")
					elif(len(cuentas)==0):
						boton_manipular_cuentas.set("Seleccione una opcion")
						messagebox.showwarning(message="Error, no hay ninguna cuenta en la base de datos", title="Sistema huellitas")
						cuentas_proveedores()

					def verificar_seleccion_cuentas2(evento):
						seleccion = lista_cuentas.selection()
						if not seleccion:
							return
						index = seleccion
						valores = lista_cuentas.item(index, 'values')
						if not valores or len(valores) == 0:
							return
						lista_cuentas.unbind("<<TreeviewSelect>>")
						respuesta = messagebox.askyesno("Huellitas sistema", "Desea eliminar la siguiente cuenta " + valores[0] +"?")
						if(respuesta == True):
							seleccion = lista_cuentas.selection()
							index = seleccion
							id_cuenta = lista_cuentas.item(index, 'text')
							base_de_datos.eliminarCuenta(id_cuenta)
							label_eliminar_cuenta.place(x=400, y=60)
							cuentas_proveedores()
						elif(respuesta==False):
							lista_cuentas.bind("<<TreeviewSelect>>", verificar_seleccion_cuentas2)
							label_eliminar_cuenta.place_forget()

					lista_cuentas.bind("<<TreeviewSelect>>", verificar_seleccion_cuentas2)
				if (opcion== 'Eliminar cuentas'):
					eliminar_cuenta()


		def menu_proveedores():
			frame_cuentas.pack_forget()
			label_modificar_proveedor.place_forget()
			label_eliminar_proveedor.place_forget()
			label_alta_proveedor.place_forget()
			frame_contenido_proveedores.pack_forget()
			global frame_top_proveedores, label_busqueda, entry_busqueda_proveedores, boton_manipular_proveedores, lista_proveedores, boton_cuentas_proveedores, label_proveedores
			if 'modProveedores' not in globals():
				global modProveedores
				modProveedores = True
				frame_top_proveedores = CTkFrame(frame_proveedores, corner_radius=0, fg_color=verde_oscuro)
				label_busqueda = CTkLabel(frame_top_proveedores, text="Buscar proveedor:", font=fuente_default, text_color='white')
				entry_busqueda_proveedores = CTkEntry(frame_top_proveedores, font=fuente_default)
				opciones = ["Nuevo proveedor", "Modificar proveedor", "Eliminar proveedor", "Proveedores inactivos"]
				boton_manipular_proveedores = CTkOptionMenu(frame_top_proveedores, values=opciones, command=seleccion_proveedores, font=fuente_default)
				boton_cuentas_proveedores = CTkButton(frame_top_proveedores, text="Cuentas proveedores", font=fuente_default, command=cuentas_proveedores, hover_color=azul_oscuro, fg_color=azul)
				label_proveedores= CTkLabel(frame_proveedores, text="PROVEEDORES", font=fuente_titulos, text_color='white', bg_color=verde_oscuro)
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
			label_busqueda.pack(side=LEFT, padx=(20,4))
			entry_busqueda_proveedores.pack(side=LEFT)
			entry_busqueda_proveedores.bind("<KeyRelease>", actualizar_entrada_proveedores)
			boton_cuentas_proveedores.pack(side=RIGHT,padx=20)
			boton_manipular_proveedores.pack(side=RIGHT, padx=20)
			boton_manipular_proveedores.configure(state='normal')
			boton_manipular_proveedores.set("Seleccione una opcion")
			label_proveedores.place(x=570, y=14)
			lista_proveedores.pack(side=LEFT,padx=20, ipady=200)
			lista_proveedores.bind("<Button-1>", block_event)
			lista_proveedores.unbind("<<TreeviewSelect>>")
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
									menu_proveedores()
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
				lista_proveedores.unbind("<<TreeviewSelect>>")
				label_modificar_proveedor.place_forget()
				label_eliminar_proveedor.place_forget()
				label_alta_proveedor.place_forget()
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
								messagebox.showinfo(message="El proveedor fue modificado correctamente", title="Sistema huellitas")
								if frame_contenido_proveedores.winfo_ismapped():
									frame_contenido_proveedores.pack_forget()
									frame_contenido_proveedores.update()
									menu_proveedores()			
						else:
							messagebox.showwarning(message="Porfavor complete todos los campos para modificar el proveedor correctamente", title="Sistema huellitas")
				elif(len(proveedores) == 0):
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
				def dar_de_baja_proveedor():
					listarProveedores()
					label_modificar_proveedor.place_forget()
					label_eliminar_proveedor.place_forget()
					label_alta_proveedor.place_forget()
					proveedores = []
					proveedores = base_de_datos.listarProveedores()
					if(len(proveedores)>0):
						label_eliminar_proveedor.place(x=110, y=60)
						lista_proveedores.unbind("<Button-1>")
					elif(len(proveedores)==0):
						boton_manipular_proveedores.set("Seleccione una opcion")
						messagebox.showwarning(message="Error, no hay ningun proveedor en la base de datos", title="Sistema huellitas")
						menu_proveedores()
					def verificar_seleccion_proveedor2(evento):
						seleccion = lista_proveedores.selection()
						if not seleccion:
							return


						index = seleccion
						valores = lista_proveedores.item(index, 'values')
						if not valores or len(valores) == 0:
							return

						lista_proveedores.unbind("<<TreeviewSelect>>")
						respuesta = messagebox.askyesno("Huellitas sistema", "Desea darle de baja a " + valores[0] +"?")
						if(respuesta == True):
							seleccion = lista_proveedores.selection()
							index = seleccion
							id_proveedor = lista_proveedores.item(index, 'text')
							base_de_datos.darDeBajaProveedor(id_proveedor)
							label_eliminar_proveedor.place(x=110, y=60)
							menu_proveedores()
						elif(respuesta==False):
							lista_proveedores.bind("<<TreeviewSelect>>", verificar_seleccion_proveedor2)
							label_eliminar_proveedor.place_forget()

					lista_proveedores.bind("<<TreeviewSelect>>", verificar_seleccion_proveedor2)
				if (opcion== 'Eliminar proveedor'):
					dar_de_baja_proveedor()

			elif(opcion == "Proveedores inactivos"):
				lista_proveedores.unbind("<<TreeviewSelect>>")
				listarProveedoresInac()

				def dar_de_alta_proveedor():
					label_modificar_proveedor.place_forget()
					label_eliminar_proveedor.place_forget()
					label_alta_proveedor.place_forget()
					listarProveedoresInac = []
					listarProveedoresInac = base_de_datos.listarProveedoresInactivos()
					if(len(listarProveedoresInac)>0):
						label_alta_proveedor.place(x=110, y=60)
						lista_proveedores.unbind("<Button-1>")
					elif(len(listarProveedoresInac)==0):
						boton_manipular_proveedores.set("Seleccione una opcion")
						messagebox.showwarning(message="Error, no hay ningun proveedor dado de baja en la base de datos", title="Sistema huellitas")
						menu_proveedores()
					def verificar_seleccion_proveedor2(evento):
						seleccion = lista_proveedores.selection()
						if not seleccion:
							return


						index = seleccion
						valores = lista_proveedores.item(index, 'values')
						if not valores or len(valores) == 0:
							return

						lista_proveedores.unbind("<<TreeviewSelect>>")
						respuesta = messagebox.askyesno("Huellitas sistema", "Desea darle de alta a " + valores[0] +"?")
						if(respuesta == True):
							seleccion = lista_proveedores.selection()
							index = seleccion
							id_proveedor = lista_proveedores.item(index, 'text')
							base_de_datos.darDeAltaProveedor(id_proveedor)
							label_alta_proveedor.place(x=110, y=60)
							menu_proveedores()
							
						elif(respuesta==False):
							lista_proveedores.bind("<<TreeviewSelect>>", verificar_seleccion_proveedor2)

					lista_proveedores.bind("<<TreeviewSelect>>", verificar_seleccion_proveedor2)

				if (opcion == 'Proveedores inactivos'):
					dar_de_alta_proveedor()

		menu_proveedores()


	global imagen_proveedores
	imagen_proveedores = Image.open(os.path.join(carpeta_imagenes, "proveedores.png"))
	imagen_proveedores1 = CTkImage(dark_image=imagen_proveedores, size=(30, 30))

	boton_proveedores = CTkButton(frame_menu,image=imagen_proveedores1 ,compound='left' ,text="Proveedores", fg_color=verde_claro, text_color=gris_oscuro, font=fuente_default, command=proveedores, anchor='w', width=150, height=40, corner_radius=0)
	boton_proveedores.pack(ipady=6)

	def limpiar_articulos():
		for widget in frame_articulos2.winfo_children():
			widget.destroy()


	def ventas():


		borrar_frames()
		global total
		total = IntVar(value=0)
		carpeta_tickets = "Tickets"
		def menu_ventas():
			
			global carrito
			carrito ={}


			limpiar_articulos()

			
			def vender():
				
				if(len(carrito) != 0):
					for info in carrito.values():
						nombre_articulo = info['nombre']
						cantidad_comprada = info['cantidad']

						cantidad_vieja_tupla = base_de_datos.traerCantidadVieja(nombre_articulo)
						cantidad_vieja = int(cantidad_vieja_tupla[0][0])
						cantidad_nueva = cantidad_vieja - cantidad_comprada
						if(cantidad_nueva>0):
							base_de_datos.actualizarCantidadArt(nombre_articulo, cantidad_nueva)

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
							nuevoPdf.drawString(50,750, "Fecha:")
							nuevoPdf.drawString(110, 750, fechaActual)
							y=600
							nuevoPdf.drawString(50, 660, "Producto")
							nuevoPdf.drawString(300, 660, "Cantidad")
							nuevoPdf.drawString(400, 660, "P/Unitario")
							global total_carrito1
							total_carrito1 = 0
							for info in carrito.values():
								precio = info["precio"]
								cantidad = info["cantidad"]
								total_carrito1 = total_carrito1 + (precio * cantidad)
							for id_producto, datos in carrito.items():
								nuevoPdf.drawString(50, y, str(datos["nombre"]))
								nuevoPdf.drawString(300, y, str(datos["cantidad"]))
								nuevoPdf.drawString(400, y, "$" +  str(datos["precio"]))
								y-=20
								nuevoPdf.drawString(410, 80, "Total: $" + str(total_carrito1))
							nuevoPdf.save()
							subprocess.Popen(nombreArchivo, shell=True)

						elif(cantidad_nueva<0):
							messagebox.showwarning("Huellitas", "Estas intentando vender mas cantidad de la debida en un producto del carrito")
								
					
				else:
					messagebox.showwarning(message="No hay ningun articulo en el carrito", title="Sistema huellitas")


			
			def actualizar_entrada_articulos_ventas(*args):
				fila_ac = 0
				column = 0
				articulos = []
				articulos = base_de_datos.listarPyNArticulosVentas()
				buscador = entry_busqueda.get().lower()
				
				limpiar_articulos()

				for articulo in articulos:
					nombre_articulo1 = articulo[1].lower()
					if nombre_articulo1.startswith(buscador):
						
						tarjeta = CTkFrame(frame_articulos2, fg_color='#DFDFDF')
						tarjeta.grid(row=fila_ac, column = column, padx=15, pady=(40,0), sticky="nsew")

						informacion = articulo[1] + "\n" + "$" + str(articulo[2])
						label_articulo1 = CTkLabel(tarjeta, text=informacion, text_color=gris_oscuro)
						label_articulo1.pack(padx=5,pady=(10,5))
						boton_agregar_carrito = CTkButton(tarjeta, text="Agregar al carrito", command=lambda art=articulo: agregar_al_carrito(art))
						boton_agregar_carrito.pack(pady=(0,10),padx=10)
						column += 1
						if column >= 4:
							column = 0
							fila_ac += 1
				if(buscador== ""):
					limpiar_articulos()
					listar_articulos_ventas()

			def buscar_articulos(opcion):
				categoria = opcion

				articulos1 = []
				articulos1 = base_de_datos.listarPyNArticulosVentasPorCat(categoria)
				columna_actual = 0
				fila_actual = 0
				if (len(articulos1) > 0 ):
					limpiar_articulos()
					for articulo in articulos1:
						#creamos la tarjeta del articulo
						tarjeta = CTkFrame(frame_articulos2, fg_color='#DFDFDF')
						tarjeta.grid(row=fila_actual, column = columna_actual, padx=15, pady=(40,0), sticky="nsew")



						informacion = articulo[1] + "\n" + "$" + str(articulo[2])
						label_articulo1 = CTkLabel(tarjeta, text=informacion, text_color=gris_oscuro)
						label_articulo1.pack(padx=5,pady=(10,5))
						boton_agregar_carrito = CTkButton(tarjeta, text="Agregar al carrito", command=lambda art=articulo: agregar_al_carrito(art))
						boton_agregar_carrito.pack(pady=(0,10),padx=10)

						columna_actual += 1
						if columna_actual == 4:
							columna_actual = 0
							fila_actual += 1
				elif(len(articulos1) == 0):
					limpiar_articulos()
					articulosNulos = CTkLabel(frame_articulos2, text="Esta categoria no contiene ningun articulo", font=fuente_default, text_color=azul_oscuro)
					articulosNulos.place(x=255,y=250)


			def borrar_filtros():
				limpiar_articulos()
				listar_articulos_ventas()
				categorias_ventas.set("Seleccione una categoria")
				entry_busqueda.delete(0, END)
					
			
			global label_vender,label_articulos, frame_busqueda, frame_carrito, entry_busqueda, boton_vender, label_total,label_carrito, label_total_precio, frame_carrito_articulos, frame_carrito_total,label_articulo,label_precio,label_cantidad,label_total,label_total_precio,boton_vender, label_busqueda, label_articulos_carrito, categorias_ventas, label_categoria, boton_borrar_filtros 
			if 'modVentas' not in globals():
				global modVentas
				modVentas = True
				frame_busqueda= CTkFrame(frame_ventas, fg_color='white', corner_radius=10, height=80)
				label_busqueda = CTkLabel(frame_busqueda, text="Buscar articulo", font=fuente_default)
				label_categoria = CTkLabel(frame_busqueda, text="Buscar por categoria", font=fuente_default)
				categorias = []
				categorias = base_de_datos.listarCategorias()
				nombre_categoria = [categoria[1] for categoria in categorias]
				categorias_ventas = CTkOptionMenu(frame_busqueda, values=nombre_categoria, font=fuente_default, command=buscar_articulos)
				entry_busqueda = CTkEntry(frame_busqueda, font=fuente_default)

				boton_borrar_filtros = CTkButton(frame_busqueda, text="Borrar filtros", command=borrar_filtros, fg_color=azul, hover_color=azul_oscuro, font=fuente_default)

				label_articulos_carrito= CTkLabel(frame_ventas, text="ARTICULOS", font=fuente_ventas, text_color=verde_oscuro)
				

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
			entry_busqueda.bind("<KeyRelease>", actualizar_entrada_articulos_ventas)
			

			label_categoria.pack(side=LEFT, padx=(40,5))
			categorias_ventas.pack(side=LEFT)
			categorias_ventas.set("Seleccione una categoria")
			boton_borrar_filtros.pack(side=RIGHT, padx=30)
			label_articulos_carrito.place(x=350, y=80)
			
			

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
			boton_vender.grid(row=1,column=3,pady=(10,10))
			
			categorias = []
			categorias = base_de_datos.listarCategorias()
			nombre_categoria = [categoria[1] for categoria in categorias]
			categorias_ventas.configure(values=nombre_categoria)

			articulos = []
			articulos = base_de_datos.listarPyNArticulosVentas()

			global columna_actual, fila_actual, columna1, fila1
			
			columna1 = 0
			fila1 = 0
			carrito = {}

			def listar_articulos_ventas():
				columna_actual = 0
				fila_actual = 0
				for articulo in articulos:
					#creamos la tarjeta del articulo
					tarjeta = CTkFrame(frame_articulos2, fg_color='#DFDFDF')
					tarjeta.grid(row=fila_actual, column = columna_actual, padx=15, pady=(40,0), sticky="nsew")



					informacion = articulo[1] + "\n" + "$" + str(articulo[2])
					label_articulo1 = CTkLabel(tarjeta, text=informacion, text_color=gris_oscuro)
					label_articulo1.pack(padx=5,pady=(10,5))
					boton_agregar_carrito = CTkButton(tarjeta, text="Agregar al carrito", command=lambda art=articulo: agregar_al_carrito(art))
					boton_agregar_carrito.pack(pady=(0,10),padx=10)

					columna_actual += 1
					if columna_actual == 4:
						columna_actual = 0
						fila_actual += 1

			

			def agregar_al_carrito(art):
				global carrito
				global fila1
				fila1 += 1
				global cantidad_anterior, total_precio, total_carrito
				cantidad_anterior = 0
				total_precio = 0
				total_carrito = 0
				global cantidad
				producto_id = art[0]
				nombre = art[1]
				precio= art[2]
				cantidad = 1


				label_nombre= CTkLabel(frame_carrito_articulos, text=nombre)
				label_monto = CTkLabel(frame_carrito_articulos, text=precio)

				carrito[producto_id] = {"nombre": nombre, "precio": precio, "cantidad":cantidad, "total":total_carrito}

				

				def opcion_seleccionada(opcion, producto_id = producto_id):
					
					global total_precio, cantidad_anterior, total_carrito
					cantidad = int(opcion_cantidad.get())
					precio_unitario = carrito[producto_id]["precio"]
					
					
					

					ids_productos = list(carrito.keys())
					


					if cantidad >=1:
						total_carrito = 0
						carrito[producto_id]["cantidad"] = cantidad


						total_precio = precio_unitario * cantidad
						label_monto.configure(text=total_precio)


						for info in carrito.values():
							precio = info["precio"]
							cantidad = info["cantidad"]

							total_carrito = total_carrito + (precio * cantidad)
							
							label_total_precio.configure(text=f"${total_carrito}")

					
				
				opciones = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
				opcion_cantidad = CTkOptionMenu(frame_carrito_articulos, values=opciones, font=fuente_default, width=10, command=lambda opcion: opcion_seleccionada(opcion, producto_id))
				label_nombre.grid(row=fila1, column=0, pady=5)
				label_monto.grid(row=fila1, column=1, pady=5)
				opcion_cantidad.grid(row=fila1, column=2, pady=5)


				total.set(total.get() + precio)
				label_total_precio.configure(text=f"${total.get()}")

			def limpiar_carrito():
				global carrito, fila1

				for widget in frame_carrito_articulos.winfo_children():
					info = widget.grid_info()
					if info["row"] > 0:
						widget.destroy()

				carrito.clear()
				fila1= 0 
				total.set(0)
				label_total_precio.configure(text="$0")

			limpiar_carrito()
				
			boton_limpiar_carrito = CTkButton(frame_carrito_total, text="Limpiar carrito", font=fuente_default, fg_color='red', command=limpiar_carrito)
			boton_limpiar_carrito.grid(row=1, column=0, padx=20)

			listar_articulos_ventas()

			frame_articulos2.grid_propagate(False)
			frame_articulos2.pack(side=LEFT,padx=10, ipady=78)
			

		menu_ventas()

	
	global imagen_ventas
	imagen_ventas = Image.open(os.path.join(carpeta_imagenes, "carrito.png"))
	imagen_ventas1 = CTkImage(dark_image=imagen_ventas, size=(30, 30))	

	boton_ventas = CTkButton(frame_menu, text="Ventas",image=imagen_ventas1, compound="left", fg_color=verde_claro, text_color=gris_oscuro, font=fuente_default, command=ventas, anchor='w', width=150, height=40, corner_radius=0)
	
	boton_ventas.pack(ipady=6)

	
	ventana_p.mainloop()
