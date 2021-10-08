import pandas as pd
import numpy as np
#load Data
node1_record = pd.read_csv("../Data/Node1_5SecData.csv")
node1_record.AbsT = pd.to_datetime(node1_record.AbsT)
node1_record = node1_record.set_index("AbsT")
print(node1_record.head())
# plot the temperature to check
import matplotlib.pyplot as plt
plt.figure(figsize=(15,7))
plt.plot(node1_record.Temp)
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.grid()
plt.title("Node 1 Temperature")
plt.show()

# make power spectral Density

nd1_temp = node1_record.Temp
nd1_mean = nd1_temp.mean()
nd1_temp = nd1_temp - nd1_mean # remove mean
psd, fs = plt.psd(nd1_temp.to_numpy(), Fs = 1/5)
plt.show()
#our orignal data is sample once every 5 seconds

numerate = ((fs**2)*psd).sum() # \int_0^\infty (fs^2)S_xx(f)df
denominator = psd.sum() # \int_0^\infty S_xx(f)df
fb = np.sqrt( numerate/ denominator)

T = 1/(2 * fb) # sampling rate at 2 time bandwidth
Ts = T/4 # pratically we will sample at 4 time Nyquist rate
print(f"Bandwidth: {fb} Hz.")
print(f"Nyquist Sampling Period: {T:0.0f} s.")
print(f"Practical Sampling Period: {Ts:0.0f} s.")

node1_temp230s = node1_record.Temp.resample("230s").mean() # resample to 230 s
node1_temp50s = node1_record.Temp.resample("50s").mean() #resample to 50 s
plt.figure(figsize=(15,7))
plt.plot(node1_record.Temp, label="Original at 5s")
plt.plot(node1_temp50s, label="Sample at 50s")
plt.plot(node1_temp230s, label="Sample at 230s")
plt.legend()
plt.xlabel("Time")
plt.grid()
plt.show()