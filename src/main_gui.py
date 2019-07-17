from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import tkinter
import winsound #untuk play dan stop music
import sys
import glob
from numpy import *
from scipy import signal
from matplotlib import pyplot
import sklearn.decomposition

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import math
import os
from scipy.io import wavfile
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import FastICA
from sklearn.decomposition import SparsePCA
from method.data_utils import Audio
    
root = tkinter.Tk()#membuat window baru

def ica(X):
    # Compute ICA
    ica = FastICA()
    S_ = ica.fit(X).transform(X)  # Get the estimated sources
    A_ = ica.mixing_  # Get estimated mixing matrix
    np.allclose(X, np.dot(S_, A_.T) + ica.mean_)
    return S_


def sca(X):
    # Compute ICA
    sca = SparsePCA()
    S_ = sca.fit(X).transform(X)  # Get the estimated sources
    return S_

def write_wav(fs_1, S_, method, file_name, write_wav=True):
    # filename = os.listdir(file_name)
    if method == "ICA":
        #if the using method is ICA
        multiply_factor = 1000000

        temp_output_1 = multiply_factor*S_[:,0]
        temp_output_2 = multiply_factor*S_[:,1] 

    if method == "SCA":
        multiply_factor = 1

        temp_output_1 = multiply_factor*S_[:,1]
        temp_output_2 = multiply_factor*S_[:,0] 

    if write_wav == True:

        #write separates wav audio
        name_wav = file_name.split("/")
        nameI = name_wav[-1].split("_")
        #untuk instrumen
        wavfile.write("../results/separates_audio/"+nameI[0]+"_"+nameI[1]+"_"+"Instrumen"+"_"+"Separate"+method+"_"+nameI[3], fs_1, temp_output_1.astype(np.int16))
        #untuk vokal
        wavfile.write("../results/separates_audio/"+nameI[0]+"_"+nameI[1]+"_"+"Vokal"+"_"+"Separate"+method+"_"+nameI[3], fs_1, temp_output_2.astype(np.int16))
        tabel_isi(3,1,nameI[0]+"_"+nameI[1]+"_"+"Instrumen"+"_"+"Separate"+method+"_"+nameI[3],"Instrumen")
        tabel_isi(4,2,nameI[0]+"_"+nameI[1]+"_"+"Vokal"+"_"+"Separate"+method+"_"+nameI[3],"Vokal")

#create blank tabel
def blank(i,j):
	enter = tkinter.Label(root)
	enter.grid(row=i,column=j)

#fungsi untuk tombol browse
def browse():
    file_dialog = tkinter.Tk()
    file_dialog.withdraw()
    global file_name #global variabel
    file_name = filedialog.askopenfilename(initialdir = "/",title = "Select File",filetypes = (("wav file","*.wav"),("all files","*.*")))
    
    split_file_name = file_name.split("/")
    input_browse.delete(0, END)
    input_browse.insert(1,(split_file_name[len(split_file_name)-1]))#print file wave

#untuk mulai split
def go(getDropdown):
    # read file

    fs_1, voice_1 = wavfile.read(file_name)
    voice_1 = voice_1.astype(np.float64)

    if getDropdown == "ICA":
        S_ = ica(voice_1)
        write_wav(fs_1,S_,getDropdown,file_name)
    else:
        S_ = sca(voice_1)
        write_wav(fs_1,S_,getDropdown,file_name)

#fungsi untuk play music pada folder destination
def play_music(wav_name):
	winsound.PlaySound("../results/separates_audio/"+wav_name,winsound.SND_FILENAME|winsound.SND_ASYNC)

#fungsi untuk stop music pada folder destination
def stop_music(wav_name):
	winsound.PlaySound(None, winsound.SND_FILENAME|winsound.SND_ASYNC)

#create tabel
def tabel_isi(baris,no,filename,jenis):
    btn_play =  {} #array button play
    btn_stop =  {} #arrat button stop
    wav_name = {} #array nama lagu
    for i in range(baris,baris+1):
        for j in range(5):
            if(j == 0):
                string = str(no)
            elif(j == 1):
                string = wav_name[i] = str(filename)
			  #wav_name[i] = str(string)
            elif(j == 2):#membuat button play
            	btn_play[i] = tkinter.Button(root, text = "PLAY", command=lambda: play_music(wav_name[i]))
            	btn_play[i].grid(row=i,column=j)
            elif(j == 3):#membuat button stop
            	btn_stop[i] = tkinter.Button(root, text = "STOP", command=lambda: stop_music(wav_name[i]))
            	btn_stop[i].grid(row=i,column=j)
            else:
                string = str(jenis)
            if j < 2 or j > 3:#saat yang ditampilkan adalah bukan button
                tabel = tkinter.Entry(root,width=30)
                tabel.insert(1," %s"%(string))#insert data tabel
                tabel.grid(row=i, column=j)
                
#menulis judul pada window
root.title("PyBSS")

baris = 0
#membuat inputan browse
input_browse = tkinter.Entry(root,width=30)
input_browse.grid(row=baris,column=baris)

#membuat tombol browse
btn_browse = tkinter.Button(root, text = "BROWSE", command=browse)
btn_browse.place(x=190,y=0)

#membuat combo box
tabel = tkinter.Label(root,text = "METODE")
tabel.place(x=403, y=0)

comboExample = ttk.Combobox(root, 
                            values=[
                                    "ICA", 
                                    "SCA"])
# comboExample.grid(row=baris+1, column=baris)
comboExample.place(x=457,y=0)
comboExample.current(0)
# print(comboExample.current(), comboExample.get())

#membuat tombol go
btn_browse = tkinter.Button(root, text = "SEPARATE", 
    command=lambda: go(comboExample.get()))
btn_browse.place(x=255,y=0)

blank(baris+1,0)
#membuat tabel header
tabel = tkinter.Label(root,text = "NO")
tabel.grid(row=baris+2, column=0)

tabel = tkinter.Label(root,text = "FILENAME")
tabel.grid(row=baris+2, column=1)

tabel = tkinter.Label(root,text = "PLAYER")
tabel.grid(row=baris+2, column=2)

tabel = tkinter.Label(root,text = "MUSIC")
tabel.grid(row=baris+2, column=3)

tabel = tkinter.Label(root,text = "TYPE")
tabel.grid(row=baris+2, column=4)

tabel_isi(baris+3,"","","")#buat tabel pertama untuk display aja

root.mainloop()
