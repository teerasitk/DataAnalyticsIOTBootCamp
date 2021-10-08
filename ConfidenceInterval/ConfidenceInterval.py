
import pandas as pd
from scipy.stats import  t, sem
import matplotlib.pyplot as plt # for plot grapg

df_temp = pd.read_csv("../Data/NodeTemperature.csv") # Load the csv file
df_temp.AbsT = pd.to_datetime(df_temp.AbsT)
# convert data-time text into actual datetime list
df_temp = df_temp.set_index("AbsT") # set "AbsT" column as index column
print(df_temp.head()) # print first 5 rows
print("\n")
print("\n")
plt.figure(figsize=(15,8))
plt.plot(df_temp.node1, label=f"node1")
plt.plot(df_temp.node2, label=f"node2")
plt.plot(df_temp.node3, label=f"Node3")
plt.plot(df_temp.node4, label=f"node4")
plt.legend()
plt.title("Temperature")
plt.xlabel("Time")
plt.show()

# construct 95%  Confidence Interval
confidence = 0.95
lowers = []
uppers = []
means = []
for row in range(df_temp.shape[0]):# For each row
  data = df_temp.iloc[row] # get date
  lower, upper = t.interval(confidence,df=len(data)-1, loc=data.mean(),
                            scale=sem(data))
  #compute a confidence interval of temperature
  lowers.append(lower)
  uppers.append(upper)
  means.append(data.mean())

# save to file
confidenceMean = pd.DataFrame({"upper_Conf":uppers,
                               "lower_Conf":lowers,
                               "sensorMean":means},
                              index=df_temp.index)
confidenceMean.to_csv("confidenceInterval.csv") # save to csv file
# plot the output
plt.figure(figsize=(15,10))
plt.plot(confidenceMean.upper_Conf, label="upper bound")
plt.plot(confidenceMean.lower_Conf, label="lower bound")
plt.plot(confidenceMean.sensorMean, label="sensor mean")
plt.title("95% Confidence for Mean")
plt.grid()
plt.legend()
plt.show()