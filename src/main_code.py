import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import math
from scipy.io import wavfile
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import FastICA
from sklearn.decomposition import SparsePCA


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
	A_ = ica.mixing_
	# print(np.allclose(X, S_))
	print(X)
	print(S_)
	print(np.allclose(X, np.dot(S_, A_.T) + np.mean(sca.components_ == 0)))
	return S_


def mse(S_):
	#pengujian metode MSE
	MSE = mean_squared_error(S_[:,0]/1000000, S_[:,1]/1000000)
	return MSE


def sir(MSE):
	#pengujian metode SIR
	SIR = -10 * math.log10(MSE)
	return SIR


def write_wav(X, fs_2, S_, MSE, SIR, method, estimated=True, write_matrix=True, write_wav=True):

	if method == "ica":
		#if the using method is ICA
		multiply_factor = 1000000 ;

		temp_output_1 = multiply_factor*S_[:,0]
		temp_output_2 = multiply_factor*S_[:,1]	

	if method == "sca":
		temp_output_1 = S_[:,0]
		temp_output_2 = S_[:,1]	

	if write_matrix == True:
		#write matriks of data
		print("Matriks pemisahan suara 1 metode "+method+": " + str(S_[:,0]))
		print("Matriks pemisahan suara 2 metode "+method+": " + str(S_[:,1]))

	if estimated == True:
		print("Estimasi error MSE metode "+method+": " + str(MSE))
		print("Estimasi error SIR metode "+method+": " + str(SIR))

	if write_wav == True:
		#write mixing wav audio
		wavfile.write("../results/mix_audio/1_mix_"+method+".wav", fs_2, X.astype(np.int16))

		#write separates wav audio
		wavfile.write("../results/separates_audio/1_vokal_separate_"+method+".wav", fs_2, temp_output_2.astype(np.int16))
		wavfile.write("../results/separates_audio/1_instrumen_separate_"+method+".wav", fs_2, temp_output_1.astype(np.int16))


method = "sca"

fs_1, voice_1 = wavfile.read("../results/sources_audio/1_vokal_source.wav")
fs_2, voice_2 = wavfile.read("../results/sources_audio/1_instrumen_source.wav")
m, = voice_1.shape
voice_2 = voice_2[:m]

S = np.c_[voice_1, voice_2]
# A = np.array([[1, 1], [0.5, 2]])
A = np.array([[0.3816, 0.8678], [0.8534, -0.5853]])  # Mixing matrix
X = np.dot(S, A.T)  # Generate observations

if method == "ica":
	S_ = ica(X)
	MSE_ica = mse(S_)
	SIR_ica = sir(MSE_ica)
	write_wav(X,fs_2,S_,MSE_ica,SIR_ica,method)
else:
	S_ = sca(X)
	MSE_sca = mse(S_)
	SIR_sca = sir(MSE_sca)
	write_wav(X,fs_2,S_,MSE_sca,SIR_sca,method)

# Plot results
# pl.figure()
# pl.subplot(3, 1, 1)
# pl.plot(S)
# pl.title('True Sources')
# pl.subplot(3, 1, 2)
# pl.plot(X)
# pl.title('Observations (mixed signal)')
# pl.subplot(3, 1, 3)
# pl.plot(S_)
# pl.title('ICA estimated sources')
# pl.subplots_adjust(0.09, 0.04, 0.94, 0.94, 0.26, 0.36)
# pl.show()