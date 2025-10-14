import os
import sqlite3
import sys
import shutil

carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, ("imagenes"))

def get_appdata_folder(nombre_app="HuellitasApp"):
    """
    Retorna una carpeta persistente (por usuario) donde guardar datos.
    - En Windows: C:/Users/<usuario>/AppData/Local/HuellitasApp
    - En Linux: /home/<usuario>/.miapp
    - En macOS: /Users/<usuario>/Library/Application Support/MiApp
    """
    base = None
    if sys.platform.startswith("win"):
        base = os.path.join(os.environ["LOCALAPPDATA"], nombre_app)
    elif sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~/Library/Application Support"), nombre_app)
    else:
        base = os.path.join(os.path.expanduser("~"), f".{nombre_app.lower()}")

    os.makedirs(base, exist_ok=True)
    return base




class baseDeDatos():
	def __init__(self, db_name: str = 'negocio.db'):
		# 🔹 NUEVA ruta persistente (correctamente definida primero)
		db_folder_nuevo = get_appdata_folder("MiNegocio")
		db_path_nuevo = os.path.join(db_folder_nuevo, db_name)

		# 🔹 RUTA VIEJA (donde estaba antes en tu proyecto)
		db_folder_viejo = os.path.join(os.path.dirname(__file__), "db_folder")
		db_path_viejo = os.path.join(db_folder_viejo, db_name)
		# 🔁 MIGRACIÓN AUTOMÁTICA (solo la primera vez)
		if os.path.exists(db_path_viejo) and not os.path.exists(db_path_nuevo):
			print("📦 Migrando base de datos a nueva ubicación...")
			shutil.copy2(db_path_viejo, db_path_nuevo)

		self.connection = sqlite3.connect(db_path_nuevo)
		self.cursor = self.connection.cursor()

	def crearTabla(self):
		with self.connection:
			self.connection.execute('''
				CREATE TABLE IF NOT EXISTS"articulos" (
				"id"	INTEGER,
				"nombre"	TEXT NOT NULL,
				"id_categoria"	TEXT,
				"subcategoria" TEXT,
				"id_proveedor"	INTEGER,
				"precio_costo"	INTEGER NOT NULL,
				"precio_venta"	INTEGER NOT NULL,
				"cantidad"	INTEGER NOT NULL,
				"estado" TEXT NOT NULL DEFAULT 'activo',
				"codigo_barras"	TEXT,
				FOREIGN KEY("id_proveedor") REFERENCES "proveedores"("id"),
				FOREIGN KEY("id_categoria") REFERENCES "categorias"("id"),
				PRIMARY KEY("id" AUTOINCREMENT)
				);
			''')
		with self.connection:
			self.connection.execute('''
				CREATE TABLE IF NOT EXISTS "categorias" (
				"id"	TEXT,
				"categoria"	TEXT,
				"estado" TEXT NOT NULL DEFAULT 'activo',
				PRIMARY KEY("id")
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
		with self.connection:
			self.connection.execute('''
				CREATE TABLE IF NOT EXISTS "cuentas" (
					"num"	INTEGER,
					"fecha"	TEXT,
					"proveedor"	INTEGER,
					"saldo"	INTEGER,
					"pagos" INTEGER,
					"pedidos" INTEGER,
					FOREIGN KEY("proveedor") REFERENCES "proveedores"("id"),
					PRIMARY KEY("num" AUTOINCREMENT)
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

	def insertCategoria(self, id_categoria,categoria):
		with self.connection:
			self.cursor.execute("INSERT INTO categorias (id, categoria) VALUES (?,?)",
				(id_categoria,categoria)
			)

	def insertProveedor(self, proveedor):
		with self.connection:
			self.cursor.execute("INSERT INTO proveedores (nombre, telefono) VALUES (?,?)",
				(proveedor.nombre, proveedor.telefono))

	def insertCuenta(self, cuenta):
		with self.connection:
			self.cursor.execute("INSERT INTO cuentas (fecha, proveedor, saldo, pagos, pedidos) VALUES (?,?,?,?,?)",
				(cuenta.fecha, cuenta.proveedor, cuenta.saldo, cuenta.pagos, cuenta.pedidos))

	def listarArticulos(self):
		with self.connection:
			self.cursor.execute("SELECT * FROM articulos WHERE estado == 'activo'")
			return self.cursor.fetchall()

	def listarArticulosInactivos(self):
		with self.connection:
			self.cursor.execute("SELECT * FROM articulos WHERE estado == 'inactivo'")
			return self.cursor.fetchall()

	def listar_art_cod_barras(self, codigo_barras):
		with self.connection:
			self.cursor.execute("SELECT id, nombre, id_categoria, subcategoria, id_proveedor, precio_costo, precio_venta, cantidad FROM articulos WHERE codigo_barras == (?)",
				(codigo_barras,))
			return self.cursor.fetchall()

	def listarPyNArticulos(self):
		with self.connection:
			self.cursor.execute("SELECT id, nombre, precio_venta, cantidad FROM articulos WHERE estado == 'activo'")
			return self.cursor.fetchall()

	def listarPyNArticulosVentas(self):
		with self.connection:
			self.cursor.execute("SELECT id, nombre, precio_venta FROM articulos WHERE estado == 'activo' AND cantidad > 0")
			return self.cursor.fetchall()

	def listarPyNArticulosVentasPorCat(self, categoria):
		with self.connection:
			self.cursor.execute("SELECT id, nombre, precio_venta FROM articulos WHERE estado == 'activo' AND cantidad > 0 AND id_categoria = (?)",
				(categoria,))
			return self.cursor.fetchall()
		
	def listarPyNArticulosInactivos(self):
		with self.connection:
			self.cursor.execute("SELECT id, nombre, precio_venta FROM articulos WHERE estado == 'inactivo'")
			return self.cursor.fetchall()

	def listarCategorias(self):
		with self.connection:
			self.cursor.execute("SELECT * FROM categorias WHERE estado == 'activo'")
			return self.cursor.fetchall()

	def listarCategoriasInactivas(self):
		with self.connection:
			self.cursor.execute("SELECT * FROM categorias WHERE estado == 'inactivo'")
			return self.cursor.fetchall()

	def listarProveedores(self):
		with self.connection:
			self.cursor.execute("SELECT * FROM proveedores WHERE estado == 'activo'")
			return self.cursor.fetchall()

	def listarCuentas(self):
		with self.connection:
			self.cursor.execute("SELECT * FROM cuentas")
			return self.cursor.fetchall()	

	def listarCuentasPorProveedor(self, id_proveedor):
		with self.connection:
			self.cursor.execute("SELECT * FROM cuentas WHERE proveedor == (?)",
				(id_proveedor,))
			return self.cursor.fetchall()	


	def listarProveedoresInactivos(self):
		with self.connection:
			self.cursor.execute("SELECT * FROM proveedores WHERE estado == 'inactivo'")
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

	def actualizarCuenta(self, cuenta, id_cuenta):
		with self.connection:
			self.cursor.execute("UPDATE cuentas SET fecha = ?, proveedor = ?, saldo = ?, pagos = ?, pedidos = ? WHERE num = ?",
				(cuenta.fecha, cuenta.proveedor, cuenta.saldo, cuenta.pagos, cuenta.pedidos, id_cuenta))

	def darDeBajaCategoria(self, id_categoria):
		with self.connection:
			self.cursor.execute("UPDATE categorias SET estado = 'inactivo' WHERE id = ?", (id_categoria,))

	def darDeAltaCategoria(self, id_categoria):
		with self.connection:
			self.cursor.execute("UPDATE categorias SET estado = 'activo' WHERE id = ?", (id_categoria,))		

	def darDeBajaProveedor(self, id_proveedor):
		with self.connection:
			self.cursor.execute("UPDATE proveedores SET estado = 'inactivo' WHERE id = ?", (id_proveedor,))

	def darDeAltaProveedor(self, id_proveedor):
		with self.connection:
			self.cursor.execute("UPDATE proveedores SET estado = 'activo' WHERE id = ?", (id_proveedor,))

	def darDeBajaArticulo(self, id_articulo):
		with self.connection:
			self.cursor.execute("UPDATE articulos SET estado = 'inactivo' WHERE id = ?", (id_articulo,))

	def darDeAltaArticulo(self, id_articulo):
		with self.connection:
			self.cursor.execute("UPDATE articulos SET estado = 'activo' WHERE id = ?", (id_articulo,))

	def eliminarCuenta(self, id_cuenta):
		with self.connection:
			self.cursor.execute("DELETE FROM cuentas WHERE num = ?",
				(id_cuenta,))

	def actualizarCantidadArt(self, nombre_articulo, cantidad_nueva):
		with self.connection:
			self.cursor.execute("UPDATE articulos SET cantidad = ? WHERE nombre = ?",
				(cantidad_nueva, nombre_articulo,))

	def traerCantidadVieja(self, nombre_articulo):
		with self.connection:
			self.cursor.execute("SELECT cantidad FROM articulos WHERE nombre = ?",
				(nombre_articulo,))
			return self.cursor.fetchall()
	