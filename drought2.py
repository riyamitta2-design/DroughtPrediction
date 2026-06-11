import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
df= pd.read_csv("C:\\Users\\riyam\\OneDrive\\Documents\\weather.csv")
print(df)
print(df.head())
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.info()) 
print(df.describe()) #Stats
print(df["Rainfall"])
print(type(df["Rainfall"]))
print(df[["Rainfall", "Temperature"]])
print(df.iloc[0:2]) #Selecting rows from 0 to 2 excluded
print(df.iloc[0,0])
print(df[df["Rainfall"]<25])
print(df[(df["Temperature"]>38) & (df["Rainfall"]<25)])
df["Drought"] = df["Rainfall"] <25
print(df.head())
print(df["City"].value_counts())
print(df.sort_values("Rainfall"))
print(df.groupby(["City", "Temperature"])["Rainfall"].agg(["mean","max","min"]).reset_index())
#plt.hist(df["Temperature"],bins=5)
#plt.title("Distribution of Temperature")
#plt.xlabel("Temperature")
#plt.ylabel("Frequency")
#plt.show()
#plt.scatter(df["Temperature"],df["Rainfall"])
#plt.show()
print(df["Temperature"].corr(df["Rainfall"]))
df1=df.groupby(["City"])["Rainfall"].agg(["mean"])
print(df1.head())
df1.plot(kind="bar")
#plt.show()
#plt.boxplot(df["Rainfall"])
#plt.show()
#df["Drought"].value_counts().plot(kind="pie")
plt.ylim(0,150)
plt.show()
X = df[["Rainfall","Temperature","Humidity"]]
X.head()

