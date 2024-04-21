import serial
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Configura el puerto serie
ser = serial.Serial('COM7', 115200)  # Ajusta el puerto y la velocidad de acuerdo a tu configuración

# Inicializa las listas para almacenar los datos
timestamps = []
ecg_data = []

# Bandera para indicar si se está recibiendo un nuevo lote
new_batch_received = False

# Función para guardar los datos en un archivo CSV con nombre basado en la fecha actual
def save_to_csv(timestamps, ecg_data):
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f'ecg_data_{current_date}.csv'
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'ECG Data'])
        for timestamp, data in zip(timestamps, ecg_data):
            writer.writerow([timestamp, data])
    return file_name

# Función para graficar los datos
def plot_data(timestamps, ecg_data):
    plt.plot(timestamps, ecg_data)
    plt.xlabel('Timestamp')
    plt.ylabel('ECG Data')
    plt.title('ECG Data Plot')
    plt.show()

# Lee los datos del puerto serie y los procesa
while True:
    line = ser.readline().decode().strip()
    
    if line == 'NEW_BATCH':
        if timestamps and ecg_data:
            # Guarda los datos en un archivo CSV
            csv_file = save_to_csv(timestamps, ecg_data)
            # Grafica los datos
            plot_data(timestamps, ecg_data)
            # Limpia las listas para los nuevos datos
            timestamps.clear()
            ecg_data.clear()
            break  # Sale del bucle while después de guardar un archivo CSV
        new_batch_received = True
    else:
        if new_batch_received:
            # Ignora la primera línea de datos después de recibir un nuevo lote
            new_batch_received = False
        else:
            # Divide la línea en timestamp y valor ECG
            timestamp, data = map(int, line.split(','))
            timestamps.append(timestamp)
            ecg_data.append(data)
