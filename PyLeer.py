import serial, time
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime

arduino = serial.Serial('COM7', 115200, timeout=0.01)  # Se debe indicar el puerto serial y la velocidad de transmisión 

time.sleep(2)

numero_datos = 1000  # Para de graficar a los 1000 datos
ECG = np.ndarray((0), dtype=int)  # aquí se almacenará la señal 

# mientras el arreglo no tenga los datos que requiero los solicito
while ECG.shape[0] < numero_datos:
    
    # esto lee lo que haya en el buffer
    datos = arduino.readlines(arduino.inWaiting())
    
    datos_por_leer = len(datos)
    
    # Si hay mas datos de los que quiero leer
    # solo me quedo con la cantidad que me interesa
    if len(datos) > numero_datos:
        datos = datos[0:numero_datos]
        # creo un arreglo de ceros para leer estos valores
        valores_leidos = np.zeros(numero_datos, dtype=int)
    else:
        # creo un arreglo de ceros para leer estos valores
        valores_leidos = np.zeros(datos_por_leer, dtype=int)

    
    posicion = 0
    #se convierten los datos a valores numericos de voltaje. 
    for dato in datos:
        # voy a tratar de convertir los datos
        try:
            # elimino los saltos de linea y caracter de retorno y convierto a entero
            valores_leidos[posicion] = int(dato.decode().strip())
        except:
            # si no puedo convertir completo la muestra con el anterior
            # valores_leidos[posicion] = 0  # alternativa
            valores_leidos[posicion] = valores_leidos[posicion - 1]
        posicion = posicion + 1
    # agrego los datos leidos al arreglo
    ECG = np.append(ECG, valores_leidos)
    # Introduzco un delay para que se llene de nuevo el buffer
    time.sleep(2)

# como la ultima lectura puede tener mas datos de los que necesito descarto las muestras restantes
ECG = ECG[0:numero_datos]

# Obtener la fecha y hora actual
fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# Crear el nombre del archivo con la fecha actual
csv_filename = f"ECG_{fecha_actual}.csv"

# Guardar los datos en un archivo CSV
with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    for dato in ECG:
        writer.writerow([dato])

# ya con los datos leidos podemos graficar
plt.plot(ECG)
plt.show()

arduino.close()  # Cerrar puerto serial, siempre debe cerrarse
