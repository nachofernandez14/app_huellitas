import pandas as pd
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import os

# === CONFIGURACIÓN ===
input_folder = r"C:/Users/elian/OneDrive/Desktop/codigos_barras"     # carpeta donde están las imágenes
output_pdf = "codigos_etiquetas.pdf"

# Tamaño de cada etiqueta
label_width = 9 * cm
label_height = 4 * cm

# Márgenes
margin_x = 0.5 * cm
margin_y = 0.5 * cm

# Espaciado entre etiquetas
spacing_x = 0.5 * cm
spacing_y = 0.5 * cm

# Cálculo de cuántas entran por página A4
page_width, page_height = A4
cols = int((page_width - 2 * margin_x + spacing_x) // (label_width + spacing_x))
rows = int((page_height - 2 * margin_y + spacing_y) // (label_height + spacing_y))

# Crear PDF
c = canvas.Canvas(output_pdf, pagesize=A4)

x_positions = [margin_x + i * (label_width + spacing_x) for i in range(cols)]
y_positions = [page_height - margin_y - (i + 1) * label_height - i * spacing_y for i in range(rows)]

# Iterar imágenes
images = [f for f in sorted(os.listdir(input_folder)) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
i = 0

for filename in images:
    path = os.path.join(input_folder, filename)
    name = os.path.basename(filename)
    for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]:
        if name.endswith(ext):
            name = name[: -len(ext)]
    name = name.strip() 

    # Calcular posición
    col = i % cols
    row = (i // cols) % rows
    x = x_positions[col]
    y = y_positions[row]

    # Dibujar borde opcional
    c.rect(x, y, label_width, label_height)

    # Dibujar nombre
    c.setFont("Helvetica", 10)
    c.drawCentredString(x + label_width / 2, y + label_height - 12, name)

    # Cargar imagen y escalar a ancho disponible
    try:
        with Image.open(path) as img:
            img_width, img_height = img.size
            aspect = img_width / img_height

            # Espacio disponible debajo del texto
            available_width = label_width - 0.5 * cm
            available_height = label_height - 1.5 * cm

            if aspect > 1:
                new_width = min(available_width, available_height * aspect)
                new_height = new_width / aspect
            else:
                new_height = min(available_height, available_width / aspect)
                new_width = new_height * aspect

            img_x = x + (label_width - new_width) / 2
            img_y = y + 0.5 * cm
            c.drawImage(path, img_x, img_y, width=new_width, height=new_height, preserveAspectRatio=True)
    except Exception as e:
        print(f"Error con {filename}: {e}")

    i += 1

    # Nueva página si se llena la actual
    if i % (cols * rows) == 0 and i < len(images):
        c.showPage()

# Guardar PDF
c.save()
print(f"PDF creado: {output_pdf}")
""" 
df = pd.read_excel('productos_huellitas_cod.xlsx')
df.columns = df.columns.str.lower()
print(df)
conn = sqlite3.connect('db_folder/negocio.db')
df.to_sql('articulos', conn, if_exists='append', index=False)
conn.close()
print("Base de datos actualizada")
"""
