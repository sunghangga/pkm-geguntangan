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
	# ica = FastICA()
	# A_ = ica.mixing_
	# print(np.allclose(X, S_))
	# print(X)
	# print(S_)
	# print(np.allclose(X, np.dot(S_, A_.T) + np.mean(sca.components_ == 0)))
	return S_


def mse(S_,voice_1,voice_2,method):
	# S_[:,0] = instrumen, S_[:,1] = vokal
	# voice_1 = vokal, voice_2 = instrumen
	MSE = []
	#pengujian metode MSE
	if method == "Ica":
		MSE.append(mean_squared_error(voice_1/1000000, S_[:,1]/1000000)) # MSE vokal
		MSE.append(mean_squared_error(voice_2/1000000, S_[:,0]/1000000)) # MSE instrumen
	else:
		MSE.append(mean_squared_error(voice_1/1000000, S_[:,0]/1000000)) # MSE vokal
		MSE.append(mean_squared_error(voice_2/1000000, S_[:,1]/1000000)) # MSE instrumen
	
	return MSE


def sir(MSE):
	#pengujian metode SIR
	SIR = []
	SIR.append(-10 * math.log10(MSE[0])) # SIR vokal
	SIR.append(-10 * math.log10(MSE[1])) # SIR instrumen
	return SIR


def write_wav(X, fs_2, S_, MSE, SIR, method, fVokal, fInstrumen, estimated=True, write_matrix=False, write_wav=True):

	if method == "Ica":
		#if the using method is ICA
		multiply_factor = 1000000;

		temp_output_1 = multiply_factor*S_[:,0]
		temp_output_2 = multiply_factor*S_[:,1]	

	if method == "Sca":
		multiply_factor = 1;

		temp_output_1 = multiply_factor*S_[:,1]
		temp_output_2 = multiply_factor*S_[:,0]	

	if write_matrix == True:
		#write matriks of data
		print("Matriks pemisahan suara 1 metode "+method+": " + str(temp_output_1))
		print("Matriks pemisahan suara 2 metode "+method+": " + str(temp_output_2))

	if estimated == True:
		print("Estimasi error MSE (vokal) metode "+method+": " + str(MSE[0]))
		print("Estimasi error MSE (instrumen) metode "+method+": " + str(MSE[1]))
		print("Estimasi error SIR metode (vokal) "+method+": " + str(SIR[0]))
		print("Estimasi error SIR metode (instrumen) "+method+": " + str(SIR[1]))

	if write_wav == True:
		#write mixing wav audio
		nameV = fVokal.split("_")
		wavfile.write("../results/mix_audio/"+nameV[0]+"_"+nameV[1]+"_"+"Mix"+method+"_"+nameV[3], fs_2, X.astype(np.int16))

		#write separates wav audio
		nameI = fInstrumen.split("_")
		#untuk instrumen
		wavfile.write("../results/separates_audio/"+nameI[0]+"_"+nameI[1]+"_"+nameI[2]+"_"+"Separate"+method+"_"+nameI[3], fs_1, temp_output_1.astype(np.int16))
		#untuk vokal
		wavfile.write("../results/separates_audio/"+nameV[0]+"_"+nameV[1]+"_"+nameV[2]+"_"+"Separate"+method+"_"+nameV[3], fs_2, temp_output_2.astype(np.int16))


def load_data():
	# Loading Data
	n_sources = 1 #untuk banyak data yang akan di load ke direktori source
	directory = os.path.abspath(__file__ + "/../../data")
	for filename in os.listdir(directory):
		if filename.endswith(".wav"):
			# if "vokal" in filename.lower():
			print(filename)
			audio = Audio(nb_tracks=n_sources, param=filename).load_tracks(param=filename)
			continue
		else:
			continue
	

# n_sources = 2
# n = 2
# audio = Audio(nb_tracks=n_sources, param=n).load_tracks(param=n)

#untuk membuat data
# load_data()

# method = Ica atau Sca
method = "Ica"

directoryVokal = os.path.abspath(__file__ + "/../../results/sources_audio/vokal/")
directoryInstrumen = os.path.abspath(__file__ + "/../../results/sources_audio/instrumen/")
for filenameVokal in os.listdir(directoryVokal):
	for filenameInstrumen in os.listdir(directoryInstrumen):
		if filenameVokal.endswith(".wav") and filenameInstrumen.endswith(".wav"):
			fs_1, voice_1 = wavfile.read("../results/sources_audio/vokal/"+filenameVokal)
			fs_2, voice_2 = wavfile.read("../results/sources_audio/instrumen/"+filenameInstrumen)
			m, = voice_1.shape
			voice_2 = voice_2[:m]

			S = np.c_[voice_1, voice_2]

			# A = np.array([[1, 1], [0.5, 2]])
			A = np.array([[0.3816, 0.8678], [0.8534, -0.5853]])  # Mixing matrix
			X = np.dot(S, A.T)  # Generate observations

			if method == "Ica":
				S_ = ica(X)
				MSE_ica = mse(S_,voice_1,voice_2,method)
				SIR_ica = sir(MSE_ica)
				write_wav(X,fs_2,S_,MSE_ica,SIR_ica,method,filenameVokal,filenameInstrumen)
			else:
				S_ = sca(X)
				MSE_sca = mse(S_,voice_1,voice_2,method)
				SIR_sca = sir(MSE_sca)
				write_wav(X,fs_2,S_,MSE_sca,SIR_sca,method,filenameVokal,filenameInstrumen)
			continue
		else:
			continue
		print("\n")
		break

# # Plot results
# pl.figure()

# # pl.title('True Sources')
# pl.subplot(5, 1, 1)
# pl.plot(voice_1)
# pl.subplot(5, 1, 2)
# pl.plot(voice_2)

# # pl.title('Observations (mixed signal)')
# pl.subplot(5, 1, 3)
# pl.plot(X)

# # pl.title('ICA estimated sources')
# pl.subplot(5, 1, 4)
# pl.plot(S_[:,0])
# pl.subplot(5, 1, 5)
# pl.plot(S_[:,1])

# pl.subplots_adjust(0.09, 0.04, 0.94, 0.94, 0.26, 0.36)
# pl.show()