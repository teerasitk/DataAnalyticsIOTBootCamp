import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

nodex = pd.read_csv("../Data/faultyData.csv", index_col="AbsT")
nodex.index = pd.to_datetime(nodex.index)
plt.plot(nodex.Temp)
plt.show()

# Global Outlier
def z_score(data):
    data_mean = data.mean()
    data_std = data.std(ddof=1) + 1e-6
    # Add small number to avoid divided by zero
    z = (data - data_mean)/data_std
    z = np.abs(z)
    return z
def z_score_outlier(data, th=3.0):
    z = z_score(data)
    outlier = (z>th)
    return outlier

z = z_score(nodex.Temp)
z_outlier = z_score_outlier(nodex.Temp, th=3)

plt.figure(figsize=(15,7))
plt.subplot(3,1,1)
plt.plot(z,"o",label="z-score")
plt.legend()
plt.subplot(3,1,2)
plt.plot(z_outlier,"o", label="Outlier")
plt.legend()
plt.subplot(3,1,3)
plt.plot(nodex.Temp,"o", label="Temperature")
plt.legend()
plt.show()

def IQROutlier(data, whis=1.5):
    #whis=1.5 is a default values
    Q1 = data.quantile(0.25) #first quartie
    Q3 = data.quantile(0.75) #third quartie
    IQR = Q3-Q1 #interquartile range
    lower = Q1 - whis*IQR
    upper = Q3 + whis*IQR
    outlier = (data < lower) | (data > upper)
    return outlier

iqr_outlier = IQROutlier(nodex.Temp)
plt.figure(figsize=(10,9))
plt.subplot(2,1,1)
plt.plot(iqr_outlier,"o", label="IQR Outlier")
plt.legend()
plt.subplot(2,1,2)
plt.plot(nodex.Temp,"o", label="Temperature")
plt.legend()
plt.show()


def removeAndReplaceOutlier(data, outlier, intp="linear"):
    data_out = data.copy()
    data_out[outlier] = None
    data_out = data_out.interpolate(intp)
    return data_out

outlier_removed_by_z = removeAndReplaceOutlier(nodex.Temp, z_outlier)
outlier_removed_by_iqr = removeAndReplaceOutlier(nodex.Temp, iqr_outlier)
plt.figure(figsize=(15,8))
plt.subplot(2,1,1)
plt.plot(outlier_removed_by_z, label="Outlier-removed using z")
plt.plot(nodex.Temp, label="Temperature")
plt.legend()
plt.subplot(2,1,2)
plt.plot(outlier_removed_by_iqr, label="Outlier-removed using iqr")
plt.plot(nodex.Temp, label="Temperature")
plt.legend()
plt.grid()
plt.show()

outlier_removed_by_z.to_csv("removeByZ.csv")
outlier_removed_by_iqr.to_csv("removeByIQR.csv")