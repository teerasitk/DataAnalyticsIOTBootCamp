from sklearn import linear_model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

node1 = pd.read_csv("../Data/Node1.csv", index_col="AbsT")
node1.index = pd.to_datetime(node1.index)
humidity = node1.RelH

k = 700
K = 100
plt.plot(humidity.values[k-K:k+K+1])
plt.show()

K = 15 # (2*15+1)=31 samples
regr = linear_model.LinearRegression()

num_dat = len(humidity)
output = []
x = np.arange(2*K+1).reshape(-1,1)
for k in range(num_dat):
  if k < K:
    output.append(0)
  elif num_dat-k < K+1:
    output.append(0)
  else:
    dat_win = humidity.iloc[k-K:k+K+1].values
    regr.fit(x, dat_win)
    output.append(regr.coef_)
slope = pd.Series(output, index=humidity.index)
detected_results = (slope > 0) # our result
actual_occupancy = (node1.Occ > 0.5) # ground data

plt.subplot(2,1,1)
plt.plot(detected_results, 
         label="Detected positive slope")
plt.legend()
plt.subplot(2,1,2)
plt.plot(actual_occupancy, 
         label="Someone inside")
plt.legend()
plt.show()
actual_occupancy = pd.DataFrame(actual_occupancy)
detected_results  = pd.DataFrame(detected_results)
detected_results.to_csv("detectedResult.csv")
actual_occupancy.to_csv("groundData.csv")


print("Accuracy: ", accuracy_score(actual_occupancy, detected_results))
