import pandas as pd
from lazypredict.Supervised import LazyClassifier
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import joblib
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('training.csv')
data.sort_index(inplace = True)
# Data manipulation
# data.loc[data["state"] == "normal", "state"] = True
# data.loc[data["state"] == "abnormal", "state"] = False
# data.rename(columns = {'state':'abnormality'}, inplace = True)
# data.to_csv('out.csv')
print(data)
data = data.iloc[:, 1:] # Fit without index 
X = data.loc[:, ~data.columns.isin(['state'])] 
y= data['state']
print(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state = 0)

# Create a decision tree model and fit it to the training data
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Make predictions on the testing data and evaluate the model's accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy}")
data.to_csv('pred.csv')

# Store the model to a file
filename = 'decision_tree_model.sav'
joblib.dump(model, filename)

clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
models,predictions = clf.fit(X_train, X_test, y_train, y_test)

print(models)
