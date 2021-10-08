import pandas as pd
import matplotlib.pyplot as plt
#load Data
node2_record = pd.read_csv("../Data/Node2Missing.csv")
node2_record.AbsT = pd.to_datetime(node2_record.AbsT)
node2_record = node2_record.set_index("AbsT")
print("Orignal Data:\n", node2_record.Temp["2016-03-15 11:59:40":"2016-03-15 12:20:30"])

node2_record_fill_NA = node2_record.Temp.resample("5s").first()
print("Fill with NA: \n", node2_record_fill_NA["2016-03-15 12:00":"2016-03-15 12:00:30"])

plt.figure(figsize=(15,7))
plt.plot(node2_record.Temp,"*", label="orignal Data")
for method in ["nearest", "linear", "cubic"]: #for each method
    plt.plot(node2_record_fill_NA.interpolate(method=method), label=method)
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.legend()
plt.grid()
plt.title("Fill Missing Values")
plt.show()

#Decide to use linear interpolation
node2_record_fill_data = node2_record_fill_NA.interpolate(method="linear")
node2_record_fill_data = pd.DataFrame(node2_record_fill_data)
print(node2_record_fill_data["2016-03-15 11:59:40":"2016-03-15 12:00:30"])
node2_record_fill_data.to_csv("Node2TemperatureFillMissing.csv")