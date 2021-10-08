import pandas as pd
from scipy.stats import ttest_1samp, t, sem
import matplotlib.pyplot as plt # for plot graph

df_temp = pd.read_csv("../Data/NodeTemperature.csv") # Load the csv file
df_temp.AbsT = pd.to_datetime(df_temp.AbsT)
# convert data-time text into actual datetime list
df_temp = df_temp.set_index("AbsT") # set "AbsT" column as index column
t_scores = [] #empty list
p_values = [] #empty list
significance_level = 0.05 # Type I Error
target_temp = 20.8
for row in range(df_temp.shape[0]):
  data = df_temp.iloc[row]
  t_score, p_val = ttest_1samp(data, popmean=target_temp)
  t_scores.append(t_score)
  if t_score < 0:
    # Expecting positive t-score if
    # temperature is above target_temp
    # t-score < 0 indicates that temp is lower
    # than the target_temp.
    # Thus, change p to 1-p when t-score <0
    p_values.append(1 - p_val/2.0)
  else:
    p_values.append(p_val/2.0) # Divided by 2 since it is 2-tail test
t_crit = t.ppf(1 - significance_level,3) #df = n-1=4-1 sensors

# convert t_scores and p_values into pandas data frame
test_stats = pd.DataFrame({"t_score":t_scores,
                           "p_value":p_values,
                           "t_critical":t_crit},
                          index=df_temp.index)
test_stats.to_csv("TTestFor20_8.csv") # save to file

# plot the t-score and p-value
plt.figure(figsize=(15,8))
plt.subplot(2,1,1)
plt.plot(test_stats.t_score, label="t-score")
plt.plot(test_stats.t_critical, label="5%-Significance Critical Value")
plt.grid()
plt.legend()
plt.subplot(2,1,2)
plt.plot(test_stats.p_value, label="p-value")
plt.grid()
plt.ylim(0,0.2)
plt.yticks([0,0.05,0.1,0.15,0.2])
plt.legend()
plt.show()

#plot the on and off time with node temperatures
alpha = significance_level
ac_on = (test_stats.p_value < alpha)
plt.figure(figsize=(15,8))
plt.plot(ac_on*1+20.2, label="Ac ON")
plt.plot(df_temp.node1, label="node1")
plt.plot(df_temp.node2, label="node2")
plt.plot(df_temp.node3, label="node3")
plt.plot(df_temp.node4, label="node4")
plt.grid()
plt.xlabel("Time")
plt.title("AC On vs Temperatures")
plt.show()

def makeText(is_on):
    if is_on:
        return "On"
    else:
        return "Off"
ac_status = pd.DataFrame({"status": ac_on},
                         index=df_temp.index)
ac_status.status = ac_status.status.map(makeText)
print(ac_status.head())
ac_status.to_csv("ACStatus.csv")

