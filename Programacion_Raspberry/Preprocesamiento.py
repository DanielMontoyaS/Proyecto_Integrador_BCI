import numpy as np
import scipy
from scipy.signal import filtfilt,iirnotch
from scipy import signal
from sklearn import preprocessing

def bandPassFilter(signal):
    fs,lowcut,highcut = 250, 7.5 , 31.0 # Frecuencias de corte
    order = 3  # orden de filtro
    b , a = scipy.signal.butter(order, [lowcut, highcut], "bandpass", analog= False, fs=fs)
    y = scipy.signal.filtfilt(b,a,signal,axis=0)
    return(y)

def NotchFilter(signal):
    fs = 250 #Frecuencia de muestreo
    f0 = 60.0  # Frecuencia de remoción (Hz)
    Q = 3.0  # Factor de calidad
    bn, an = iirnotch(f0, Q, fs) # Diseño de filtro
    y = scipy.signal.filtfilt(bn,an,signal,axis=0,method="gust") # Aplicación del filtro
    return(y)


# Segmentación de la muestra
 
def get_frame(DF_elec , frame_size,hop_size):
    df=DF_elec
    frames=[]
    min_max_scaler = preprocessing.MinMaxScaler()
    
    for i in range(0,len(df)-frame_size+1,hop_size):
      ch1=min_max_scaler.fit_transform(df[0].values[i:i+frame_size].reshape(frame_size,1))
      ch2=min_max_scaler.fit_transform(df[1].values[i:i+frame_size].reshape(frame_size,1))
      ch3=min_max_scaler.fit_transform(df[2].values[i:i+frame_size].reshape(frame_size,1))
      ch4=min_max_scaler.fit_transform(df[3].values[i:i+frame_size].reshape(frame_size,1))
      ch5=min_max_scaler.fit_transform(df[4].values[i:i+frame_size].reshape(frame_size,1))
      ch6=min_max_scaler.fit_transform(df[5].values[i:i+frame_size].reshape(frame_size,1))
      ch7=min_max_scaler.fit_transform(df[6].values[i:i+frame_size].reshape(frame_size,1))
      ch8=min_max_scaler.fit_transform(df[7].values[i:i+frame_size].reshape(frame_size,1)) 
    
      array = np.concatenate((ch2,ch6,ch1,ch5,ch7,ch4), axis=1) #Matriz de señales
  
      frames.append(array)

    return np.array(frames)



