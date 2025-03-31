from customtkinter import *
import customtkinter
from PIL import Image, ImageTk
import os
from manejo_db import baseDeDatos
import principal
import tkinter 
from tkinter import messagebox
##RUTAS
##CARPETA PRINCIPAL 
carpeta_principal = os.path.dirname(__file__)
##.Desktop\Proyecto final programacion
carpeta_imagenes = os.path.join(carpeta_principal, ("img"))
##.Desktop\Proyecto final programacion\img

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

##COLORES
gris_oscuro = '#EBEBEB'
gris_claro = '#8A8A8A'
verde_claro = '#02FA66'
verde_oscuro = '#058A3B'
#Creamos las fuentes

##CREAMOS LA BASE DE DATOS
base_de_datos = baseDeDatos()
base_de_datos.crearTabla()




def iniciar_sesion():
	ventana = CTk()
	ventana.geometry("800x500")
	ventana.title("Huellitas Sistema")
	ventana.iconbitmap(os.path.join(carpeta_imagenes, "huellitas.ico"))
	##Le ponemos que la ventana se centre en la pantalla
	ancho_pantalla = ventana.winfo_screenwidth()
	alto_pantalla = ventana.winfo_screenheight()
	x = (ancho_pantalla // 2) - (800 // 2) 
	y = (alto_pantalla // 2) - (500 // 2)
	ventana.geometry(f"800x500+{x}+{y}")

	#fuentes
	fuente_login = CTkFont(family="Ebrima", size=14, weight="bold")
	fuente_marca = CTkFont(family="Myanmar Text", size=11, weight="bold")
	fuente_error = CTkFont(family="Ebrima", size=13, weight="bold")

	frame_izquierdo_login = CTkFrame(ventana, fg_color=verde_claro, corner_radius=0)
	frame_contenido_login = CTkFrame(ventana, fg_color=gris_oscuro, corner_radius=0)
	##Creacion del contenido del login
	##ZONA IZQUIERDA
	imagenLogo = CTkImage(dark_image=Image.open(os.path.join(carpeta_imagenes, "huellitasLogo.png")), size=(200,135))
	label_logo = CTkLabel(frame_izquierdo_login, image=imagenLogo, text="")
	imagen_huellitas = CTkImage(dark_image=Image.open(os.path.join(carpeta_imagenes, "huellitas_titulo.png")), size=(250,100))
	label_huellitas = CTkLabel(frame_izquierdo_login, image=imagen_huellitas, text = "")
	label_marca = CTkLabel(frame_izquierdo_login, text="Desarrollado por Ignacio Fernandez", font=fuente_marca)

	frame_izquierdo_login.pack(side=LEFT, fill=Y, ipadx=80)
	label_logo.pack(pady=(80,0))
	label_huellitas.pack()
	label_marca.pack(side=BOTTOM)

	

	def ocultar_widgets_login():
		for widget in frame_contenido_login.winfo_children():
			widget.pack_forget()

	##ZONA DERECHA
	imagenLogin = CTkImage(dark_image=Image.open(os.path.join(carpeta_imagenes, "persona.png")), size=(100,100))
	label_login = CTkLabel(frame_contenido_login, image=imagenLogin, text="", )
	entry_usuario = CTkEntry(frame_contenido_login, fg_color=verde_claro, border_width=0, placeholder_text="Ingrese su usuario", font=fuente_login)
	entry_contraseña = CTkEntry(frame_contenido_login, show="*", fg_color=verde_claro, border_width=0, placeholder_text="Ingrese su contraseña", font=fuente_login)

	label_error = CTkLabel(frame_contenido_login, text="Ingrese los datos correctamente", text_color="red", font=fuente_error)
	label_error2 = CTkLabel(frame_contenido_login, text="Las contraseñas no coinciden", text_color="red", font=fuente_error)
	label_error3 = CTkLabel(frame_contenido_login, text="La contraseña o el usuario no son correctos", text_color="red", font=fuente_error)


	

	def register():
		ocultar_widgets_login()
		def logicaRegistro():
			usuario = entry_usuario.get()
			contraseña = entry_contraseña.get()
			repcontraseña = entry_contraseña2.get()
			if(usuario != "" and contraseña != ""):
				if (contraseña == repcontraseña):
					base_de_datos.crearUsuario(usuario, contraseña)	
					messagebox.showinfo(message="Usuario creado correctamente", title="Huellitas sistema")
					inicio_sesion()
				else:
					label_error2.pack(pady=10)
			else:
				label_error.pack(pady=10)
				
		global label_register, entry_contraseña2, boton_registrar, boton_volver
		if 'modRegister' not in globals():
			global modRegister
			modRegister=True
			label_register = CTkLabel(frame_contenido_login, text="Ingrese los datos para registrarse", font=fuente_login, text_color=gris_claro)
			entry_contraseña2 = CTkEntry(frame_contenido_login, show="*", fg_color=verde_claro, border_width=0, placeholder_text="Ingrese la contraseña nuevamente", font=fuente_login)
			boton_registrar = CTkButton(frame_contenido_login, text="Registrarme", fg_color=verde_oscuro, font=fuente_login, command=logicaRegistro)
			boton_volver = CTkButton(frame_contenido_login, text="Volver", fg_color=verde_oscuro, font=fuente_login, command=inicio_sesion)
		frame_contenido_login.pack(side=RIGHT, fill=Y)
		label_register.pack(padx=74, pady=40)
		entry_usuario.pack(ipady=5, ipadx=55, pady=(0,20))
		entry_usuario.delete(0, END)
		entry_usuario.configure(placeholder_text="Ingrese un usuario")
		entry_contraseña.pack(ipady=5, ipadx=55)
		entry_contraseña.delete(0, END)
		entry_contraseña.configure(placeholder_text="Ingrese una contraseña")
		entry_contraseña2.pack(ipady=5, ipadx=55, pady=20)
		entry_contraseña2.delete(0, END)
		entry_contraseña2.configure(placeholder_text="Ingrese su contraseña nuevamente")
		boton_registrar.pack(pady=20)
		boton_volver.pack()

	boton_register = CTkButton(frame_contenido_login, text="Registrarme", fg_color=verde_oscuro, font=fuente_login, command=register)

	def inicio_sesion():
		ocultar_widgets_login()
		global validacion
		validacion = False

		
		def logicaInicioSesion():
			global validacion
			usuario = entry_usuario.get()
			contraseña = entry_contraseña.get()
			if(usuario != "" and contraseña != ""):
				usuarios = []
				usuarios = base_de_datos.traerUsuarios()
				for us in usuarios:
					if (us[0] == usuario and us[1] == contraseña):
						validacion = True
					if(validacion == True):
						try:
							ventana.after_cancel("all")
							ventana.destroy()
						except Exception as e:
							print(f"Error al cancelar eventos: {e}")
						
						principal.ventana_principal(usuario)
						sys.exit()
						"""
						ventana.destroy()
						principal.ventana_principal(usuario)
						"""
					elif(validacion == False):
						label_error.pack_forget()	
						label_error3.pack(pady=10)
			else:
				label_error3.pack_forget()
				label_error.pack(pady=10)
			

		global boton_is
		if 'modInicioSesion' not in globals():
			global modInicioSesion
			modInicioSesion = True
			boton_is = CTkButton(frame_contenido_login, text="Iniciar sesion", fg_color=verde_oscuro, font=fuente_login, command=logicaInicioSesion)
		frame_contenido_login.pack(side=RIGHT, fill=Y)
		label_login.pack(padx=135, pady=(60,0))
		entry_usuario.pack(pady=20, ipady=5, ipadx=40)
		entry_usuario.delete(0, END)
		entry_usuario.configure(placeholder_text="Ingrese su usuario")
		entry_contraseña.pack(ipady=5, ipadx=40)
		entry_contraseña.delete(0, END)
		entry_contraseña.configure(placeholder_text="Ingrese su contraseña")
		boton_is.pack(pady=(30,15), ipady=2)
		boton_register.pack(ipady=2)

	inicio_sesion()

	ventana.mainloop()

iniciar_sesion()