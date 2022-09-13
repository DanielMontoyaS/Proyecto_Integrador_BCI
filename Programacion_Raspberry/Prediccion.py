import pandas as pd
import random
import time
import argparse
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from matplotlib import pyplot as plt
import Preprocesamiento
from scipy import signal
from tensorflow.keras.models import load_model
import posicion
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model = load_model('Modelo_Red.h5') # Carga del modelo entrenado

# Configuracion de parametros para comunicacion
def carga():
    BoardShim.enable_dev_board_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=True)
    args = parser.parse_args()
    params = BrainFlowInputParams()
    params.serial_port = args.serial_port
    board = BoardShim(BoardIds.CYTON_BOARD.value, params)
    return board

# Inicio de transmision de datos
board_info = carga()  
board_info.prepare_session()  
board_info.start_stream()



while __name__ == '__main__':      # Loop de prediccion
    
    start_time_total = time.time()
    
    print("***** Iniciar *****")
    
    start_time_adquisicion = time.time()
    
    time.sleep(2)   # Tiempo para adquisicion de datos
    data = board_info.get_current_board_data(550)  # Adquirir datos
    dato = np.transpose(data)
    df = pd.DataFrame(dato)  
    datos = df.iloc[:, 1:9] 
    
    print("\n")
    print("Tiempo de Ejecucion adquisicion:",(time.time() - start_time_adquisicion))

    doc=[]  
    
    start_time_preprocesamiento = time.time()
    
    for i in range(1, 9): # Filtrado de senales para cada cama
        Electrodo = datos[i].to_numpy()  
        x_detrended = signal.detrend(Electrodo) 
        filtradoNotch = Preprocesamiento.NotchFilter(x_detrended) 
        sig_fil = Preprocesamiento.bandPassFilter(filtradoNotch) 
        sig_fil = sig_fil[25:-25] 
        doc.append(sig_fil) 
    
    arr = np.transpose(np.array(doc))  


    print("\n")
    print("Tiempo de Ejecucion procesamiento:",(time.time() - start_time_preprocesamiento))
    print("\n")
    start_time_clasificacion = time.time()   
    
    if arr.shape == (500,8):
        
        dFrame = pd.DataFrame(arr)  
        lista = [Preprocesamiento.get_frame(dFrame,250,75)]

        data_array = np.vstack(lista)

        prediccion = model.predict(data_array) #Clasificacion de acciones
        
        print("Segmentos clasificados:",prediccion.tolist())
        print("\n")
        prom_pred=[]
        
        for i in prediccion:
          norm = 1 * (i >= 0.50) # Threshold de aceptacion
      
          prom_pred.append(norm)

        pred = 1*(np.mean(prom_pred)>=0.50) # Threshold de aceptacion
        
        print("Aplicacion de Threshold de aceptacion:",prom_pred)

        print("\n")
        print("Tiempo de Ejecucion clasificacion:",(time.time() - start_time_clasificacion))
        print("\n")
        start_time_control = time.time()   
        
        if pred == 1:
          print("Intencion Motora Identificada:","Cerrar Mano", "    Promedio de clasificacion:",np.mean(prom_pred))
          posicion.Cerrado() # Accion de cerrar mano
        else:
          print("Intencion Motora Identificada:","Abrir Mano", "    Promedio de clasificacion:",np.mean(prom_pred))
          posicion.Abierto() # Accion de abrir mano
        
        print("\n")
        print("Tiempo de Ejecucion control de ortesis:",(time.time() - start_time_control))
        print("\n")
    
    print("Tiempo de Ejecucion total:",(time.time() - start_time_total))
    print("\n")
   
    print("***** Esperar ***** \n")
    print("\n")
    print("\n")


    
 