import cv2
import pandas as pd
import random
import time
import argparse
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds

###############################################
###          Para ejecutar en CMD           ###
### --board-id 0 --serial-port /dev/ttyUSB0 ###
###############################################

DatosBEO, DatosLCH, DatosRCH, DatosDescanso = [], [], [], []
BEO, LCH, RCH, Descanso = "1", "2", "3", "4"
beo, lch, rch, des = 0, 0, 0, 0
ide = 0


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


def mainlch(placa):
    name = "S"+Subject+"R"+str(Run)+Tipo+LCH
    im = cv2.imread('C:/Users/HP/Documents/Project_Signals/Izquierda.jpg')
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", im)
    cv2.waitKey(10)

    time.sleep(2)
    data_lch = placa.get_current_board_data(500)
    df = pd.DataFrame(np.transpose(data_lch))

    df.to_csv("C:/Users/HP/Documents/Project_Signals/Recoleccion/SAMPLES/" + name + "_" +
              str(lch) + '.csv')


def mainrch(placa):
    name = "S" + Subject + "R" + str(Run) + Tipo + RCH
    im = cv2.imread('C:/Users/HP/Documents/Project_Signals/Derecha.jpg')
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", im)
    cv2.waitKey(10)

    time.sleep(2)
    data_rch = placa.get_current_board_data(500)
    df = pd.DataFrame(np.transpose(data_rch))

    df.to_csv("C:/Users/HP/Documents/Project_Signals/Recoleccion/SAMPLES/" + name + "_" +
              str(rch) + '.csv')


def mainbeo(placa):

    name = "S" + Subject + "R" + str(Run) + Tipo + BEO
    im = cv2.imread('C:/Users/HP/Documents/Project_Signals/Imagenes/Baseline.jpg')
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", im)
    cv2.waitKey(10)

    time.sleep(2)
    data_beo = placa.get_current_board_data(500)
    df = pd.DataFrame(np.transpose(data_beo))

    df.to_csv("C:/Users/HP/Documents/Project_Signals/Recoleccion/SAMPLES/" + name + "_" +
              str(beo) + '.csv')


def descanso(placa):
    name = "S"+Subject+"R"+str(Run)+Tipo+Descanso+"_"+ide
    im = cv2.imread('C:/Users/HP/Documents/Project_Signals/Imagenes/Descanso.jpg')
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", im)
    cv2.waitKey(10)

    time.sleep(2)
    data_descanso = placa.get_current_board_data(500)
    df = pd.DataFrame(np.transpose(data_descanso))

    df.to_csv("C:/Users/HP/Documents/Project_Signals/Recoleccion/SAMPLES/" + name + "_" +
              str(des) + '.csv')


operaciones = {'1': mainlch, '2': mainrch}

Subject = input('Ingresar identificación del sujeto: ')
Tipo = input('Ingresar el tipo de experimento a realizar (M/I): ')   # Tipos posibles M , I 
Run = int(input('Ingresar el número de serie: '))

time.sleep(20)

board_info = carga()
board_info.prepare_session()
print(board_info.get_sampling_rate(0))
board_info.start_stream()

valores = 0

while __name__ == '__main__':
    mainbeo(board_info)
    beo += 1
    des = 1
    ide = BEO
    descanso(board_info)

    inicio1 = time.time()

    while valores != 160:
        valores = lch + rch
        print(valores)
        opcion = str(random.randint(1, 2))
        if opcion == '1' and lch != 80:
            operaciones[opcion](board_info)
            lch += 1
            des = lch
            ide = LCH
            descanso(board_info)

        elif opcion == '2' and rch != 80:
            operaciones[opcion](board_info)
            rch += 1
            des = rch
            ide = RCH
            descanso(board_info)
    print("Tiempo", (time.time() - inicio1))

    valores, lch, rch = 0, 0, 0

    continuar = input("Desea continuar (S/N) :")

    if continuar == 'N' or continuar == 'n':
        board_info.stop_stream()

        break
    else:
        Run += 1
