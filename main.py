# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 21:39:35 2018

@author: angga
"""
import Tkinter, Tkconstants, tkFileDialog
import glob
import winsound #untuk play dan stop music
import sys
from numpy import *
from scipy import signal
import scipy.io.wavfile
from matplotlib import pyplot
import sklearn.decomposition
    
root = Tkinter.Tk()#membuat window baru

#create blank tabel
def blank(i,j):
	enter = Tkinter.Label(root)
	enter.grid(row=i,column=j)

#fungsi untuk tombol browse
def browse():
    file_dialog = Tkinter.Tk()
    file_dialog.withdraw()
    global file_name #global variabel
    file_name = tkFileDialog.askopenfilename(initialdir = "/",title = "Select File",filetypes = (("wav file","*.wav"),("all files","*.*")))
    
    split_file_name = file_name.split("/")
    input_browse.insert(1,(split_file_name[len(split_file_name)-1]))#print file wave
    return file_name

#fastICA
def ica():
    # First load the audio data, the audio data on this example is obtained from http://www.ism.ac.jp/~shiro/research/blindsep.html
    rate, source = scipy.io.wavfile.read(file_name)

    # The 2 sources are stored in left and right channels of the audio
    source_1, source_2 = source[:, 0], source[:, 1]
    data = c_[source_1, source_2]

    # Normalize the audio from int16 range to [-1, 1]
    data = data / 2.0 ** 15

    # Perform Fast ICA on the data to obtained separated sources
    fast_ica  = sklearn.decomposition.FastICA( n_components=2  )
    separated = fast_ica.fit_transform( data )

    # Check, data = separated X mixing_matrix + mean
    assert allclose( data, separated.dot( fast_ica.mixing_.T ) + fast_ica.mean_ )

    # Map the separated result into [-1, 1] range
    max_source, min_source = 1.0, -1.0
    max_result, min_result = max(separated.flatten()), min(separated.flatten())
    separated = map( lambda x: (2.0 * (x - min_result))/(max_result - min_result) + -1.0, separated.flatten() )
    separated = reshape( separated, (shape(separated)[0] / 2, 2) )
	
    # Store the separated audio, listen to them later
    vokal = "destination/vokal.wav"
    instrument = "destination/instrument.wav"
    scipy.io.wavfile.write(vokal, rate, separated[:, 0] )
    scipy.io.wavfile.write(instrument, rate, separated[:, 1] )
    vokal = vokal.split("/")
    instrument = instrument.split("/")
    tabel_isi(3,1,vokal[1],"Vokal")
    tabel_isi(4,2,instrument[1],"Instrument")
    
    # Plot the original and separated audio data
    fig = pyplot.figure( figsize=(10, 8) )
    fig.canvas.set_window_title("Blind Source Separation")

    ax = fig.add_subplot(221)
    ax.set_title("Source #1")
    ax.set_ylim([-1, 1])
    ax.get_xaxis().set_visible( False )
    pyplot.plot( data[:, 0], color='r' )

    ax = fig.add_subplot(223)
    ax.set_ylim([-1, 1])
    ax.set_title("Source #2")
    ax.get_xaxis().set_visible( False )
    pyplot.plot( data[:, 1], color='r' )

    ax = fig.add_subplot(222)
    ax.set_ylim([-1, 1])
    ax.set_title("Separated #1")
    ax.get_xaxis().set_visible( False )
    pyplot.plot( separated[:, 0], color='g' )

    ax = fig.add_subplot(224)
    ax.set_ylim([-1, 1])
    ax.set_title("Separated #2")
    ax.get_xaxis().set_visible( False )
    pyplot.plot( separated[:, 1], color='g' )
    pyplot.show()

#untuk mulai split
def go():
    ica()

#fungsi untuk play music pada folder destination
def play_music(wav_name):
	winsound.PlaySound("destination/"+wav_name,winsound.SND_FILENAME|winsound.SND_ASYNC)

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
    			  btn_play[i] = Tkinter.Button(root, text = "PLAY", command=lambda: play_music(wav_name[i]))
    			  btn_play[i].grid(row=i,column=j)
            elif(j == 3):#membuat button stop
    			  btn_stop[i] = Tkinter.Button(root, text = "STOP", command=lambda: stop_music(wav_name[i]))
    			  btn_stop[i].grid(row=i,column=j)
            else:
                string = str(jenis)
            if j < 2 or j > 3:#saat yang ditampilkan adalah bukan button
                tabel = Tkinter.Entry(root,width=30)
                tabel.insert(1," %s"%(string))#insert data tabel
                tabel.grid(row=i, column=j)
                
#menulis judul pada window
root.title("Browse Music")

baris = 0
#membuat inputan browse
input_browse = Tkinter.Entry(root,width=30)
input_browse.grid(row=baris,column=baris)

#membuat tombol browse
btn_browse = Tkinter.Button(root, text = "BROWSE", command=browse)
btn_browse.place(x=190,y=0)

#membuat tombol go
btn_browse = Tkinter.Button(root, text = "SEPARATE", command=go)
btn_browse.place(x=255,y=0)

blank(baris+1,0)
#membuat tabel header
tabel = Tkinter.Label(root,text = "NO")
tabel.grid(row=baris+2, column=0)

tabel = Tkinter.Label(root,text = "FILENAME")
tabel.grid(row=baris+2, column=1)

tabel = Tkinter.Label(root,text = "PLAYER")
tabel.grid(row=baris+2, column=2)

tabel = Tkinter.Label(root,text = "MUSIC")
tabel.grid(row=baris+2, column=3)

tabel = Tkinter.Label(root,text = "TYPE")
tabel.grid(row=baris+2, column=4)

tabel_isi(baris+3,"","","")#buat tabel pertama untuk display aja

root.mainloop()
