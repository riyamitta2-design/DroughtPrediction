import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import export_text
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.metrics import confusion_matrix
from sklearn.metrics import (
accuracy_score,
precision_score,
recall_score,
f1_score
)
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
df= pd.read_csv("C:\\Users\\riyam\\OneDrive\\Documents\\weather.csv")
df["Drought"] = df["Rainfall"] <25
X = df[["Rainfall","Temperature","Humidity"]]
print(X.head())
y = df[["Drought"]]
print(y.head())
X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.2,
random_state=2
)

print(X_train)
print(X_test)
print(len(df))
print(len(X_test))
print(len(X_train))
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(predictions)
print(y_test)


rules = export_text(
model,
feature_names=list(X.columns)
)

print(rules)
print(model.predict_proba(X_test))


plt.show()
cm = confusion_matrix(y_test,predictions)
print(cm)
accuracy = accuracy_score(y_test,predictions)
print(accuracy)
print(classification_report(y_test,predictions))
rf_model = RandomForestClassifier(n_estimators=100)
#rf_model.fit(X,y)
rv = [[100,30,80]]
#pred = rf_model.predict(rv)
#print(pred)
print(model.predict(rv))
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)
print(rf_predictions)
print(export_text(rf_model.estimators_[1], feature_names=list(X.columns)))
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)
knn = KNeighborsClassifier(n_neighbors = 3)
knn.fit(X_train_scaled,y_train)
pred_knn = knn.predict(X_test_scaled)
print(confusion_matrix(y_test,pred_knn))
new_day = pd.DataFrame({"Rainfall":[12], "Temperature":[36], "Humidity":[30]})
new_data = scaler.fit_transform(new_day)
new_day_pred = knn.predict(new_data)
print(new_day_pred)
print(model.predict(new_day))