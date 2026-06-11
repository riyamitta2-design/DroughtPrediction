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
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import numpy as np
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.ensemble import RandomForestRegressor

df= pd.read_csv("C:\\Users\\riyam\\OneDrive\\Documents\\weather.csv")
X = df[["Temperature","Humidity"]]
y = df[["Rainfall"]]
X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.2,
random_state=2
)
model = LinearRegression()
model.fit(X_train,y_train)
pred = model.predict(X_test)
print(pred)
print(y_test)

mae = mean_absolute_error(y_test,pred)
print(mae)#Average size of prediction errors, lower mae means better predictions
mse = mean_squared_error(y_test,pred)
print(np.sqrt(mse))
print(r2_score(y_test,pred)) #r2 score shows how much data is explained by our model, r2 = 1 is perfect
print(model.coef_) #coefficients of each input feature shows the relationship between that input and that output, if the coefficient is positive it that if the input goes up the output increases
#If the coefficient is negative, as the input feature increases, the output will decrease. For example if temp goes up, rainfall goes down.
print(model.intercept_)
tree = DecisionTreeRegressor(max_depth=3)
tree.fit(X_train,y_train)
pred_tree = tree.predict(X_test)
print(pred_tree)
rules = export_text(
tree,
feature_names=list(X.columns)
)

print(rules)
print("Decision Tree Rules:")
print(export_text(tree,
                  feature_names=list(X.columns)))

plot_tree(
    tree,
    feature_names=X.columns,
    filled=True,
    rounded=True
)

plt.show()

reg_model = RandomForestRegressor(n_estimators=100,max_depth=4)
reg_model.fit(X_train,y_train)
reg_pred = reg_model.predict(X_test)
print(y_test)
print(reg_pred)
mae_reg = mean_absolute_error(y_test,reg_pred)
mse_reg = mean_squared_error(y_test, reg_pred)
print(mae_reg,mse_reg)
