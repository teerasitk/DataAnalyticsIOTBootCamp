import pandas as pd
import numpy as np
#load Data
node1_record = pd.read_csv("../Data/Node1_5SecData.csv")
node1_record.AbsT = pd.to_datetime(node1_record.AbsT)
node1_record = node1_record.set_index("AbsT")

oneminuteTemp = node1_record.Temp["2016-03-15 10:08:00":"2016-03-15 10:09:00"]
print(oneminuteTemp)

resample = oneminuteTemp.resample("1s").first()
print(resample.head())
interplated_dat = resample.interpolate(method="nearest") # or "linear", or "cubicspline"
print(interplated_dat.head())
import matplotlib.pyplot as plt
plt.figure(figsize=(15,7))
plt.plot(oneminuteTemp,"o", label="orignal Data")
for method in ["nearest", "linear", "cubic"]: #for each method
    plt.plot(resample.interpolate(method=method), label=method)
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.legend()
plt.grid()
plt.show()
