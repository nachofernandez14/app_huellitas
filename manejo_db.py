import os
import sqlite3



carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, ("imagenes"))


class baseDeDatos():
	def __init__(self,db_folder:str = 'db_folder',db_name : str= 'negocio.db'):

		if not os.path.exists(db_folder):
			os.makedirs(db_folder)

		db_path = os.path.join(db_folder, db_name)
		self.connection = sqlite3.connect(db_path)
		self.cursor = self.connection.cursor()

	def crearTabla(self):
		with self.connection:
			self.connection.execute('''
				CREATE TABLE IF NOT EXISTS"articulos" (
				"id"	INTEGER,
				"nombre"	TEXT NOT NULL,
				"id_categoria"	INTEGER,
				"id_proveedor"	INTEGER,
				"precio_costo"	INTEGER NOT NULL,
				"precio_venta"	INTEGER NOT NULL,
				"cantidad"	INTEGER NOT NULL,
				"estado" TEXT NOT NULL DEFAULT 'activo',
				FOREIGN KEY("id_proveedor") REFERENCES "proveedores"("id"),
				FOREIGN KEY("id_categoria") REFERENCES "categorias"("id"),
				PRIMARY KEY("id" AUTOINCREMENT)
				);
			''')
		with self.connection:
			self.connection.execute('''
				CREATE TABLE IF NOT EXISTS "categorias" (
				"id"	INTEGER,
				"categoria"	TEXT,
				"estado" TEXT NOT NULL DEFAULT 'activo',
				PRIMARY KEY("id" AUTOINCREMENT)
				);
			''')
		with self.connection:
			self.connection.execute('''
				CREATE TABLE IF NOT EXISTS "proveedores" (
				"id"	INTEGER,
				"nombre"	TEXT,
				"telefono"	INTEGER,
				"estado" TEXT NOT NULL DEFAULT 'activo',
				PRIMARY KEY("id" AUTOINCREMENT)
				);
			''')

		with self.connection:
			self.connection.execute('''
				CREATE TABLE IF NOT EXISTS "usuarios" (
					"id" INTEGER,
					"usuario" TEXT NOT NULL,
					"contraseña" TEXT NOT NULL,
					PRIMARY KEY("id" AUTOINCREMENT)
					);
			''')

	def crearUsuario(self, usuario, contraseña):
		with self.connection:
			self.cursor.execute('INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)', (usuario, contraseña,))

	def traerUsuarios(self):
		with self.connection:
			self.cursor.execute("SELECT usuario, contraseña FROM usuarios")
			return self.cursor.fetchall()

	def insertArticulo(self, articulo):
		with self.connection:
			self.cursor.execute("INSERT INTO articulos (nombre, id_categoria, id_proveedor, precio_costo, precio_venta, cantidad) VALUES (?, ?, ?, ?, ?, ?)",
			(articulo.nombre, articulo.id_categoria, articulo.id_proveedor, articulo.precio_costo, articulo.precio_venta, articulo.cantidad)
			)

	def insertCategoria(self, categoria):
		with self.connection:
			self.cursor.execute("INSERT INTO categorias (categoria) VALUES (?)",
				(categoria,)
			)

	def insertProveedor(self, proveedor):
		with self.connection:
			self.cursor.execute("INSERT INTO proveedores (nombre, telefono) VALUES (?,?)",
				(proveedor.nombre, proveedor.telefono))

	def listarArticulos(self):
		with self.connection:
			self.cursor.execute("SELECT * FROM articulos WHERE estado == 'activo'")
			return self.cursor.fetchall()

	def listarPyNArticulos(self):
		with self.connection:
			self.cursor.execute("SELECT id, nombre, precio_venta FROM articulos WHERE estado == 'activo'")
			return self.cursor.fetchall()
		
	def listarCategorias(self):
		with self.connection:
			self.cursor.execute("SELECT * FROM categorias WHERE estado == 'activo'")
			return self.cursor.fetchall()

	def listarProveedores(self):
		with self.connection:
			self.cursor.execute("SELECT * FROM proveedores WHERE estado == 'activo'")
			return self.cursor.fetchall()

	def actualizarArticulo(self, articulo, id_articulo):
		with self.connection:
			self.cursor.execute("UPDATE articulos SET nombre = ?, id_categoria = ?, id_proveedor = ?, precio_costo = ?, precio_venta = ?, cantidad = ? WHERE id = ?",
				(articulo.nombre, articulo.id_categoria, articulo.id_proveedor, articulo.precio_costo, articulo.precio_venta, articulo.cantidad, id_articulo))

	def actualizarCategoria(self, categoria, id_categoria):
		with self.connection:
			self.cursor.execute("UPDATE categorias SET categoria = ? WHERE id = ?",
				(categoria, id_categoria))

	def actualizarProveedor(self, proveedor, id_proveedor):
		with self.connection:
			self.cursor.execute("UPDATE proveedores SET nombre = ?, telefono = ? WHERE id = ?",
				(proveedor.nombre, proveedor.telefono, id_proveedor))

	def darDeBajaCategoria(self, id_categoria):
		with self.connection:
			self.cursor.execute("UPDATE categorias SET estado = 'innactivo' WHERE id = ?", (id_categoria,))

	def darDeBajaProveedor(self, id_proveedor):
		with self.connection:
			self.cursor.execute("UPDATE proveedores SET estado = 'innactivo' WHERE id = ?", (id_proveedor,))

	def darDeBajaArticulo(self, id_articulo):
		with self.connection:
			self.cursor.execute("UPDATE articulos SET estado = 'innactivo' WHERE id = ?", (id_articulo,))
	