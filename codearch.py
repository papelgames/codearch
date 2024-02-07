import tkinter as tk
from tkinter import filedialog
import csv
import sys

path = None

def modificar_csv(input_file, output_file):
    max_int = sys.maxsize
    text_area.config(state='normal')
    while True:
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int = int(max_int / 10)
    texto_comillas = f"Quitando comillas y tabulado \n"
    text_area.insert(tk.END, texto_comillas)
    text_area.see(tk.END)  # Desplazarse al final del texto
    with open(input_file, 'r', encoding='latin-1') as file:
       
        #while file:
        csv_text = file.read()
        
        # Reemplazar comillas dobles en todo el texto
        csv_text = csv_text.replace('"', '')
        csv_text = csv_text.replace('\t', '')

    with open(output_file, 'w', encoding='latin-1') as file:
        file.write(csv_text)
    #capturo cuantos punto y coma tiene para pasar parametro
    with open(input_file, 'r', encoding='latin-1') as file:
        csv_lines = file.readlines()

        # Contar puntos y comas en la primera línea
        first_line_fields = csv_lines[0].count(';')
        Q_lines = len(csv_lines)
        
  
    texto_loop = f"El modelo tiene : {first_line_fields}\n Iniciando loop\n"
    text_area.insert(tk.END, texto_loop)
    text_area.see(tk.END)  # Desplazarse al final del texto
    
    while True:  # Bucle para verificar hasta que no haya más líneas cortas
        with open(input_file, 'r', encoding='latin-1') as file:
            csv_text = file.readlines()
            lineas_cortas = [i for i, linea in enumerate(csv_text) if linea.count(';') < first_line_fields] #busco las lineas que no tienen la cantidad de campos correctos
            
            texto_Q_lineas = f"Corrigiendo : {len(lineas_cortas)} lineas \n "
            text_area.insert(tk.END, texto_Q_lineas)
            text_area.see(tk.END)  # Desplazarse al final del texto
            
            if not lineas_cortas:
                break  # Si no hay más líneas cortas, sal del bucle
            
            for i, linea in enumerate(csv_text):
                pycpl = linea.count(';')
                
                if pycpl < first_line_fields:
                    csv_text[i] = linea.replace('\n', '')  # Reemplazar saltos de línea por ''
                    texto_control_lineas = f" Quedan lineas \n "
                    text_area.insert(tk.END, texto_control_lineas)
                    text_area.see(tk.END)  # Desplazarse al final del texto
                    
                    break
        
        with open(output_file, 'w', encoding='latin-1') as file:
                file.writelines(csv_text)
    

def ejecutar_funcion(path_):
    text_area.config(state='normal')
    text_area.delete(1.0, tk.END)  # Limpiar el widget Text
    
    if path_:
        texto_inicio = f"Iniciando el proceso en el archivo: {path_}\n"
        text_area.insert(tk.END, texto_inicio)
        text_area.see(tk.END)  # Desplazarse al final del texto

        modificar_csv(path_, path_)

        texto_fin = "Proceso finalizado\n"
        text_area.insert(tk.END, texto_fin)
        text_area.see(tk.END)  # Desplazarse al final del texto
    else:
        texto_warning = "Debe seleccionar un archivo\n"
        text_area.insert(tk.END, texto_warning)
        text_area.see(tk.END)  # Desplazarse al final del texto
    
    texto_cierre = "Fin\n"
    text_area.insert(tk.END, texto_cierre)
    text_area.see(tk.END)  # Desplazarse al final del texto

    text_area.config(state='disabled')
    
def abrir_archivo():
    global path
    archivo = filedialog.askopenfilename(initialdir="/", title="Seleccionar Archivo", filetypes=[("Archivos CSV", "*.csv")])
    if archivo:
        label_archivo.config(text="Archivo seleccionado: " + archivo)
        path = archivo
       
# Crear la ventana principal
root = tk.Tk()
root.title("CoDeArch v 0.2")
root.resizable(False, False)
# Establecer el tamaño inicial de la ventana
root.geometry("600x600")  # Establece el tamaño inicial de la ventana en 800x600 píxeles

# Asignar un ícono a la ventana
root.iconbitmap(r'.\icono.ico')  
# .
# Botón para abrir el archivo
button_abrir = tk.Button(root, text="Abrir Archivo", command=abrir_archivo)
button_abrir.pack(pady=10)

# Botón para ejecutar la función
button_ejecutar = tk.Button(root, text="Ejecutar", command=lambda: ejecutar_funcion(path))
button_ejecutar.pack(pady=10)

# Etiqueta para mostrar el archivo seleccionado
label_archivo = tk.Label(root, text="Archivo seleccionado: ")
label_archivo.pack()

# Área de texto para mostrar la salida
text_area = tk.Text(root, height=50, width=200)
text_area.pack(padx=10, pady=10)
text_area.config(state='disabled')

# Ejecutar la aplicación
root.mainloop()