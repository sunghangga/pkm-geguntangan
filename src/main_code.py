import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import math
from scipy.io import wavfile
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import FastICA
from get_sources.data_utils import Audio


n_loop = 1
n_sources = 2
Audio(nb_tracks=n_sources, param=n_loop).load_tracks(param=n_loop)

fs_1, voice_1 = wavfile.read("../results/sources_audio/1_vokal_source.wav")
fs_2, voice_2 = wavfile.read("../results/sources_audio/1_instrumen_source.wav")
m, = voice_1.shape
voice_2 = voice_2[:m]


S = np.c_[voice_1, voice_2]
# A = np.array([[1, 1], [0.5, 2]])
A = np.array([[0.3816, 0.8678], [0.8534, -0.5853]])  # Mixing matrix
X = np.dot(S, A.T)  # Generate observations

# Compute ICA
ica = FastICA()
S_ = ica.fit(X).transform(X)  # Get the estimated sources
A_ = ica.mixing_  # Get estimated mixing matrix
np.allclose(X, np.dot(S_, A_.T))

multiply_factor = 1000000 ;

temp_output_1 = multiply_factor*S_[:,0]
temp_output_2 = multiply_factor*S_[:,1]

#write mixing wav audio
wavfile.write("../results/mix_audio/1_mix" + ".wav", fs_2, X.astype(np.int16))

print(temp_output_1)
print(temp_output_2)

MSE = mean_squared_error(temp_output_1, temp_output_2)
print(MSE)

#masih salah
print(-10 * math.log10(MSE))

#write separates wav audio
wavfile.write("../results/separates_audio/1_vokal_separate" + ".wav", fs_2, temp_output_1.astype(np.int16))
wavfile.write("../results/separates_audio/1_instrumen_separate" + ".wav", fs_2, temp_output_2.astype(np.int16))


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