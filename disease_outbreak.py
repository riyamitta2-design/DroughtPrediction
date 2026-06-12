import pandas as pd
df = pd.read_csv("C:\\Users\\riyam\\Downloads\\Final_data.csv")
print(df.head())
print(df.columns)
print(df.shape)
print(df["Disease"].unique())
print(df["Disease"].value_counts())
df["Result"] = (df["Disease"]=="Dengue").astype(int)
df = df.drop(columns=["Unnamed: 0"])#removing index column from data set
print(df.isnull().sum())
print(df["Deaths"].describe())
df = df.drop(columns = ["Deaths"])
df["preci"] = df["preci"].fillna(df["preci"].median)
print(df["LAI"].describe())