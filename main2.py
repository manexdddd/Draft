import tkinter as tk
from tkinter import ttk
from bson import ObjectId
import customtkinter
import openpyxl
import os
from tkinter import filedialog, messagebox
import pandas as pd
from pymongo.mongo_client import MongoClient 
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.server_api import ServerApi
from PIL import Image, ImageTk 

import os
import openpyxl
import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from tkinter import filedialog, messagebox

import pywinstyles

def load_data():
    path = filedialog.askopenfilename()
    if path.endswith('.xlsx'):
        if not os.path.exists(path):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(["No", "MENOR DE  30", "CAMPEON", "POSICION", "PIERNA HABIL", "BUEN FICHAJE", "% SI", "% NO"])  # Headers
            workbook.save(path)

        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        list_values = list(sheet.values)

        # Convert to DataFrame for MongoDB insertion
        df = pd.DataFrame(list_values[1:], columns=list_values[0])

        # Calcular %SI basado en "Buen Fichaje"
        for index in range(len(df)):
                # Obtener filas por encima de la actual
                above_rows = df.loc[:index - 1]  # Cambiar para no incluir la fila actual

                # Contadores para las columnas deseadas
                contador_menor_30 = 0
                contador_campeon = 0
                contador_posicion = 0
                contador_pierna_habil = 0

                # Total de "BUEN FICHAJE" == "SI" en las filas anteriores
                total_buen_fichaje = above_rows["BUEN FICHAJE"].value_counts().get("SI", 0)

                # Contar coincidencias
                for above_index in range(len(above_rows)):
                    if df.loc[above_index, "BUEN FICHAJE"] == "SI":
                        # Comparar valores de las celdas deseadas
                        if df.loc[above_index, "MENOR DE 30"] == df.loc[index, "MENOR DE 30"]:
                            contador_menor_30 += 1
                        if df.loc[above_index, "CAMPEON"] == df.loc[index, "CAMPEON"]:
                            contador_campeon += 1
                        if df.loc[above_index, "POSICION"] == df.loc[index, "POSICION"]:
                            contador_posicion += 1
                        if df.loc[above_index, "PIERNA HABIL"] == df.loc[index, "PIERNA HABIL"]:
                            contador_pierna_habil += 1

                # Calcular %SI
                    # Calcular el promedio de coincidencias
                    promedio_menor_30 = contador_menor_30 / total_buen_fichaje
                    promedio_campeon = contador_campeon / total_buen_fichaje
                    promedio_posicion = contador_posicion / total_buen_fichaje
                    promedio_pierna_habil = contador_pierna_habil / total_buen_fichaje

                    # Multiplicando todos los promedios
                    percentage_si2 = (promedio_menor_30) * (promedio_campeon) * (promedio_posicion) * (promedio_pierna_habil)

                    # Calcular el porcentaje general
                    percentage_si = ((total_buen_fichaje / len(above_rows)) * percentage_si2) * 100
                    percentage_si = format(percentage_si, '.5f')
                    '''
                    print(f"Fila {index}: Total 'BUEN FICHAJE' (SI) hasta ahora: {total_buen_fichaje}, "
                          f"Contador Menor de 30: {contador_menor_30}, "
                          f"Contador Campeón: {contador_campeon}, "
                          f"campeon {promedio_campeon}",f"promedio Menor de 30 {promedio_menor_30}"
                           f"promedio pierna habil {promedio_pierna_habil}",f"promedio posicion {promedio_posicion}"
                           f"promedio pierna habil {promedio_pierna_habil}",f"promedio posicion {promedio_posicion}"
                          )
                    '''
                    
                    df.loc[index, "% SI"] = percentage_si
 
        # Calcular %NO basado en "Buen Fichaje"
        for index in range(len(df)):
                # Obtener filas por encima de la actual
                above_rows = df.loc[:index - 1]  # Cambiar para no incluir la fila actual

                # Contadores para las columnas deseadas
                contador_menor_30_no = 0
                contador_campeon_no = 0
                contador_posicion_no = 0
                contador_pierna_habil_no = 0

                # Total de "BUEN FICHAJE" == "NO" en las filas anteriores
                total_buen_fichaje_no = above_rows["BUEN FICHAJE"].value_counts().get("NO", 0)

                # Contar coincidencias
                for above_index in range(len(above_rows)):
                    if df.loc[above_index, "BUEN FICHAJE"] == "NO":
                        # Comparar valores de las celdas deseadas
                        if df.loc[above_index, "MENOR DE 30"] == df.loc[index, "MENOR DE 30"]:
                            contador_menor_30_no += 1
                        if df.loc[above_index, "CAMPEON"] == df.loc[index, "CAMPEON"]:
                            contador_campeon_no += 1
                        if df.loc[above_index, "POSICION"] == df.loc[index, "POSICION"]:
                            contador_posicion_no += 1
                        if df.loc[above_index, "PIERNA HABIL"] == df.loc[index, "PIERNA HABIL"]:
                            contador_pierna_habil_no += 1

                # Calcular %NO
                if total_buen_fichaje_no > 0:
                    # Calcular el promedio de coincidencias
                    promedio_menor_30_no = contador_menor_30_no / total_buen_fichaje_no
                    promedio_campeon_no = contador_campeon_no / total_buen_fichaje_no
                    promedio_posicion_no = contador_posicion_no / total_buen_fichaje_no
                    promedio_pierna_habil_no = contador_pierna_habil_no / total_buen_fichaje_no

                    # Multiplicando todos los promedios
                    percentage_no2 = (promedio_menor_30_no) * (promedio_campeon_no) * (promedio_posicion_no) * (promedio_pierna_habil_no)

                    # Calcular el porcentaje general
                    percentage_no = ((total_buen_fichaje_no / len(above_rows) * percentage_no2 )* 100)
                    percentage_no = format(percentage_no, '.5f')
                    '''
                    print(f"Fila {index}: Total 'BUEN FICHAJE' (NO) hasta ahora: {total_buen_fichaje_no}, "
                          f"Contador Menor de 30: {contador_menor_30_no}, "
                          f"Contador Campeón: {contador_campeon_no}, "
                          f"campeon {promedio_campeon_no}",f"promedio Menor de 30 {promedio_menor_30}"
                           f"promedio pierna habil {promedio_pierna_habil_no}",f"promedio posicion {promedio_posicion}"
                           f"promedio campeon {promedio_campeon_no}",f" opereacion 1 {percentage_no2}"
                          )
                    '''
                    # Ajustar el %NO en el DataFrame
                    df.loc[index, "% NO"] = percentage_no
                else:
                    df.loc[index, "% NO"] = 0  # Si no hay "BUEN FICHAJE", se establece a 0

        # Conexión a MongoDB
        url = "mongodb+srv://manexddd33:psw@cluster0.6drbl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(url, server_api=ServerApi('1'))

        try:
            client.admin.command('ping')
            print("MongoDB connection established successfully.")

            # Insertar DataFrame en MongoDB
            db = client.draft
            collection = db.fichajes

            # Convertir a dict y insertar en MongoDB
            collection.insert_many(df.to_dict('records'))

            # Recuperar datos de MongoDB
            cursor = collection.find()
            df_mongo = pd.DataFrame(list(cursor))

            # Eliminar la columna '_id' si existe
            if '_id' in df_mongo.columns:
                df_mongo = df_mongo.drop(columns=['_id'])

            treeview.delete(*treeview.get_children())
            # Configurar columnas del Treeview
            cols = df_mongo.columns.tolist()
            treeview["columns"] = cols

            # Cambiar la fuente del encabezado para reducir su altura
            style.configure("Treeview.Heading", font=("Helvetica", 10))  # Cambia el tamaño de la fuente según tus necesidades

            # Ajustar el ancho de cada columna a 40 píxeles
            for col_name in cols:
                treeview.heading(col_name, text=col_name)
                treeview.column(col_name, width=40, anchor="center")  # Ajustar el ancho a 40 píxeles

            for _, row in df_mongo.iterrows():
                treeview.insert("", "end", values=list(row))
            
            messagebox.showinfo("Datos", "Datos Cargados Correctamente a la Base de datos")
        except Exception as e:
            print(f"Error occurred while connecting to MongoDB: {e}")
        finally:
            client.close()
    else:
        messagebox.showerror("Error", "El archivo seleccionado no es un archivo de Excel válido.")

def load_mongo():
    url = "mongodb+srv://manexddd33:psw@cluster0.6drbl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(url, server_api=ServerApi('1'))
    
    try:
        client.admin.command('ping')
        print("MongoDB connection established successfully.")
        
        # Insert DataFrame into MongoDB
        db = client.draft
        collection = db.fichajes
        
        # Retrieve data from MongoDB
        cursor = collection.find()
        df_mongo = pd.DataFrame(list(cursor))
        
        # Eliminar columna '_id' si existe
        if '_id' in df_mongo.columns:
            df_mongo = df_mongo.drop(columns=['_id'])
        
        # Limpiar el Treeview
        treeview.delete(*treeview.get_children())
        
        # Configurar columnas del Treeview
        cols = df_mongo.columns.tolist()
        
        if df_mongo.empty:  # Verificar si no hay datos
             #treeFrame.grid_forget()
             #empty_label.pack()   
            messagebox.showerror("Error", "Base de Datos de MONGODB Vacia ")
           
        else:
            # empty_label.grid_forget()
            #treeFrame.grid(row=0, column=1, pady=10)
            treeview["columns"] = cols
            
            # Cambiar la fuente del encabezado para reducir su altura
            style.configure("Treeview.Heading", font=("Helvetica", 10))  # Cambia el tamaño de la fuente según tus necesidades

            # Ajustar el ancho de cada columna a 40 píxeles
            for col_name in cols:
                treeview.heading(col_name, text=col_name)
                treeview.column(col_name, width=40, anchor="center")  # Ajustar el ancho a 40 píxeles
            
            # Insertar las filas del DataFrame en el Treeview
            for index, row in df_mongo.iterrows():
                treeview.insert('', tk.END, values=row.tolist())
    
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Fallo al Cargar los Datos de MONGODB")


    

def insert_row():
    if not treeview.get_children():  # Si no hay hijos en el Treeview
        messagebox.showerror("Error", "No se pueden agregar registros porque no hay datos Históricos.")
        return

    url = "mongodb+srv://manexddd33:psw@cluster0.6drbl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(url, server_api=ServerApi('1'))

    # Obtener valores del formulario
    numero =0
    menor_30 =""
    campeon = ""
    posicion =""
    pierna_habil = ""
    
    numero = get_next_numero()
    menor_30 = menor_30_combobox.get()
    campeon = campeon_combobox.get()
    posicion = posicion_combobox.get()
    pierna_habil = pierna_habil_combobox.get()

    try:
        # Probar conexión a MongoDB
        client.admin.command('ping')
        print("Conexión a MongoDB establecida con éxito.")

        # Seleccionar base de datos y colección
        db = client.draft
        collection = db.fichajes
        
        # Recuperar datos actuales de la colección
        cursor = collection.find()
        df_mongo = pd.DataFrame(list(cursor))

        # Eliminar la columna '_id' si existe
        if '_id' in df_mongo.columns:
            df_mongo = df_mongo.drop(columns=['_id'])

        # Inicializar contadores para cada variable
        contador_menor_30_si = 0
        contador_menor_30_no = 0
        contador_campeon_si = 0
        contador_campeon_no = 0
        contador_posicion_si = 0
        contador_posicion_no = 0
        contador_pierna_habil_si = 0
        contador_pierna_habil_no = 0
        
        # Contar BUEN FICHAJE según el contenido de las otras columnas
        for index, row in df_mongo.iterrows():
            # Contar según 'BUEN FICHAJE'
            if row["BUEN FICHAJE"] == "SI":
                contador_menor_30_si += 1 if row["MENOR DE 30"] == menor_30 else 0
                contador_campeon_si += 1 if row["CAMPEON"] == campeon else 0
                contador_posicion_si += 1 if row["POSICION"] == posicion else 0
                contador_pierna_habil_si += 1 if row["PIERNA HABIL"] == pierna_habil else 0

            elif row["BUEN FICHAJE"] == "NO":
                contador_menor_30_no += 1 if row["MENOR DE 30"] == menor_30 else 0
                contador_campeon_no += 1 if row["CAMPEON"] == campeon else 0
                contador_posicion_no += 1 if row["POSICION"] == posicion else 0
                contador_pierna_habil_no += 1 if row["PIERNA HABIL"] == pierna_habil else 0

          # Variables para conteos 
        total_si = df_mongo[df_mongo["BUEN FICHAJE"] == "SI"].shape[0]
        total_no = df_mongo[df_mongo["BUEN FICHAJE"] == "NO"].shape[0]
        total_filas = df_mongo.shape[0]

        calculo1= (contador_menor_30_si/total_si)*(contador_campeon_si/total_si)*(contador_posicion_si/total_si)*(contador_pierna_habil_si/total_si)
        calculo2 = calculo1 * (total_si/total_filas)

        calculo3= (contador_menor_30_no/total_no)*(contador_campeon_no/total_no)*(contador_posicion_no/total_no)*(contador_pierna_habil_no/total_no)
        calculo4 = calculo3 * (total_no/total_filas)
        # Asegurarse de que haya datos en la colección antes de calcular probabilidades
        if total_filas > 0:
            # Calcular probabilidades de 'SI' y 'NO'
            porcentaje_si = calculo2 *100
            porcentaje_no = calculo4 *100
        else:
            porcentaje_si = 0
            porcentaje_no = 0

        # Formatear porcentajes a 5 decimales
        porcentaje_si = format(porcentaje_si, '.5f')
        porcentaje_no = format(porcentaje_no, '.5f')

        # Asignar BUEN FICHAJE según la probabilidad más alta
        buen_fichaje = "SI" if float(porcentaje_si) >= float(porcentaje_no) else "NO"

        print(f"Fila {index}: Total 'BUEN FICHAJE' (NO) hasta ahora: {total_no}, "
                          f"Contador Menor de 30: {contador_menor_30_no}, "
                          f"Contador Campeón: {contador_campeon_no}, "
                           f"contador pierna habil {contador_pierna_habil_no}",f"contador  {contador_posicion_no}"
                          f"calculo3 {calculo3}",f"calculo4 {calculo4}"
                           f"total no {total_no}",f"total si {total_si}"
                          )

        # Crear documento para insertar en MongoDB
        document = {
            "No": numero,
            "MENOR DE 30": menor_30,
            "CAMPEON": campeon,
            "POSICION": posicion,
            "PIERNA HABIL": pierna_habil,
            "BUEN FICHAJE": buen_fichaje,
            "% SI": porcentaje_si,
            "% NO": porcentaje_no
        }

  # Limpiar el sub_treeview antes de insertar nuevos datos
        sub_treeview.delete(*sub_treeview.get_children())

        # Insertar documento en MongoDB
        collection.insert_one(document)

        # Insertar en el Treeview
        row_values = [numero, menor_30, campeon, posicion, pierna_habil, buen_fichaje, porcentaje_si, porcentaje_no]
        treeview.insert('', tk.END, values=row_values)

        # Insertar en el sub Treeview
        row_values2 = [numero, porcentaje_si, porcentaje_no, buen_fichaje]
        sub_treeview.insert('', tk.END, values=row_values2)

        # Limpiar entradas del formulario
        clear_entries()

    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"Fallo al ingresar los datos en MongoDB: {str(e)}")






ObjectId

def get_next_numero():
    try:
        # Obtener todos los ítems del Treeview
        items = treeview.get_children()

        # Si no hay elementos en el Treeview, el número será 1
        if not items:
            return 1

        # Recorrer los elementos y obtener el valor de la columna 'No'
        numeros = []
        for item in items:
            # Obtener los valores de la fila
            row_values = treeview.item(item, 'values')
            if row_values:  # Asegurarse de que haya valores
                # El campo 'No' debería ser el primero, lo convertimos a entero y lo añadimos a la lista
                numeros.append(int(row_values[0]))

        # Obtener el número máximo y devolver el siguiente
        max_numero = max(numeros)
        return max_numero + 1

    except Exception as e:
        print(f"Error al obtener el próximo número del Treeview: {e}")
        messagebox.showerror("Error", f"Error al obtener el próximo número del Treeview: {e}")
        return 1

    
def clear_entries():
    name_entry.delete(0, "end")
    name_entry.insert(0, "Numero")
    menor_30_combobox.set(combo_list[0])
    campeon_combobox.set(combo_list[0])
    posicion_combobox.set(posiciones[0])
    pierna_habil_combobox.set(piernas[0])

def set_background(root, image_path):
    # Cargar la imagen
    image = Image.open(image_path)
    # Redimensionar la imagen para que se ajuste al tamaño de la ventana
    image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_image = ImageTk.PhotoImage(image)

    # Crear un Label para contener la imagen de fondo
    bg_label = customtkinter.CTkLabel(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  # Ocupar todo el espacio de la ventana
    bg_label.image = bg_image  # Necesario para mantener una referencia de la imagen


# Crear la ventana principal de la aplicación
root = customtkinter.CTk()

# Establecer el fondo
set_background(root, "wall3.jpg")

root.title("Hans Flick")
# Make the window full screen
root.attributes("-fullscreen", True)

style = ttk.Style(root)
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")
# Crear un Frame para organizar las imágenes y el contenido con estilo de marcador de fútbol
image_frame = customtkinter.CTkFrame(root, fg_color="#1E1E1E")  # Fondo oscuro
image_frame.pack(pady=20, padx=20)  # Espaciado alrededor del Frame

# Crear un sub-frame para los nombres de los equipos
team_frame = customtkinter.CTkFrame(image_frame, fg_color="#1E1E1E")
team_frame.pack(side="left", padx=20)  # Colocar a la izquierda del logo

# Agregar un Label para los jugadores del equipo A en el lado izquierdo
team_a_label = customtkinter.CTkLabel(
    team_frame,
    text="Alineacion:\nM. Vergara,I. Alvarez, Dua lipa, S. Pineda,\nA. Medina, Messi",  # Cambia esto a los nombres reales
    text_color="#FFFFFF",
    font=("Arial", 12))
team_a_label.pack(side="left", padx=(10, 5))

# Cargar la imagen del club
club_image_path = "club.png"  # Cambia esto a la ruta correcta de tu imagen
club_image = Image.open(club_image_path)
club_image = club_image.resize((88, 90))  # Redimensionar la imagen
club_bg_image = ImageTk.PhotoImage(club_image)

# Crear un Frame para el logo del club y el marcador
middle_frame = customtkinter.CTkFrame(image_frame, fg_color="#1E1E1E")
middle_frame.pack(side="left", padx=20)  # Colocar en el centro

# Crear un Label para contener la imagen del club
club_image_label = customtkinter.CTkLabel(middle_frame, image=club_bg_image, text="")
club_image_label.pack(side="left", padx=(10, 5))  # Colocar la imagen arriba

# Agregar un Label para el nombre del club
club_name_label = customtkinter.CTkLabel(
    middle_frame,
    text="Real Zinapeuaro FC",  # Cambia esto al nombre del club
    text_color="#FFFFFF",
    font=("Arial", 14, "bold")
)
club_name_label.pack(side="left", padx=(5, 20))  # Colocar el texto debajo de la imagen

# Crear un Label para el marcador
score_label = customtkinter.CTkLabel(
    middle_frame,
    text="100 - 0",  # Marcador inicial
    text_color="#FFCC00",
    font=("Arial", 24, "bold")
)
score_label.pack(side="left", padx=(10, 10))  # Colocar el marcador debajo del nombre del club



# Agregar un Label que diga "Predicción de Fichajes"
prediction_label = customtkinter.CTkLabel(
    middle_frame,
    text="Inteligencia Artificial",
    text_color="#FFFFFF",
    font=("Arial", 14, "bold")
)
prediction_label.pack(side="left", padx=(5, 10))  # Colocar el texto debajo de la imagen

# Cargar la imagen de predicción de fichajes
prediction_image_path = "ia.png"  # Cambia esto a la ruta correcta de la imagen de predicción
prediction_image = Image.open(prediction_image_path)
prediction_image = prediction_image.resize((91, 84))  # Ajustar tamaño de la imagen
prediction_bg_image = ImageTk.PhotoImage(prediction_image)

# Crear un Label para contener la imagen de "Predicción de Fichajes"
prediction_image_label = customtkinter.CTkLabel(middle_frame, image=prediction_bg_image, text="")
prediction_image_label.pack(side="left", padx=(20, 0))  # Colocar la imagen debajo del marcador



# Crear un sub-frame para los nombres de los jugadores del equipo B
team_b_frame = customtkinter.CTkFrame(image_frame, fg_color="#1E1E1E")
team_b_frame.pack(side="left", padx=20)  # Colocar a la derecha del logo

# Agregar un Label para los jugadores del equipo B en el lado derecho
team_b_label = customtkinter.CTkLabel(
    team_b_frame,
    text="Alineacion:\n Alejandro G.,Beyonce,Ochoa, K. Mbappé,\n Deep Learning,Examen U3 CMMI",  # Cambia esto a los nombres reales
    text_color="#FFFFFF",
    font=("Arial", 12))
team_b_label.pack(side="left", padx=(10, 5))

# Mantener las referencias a las imágenes
club_image_label.image = club_bg_image
prediction_image_label.image = prediction_bg_image


combo_list = ["SI", "NO"]
posiciones = ["DELANTERO", "MEDIO", "DEFENSA", "PORTERO"]
piernas = ["DERECHA", "IZQUIERDA"]

frame = ttk.Frame(root)
frame.pack()






widgets_frame = ttk.LabelFrame(frame, text="INSERTAR CAMPOS")
widgets_frame.grid(row=0, column=0, padx=50, pady=15, sticky="nsew")
widgets_frame.grid_columnconfigure(1, weight=100)
widgets_frame.grid_columnconfigure(1, weight=1)
widgets_frame.update_idletasks()  # 
name_entry = ttk.Entry(widgets_frame)



menor_30_label = ttk.Label(widgets_frame, text="¿MENOR DE 30 AÑOS?")
menor_30_label.grid(row=1, column=0, padx=8, pady=8, sticky="ew")
menor_30_combobox = ttk.Combobox(widgets_frame, values=combo_list)
menor_30_combobox.current(0)
menor_30_combobox.grid(row=1, column=1, padx=8, pady=8, sticky="ew")


campeon_label = ttk.Label(widgets_frame, text="¿ES CAMPEON?")
campeon_label.grid(row=2, column=0, padx=8, pady=8, sticky="ew")
campeon_combobox = ttk.Combobox(widgets_frame, values=combo_list)
campeon_combobox.current(0)
campeon_combobox.grid(row=2, column=1, padx=8, pady=8, sticky="ew")

posicion_label = ttk.Label(widgets_frame, text="POSICION")
posicion_label.grid(row=3, column=0, padx=8, pady=8, sticky="ew")
posicion_combobox = ttk.Combobox(widgets_frame, values=posiciones)
posicion_combobox.current(0)
posicion_combobox.grid(row=3, column=1, padx=8, pady=8, sticky="ew")

pierna_habil_label = ttk.Label(widgets_frame, text="PIERNA HABIL")
pierna_habil_label.grid(row=4, column=0, padx=8, pady=8, sticky="ew")
pierna_habil_combobox = ttk.Combobox(widgets_frame, values=piernas)
pierna_habil_combobox.current(0)
pierna_habil_combobox.grid(row=4, column=1, padx=8, pady=8, sticky="ew")

# Cargar la imagen para el ícono (redimensiona si es necesario)
icon_image = Image.open("plus.png")  # Ruta de la imagen

icon_image = icon_image.resize((20, 20))  # Redimensionar el ícono si es necesario
icon_photo = ImageTk.PhotoImage(icon_image)
compound="left",  # Posición del ícono, aquí está a la izquierda del texto

# Cargar la imagen para el ícono (redimensiona si es necesario)
icon_image2 = Image.open("no.png")  # Ruta de la imagen

icon_image2 = icon_image2.resize((20, 20))  # Redimensionar el ícono si es necesario
icon_photo2 = ImageTk.PhotoImage(icon_image2)
compound="left",  # Posición del ícono, aquí está a la izquierda del texto

# Cargar la imagen para el ícono (redimensiona si es necesario)
icon_image3 = Image.open("ape.png")  # Ruta de la imagen

icon_image3 = icon_image3.resize((20, 20))  # Redimensionar el ícono si es necesario
icon_photo3 = ImageTk.PhotoImage(icon_image3)
compound="left",  # Posición del ícono, aquí está a la izquierda del texto

# Cargar la imagen para el ícono (redimensiona si es necesario)
icon_image4 = Image.open("download.png")  # Ruta de la imagen

icon_image4 = icon_image4.resize((20, 20))  # Redimensionar el ícono si es necesario
icon_photo4 = ImageTk.PhotoImage(icon_image4)
compound="left",  # Posición del ícono, aquí está a la izquierda del texto

button_insert = customtkinter.CTkButton(
    widgets_frame,
    image=icon_photo,  # Agregar el ícono
    text="Insertar", 
    fg_color="#e551a4",  # Color de fondo del botón
    hover_color="#E3E3E3",  # Color al pasar el mouse sobre el botón
    text_color="#000000",  # Color del texto del botó
    font=("Arial", 16, "bold"),  # Estilo y tamaño de la fuente
    command=insert_row  # Comando para salir de la aplicación
)
button_insert.grid(row=5, column=1, padx=8, pady=5, sticky="ew")



button_uploadex = customtkinter.CTkButton(
    widgets_frame,
    image=icon_photo4,  # Agregar el ícono
    text="Subir Excel", 
    fg_color="#3dbeeb",  # Color de fondo del botón
    hover_color="#E3E3E3",  # Color al pasar el mouse sobre el botón
    text_color="#000000",  # Color del texto del botó
    font=("Arial", 16, "bold"),  # Estilo y tamaño de la fuente
    command=load_data # Comando para salir de la aplicación
)
button_uploadex.grid(row=7, column=1, padx=8, pady=0, sticky="ew")

button_upload = customtkinter.CTkButton(
    widgets_frame,
    image=icon_photo3,  # Agregar el ícono
    text="Cargar DB", 
    fg_color="#74E39A",  # Color de fondo del botón
    hover_color="#E3E3E3",  # Color al pasar el mouse sobre el botón
    text_color="#000000",  # Color del texto del botó
    font=("Arial", 16, "bold"),  # Estilo y tamaño de la fuente
    command=load_mongo # Comando para salir de la aplicación
)
button_upload.grid(row=8, column=1, padx=8, pady=0, sticky="ew")

# Cargar la imagen de predicción de fichajes
inf_image_path = "dua.jpg"  # Cambia esto a la ruta correcta de la imagen de predicción
inf_image = Image.open(inf_image_path)
inf_image = inf_image.resize((91, 84))  # Ajustar tamaño de la imagen
inf_bg_image = ImageTk.PhotoImage(inf_image)
# Crear un Label para contener la imagen de "Predicción de Fichajes"
inf_image_label = customtkinter.CTkLabel(widgets_frame, image=inf_bg_image, text="")
inf_image_label.grid(row=5, column=0, padx=0, pady=5, sticky="ew")

# Cargar la imagen de predicción de fichajes
inf_image_path = "messi.jpg"  # Cambia esto a la ruta correcta de la imagen de predicción
inf_image = Image.open(inf_image_path)
inf_image = inf_image.resize((91, 84))  # Ajustar tamaño de la imagen
inf_bg_image = ImageTk.PhotoImage(inf_image)
# Crear un Label para contener la imagen de "Predicción de Fichajes"
inf_image_label = customtkinter.CTkLabel(widgets_frame, image=inf_bg_image, text="")
inf_image_label.grid(row=8, column=0, padx=0, pady=0, sticky="ew")

# Cambia estas líneas donde configuras el Treeview
treeFrame = ttk.Frame(frame)  # Ajusta el ancho y alto del frame
treeFrame.grid(row=0, column=1,pady=10)  # Cambié a row=3 para que esté debajo de los widgets

treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("No", "MENOR DE 30", "CAMPEON", "POSICION", "PIERNA HABIL", "BUEN FICHAJE", "% SI", "% NO")
treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=14)  # Aumentar la altura
treeview.pack(expand=True, fill='both')  # Hacer que el Treeview expanda y llene el frame

# Ajustar el ancho de las columnas (opcional)
for col in cols:
    treeview.column(col, width=100)  # Cambia el ancho a un tamaño mayor
    treeview.heading(col, text=col, anchor="center")  # Centrar texto en los encabezados

# Cambiar el estilo de la fuente del encabezado y de las filas
style.configure("Treeview", font=("Helvetica", 10))  # Cambia el tamaño de la fuente para las filas
style.configure("Treeview.Heading", font=("Helvetica", 10))  # Cambia el tamaño de la fuente para los encabezados

treeScroll.config(command=treeview.yview)
# Crear el LabelFrame que contiene el Treeview
sub_table_frame = ttk.LabelFrame(frame, text="Última Predicción")
sub_table_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

# Definir las columnas del Treeview
sub_tree_cols = ("No", "% SI", "% NO", "Resultado Buen Fichaje")

# Crear el Treeview
sub_treeview = ttk.Treeview(sub_table_frame, show="headings", columns=sub_tree_cols, height=2)

# Configurar el ancho y centrado de las columnas
sub_treeview.column("No", width=50, anchor="center")
sub_treeview.column("% SI", width=50, anchor="center")
sub_treeview.column("% NO", width=50, anchor="center")
sub_treeview.column("Resultado Buen Fichaje", width=150, anchor="center")

# Configurar los encabezados de las columnas
sub_treeview.heading("No", text="No")
sub_treeview.heading("% SI", text="% SI")
sub_treeview.heading("% NO", text="% NO")
sub_treeview.heading("Resultado Buen Fichaje", text="Resultado Buen Fichaje")

# Empaquetar el Treeview
sub_treeview.pack(expand=True, fill="both")


# Crear un botón de salir con estilo personalizado
exit_button = customtkinter.CTkButton(
    root,
    text="Exit", 
    image=icon_photo2,  # Agregar el ícono
    fg_color="#ff626e",  # Color de fondo del botón
    hover_color="#D32F2F",  # Color al pasar el mouse sobre el botón
    text_color="#000000",  # Color del texto del botó
    font=("Arial", 16, "bold"),  # Estilo y tamaño de la fuente
    command=root.destroy  # Comando para salir de la aplicación
)

# Posicionar el botón en la parte inferior derecha
exit_button.pack(side='bottom', anchor='se', padx=10, pady=10)

root.mainloop()
