import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from sklearn.linear_model import SGDClassifier
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('Rainfall.csv')

df.replace(to_replace=['yes','no','Yes',"No"],value=[1,0,1,0],inplace=True)
df.rename(str.strip,axis='columns',inplace=True)



print(df.head())

print(df.shape)

print(df.info())
print(df.describe().T)
print(df.isnull().sum())
print(df.columns)


for col in df.columns:
   
  # Checking if the column contains
  # any null values
  if df[col].isnull().sum() > 0:
    val = df[col].mean()
    df[col] = df[col].fillna(val)
     
print(df.isnull().sum().sum())
print(df.groupby('RainToday').mean())

features = list(df.select_dtypes(include = np.number).columns)

print(features)



df.drop(['MaxTemp', 'MinTemp'], axis=1, inplace=True)#highly correlated
features = df.drop(['RainToday','RainTomorrow'], axis=1)
target = df.RainToday
X_train, X_val,Y_train, Y_val = train_test_split(features,target,test_size=0.2,stratify=target,random_state=2)
sgd_classifier = SGDClassifier(random_state=42)
# Train the model on the training data
sgd_classifier.fit(X_train, Y_train)
from sklearn.metrics import classification_report
# Make predictions on the validation set
val_predictions = sgd_classifier.predict(X_val)
# Print classification report
print(classification_report(Y_val, val_predictions))
joblib.dump(sgd_classifier, 'Todays_rainfall_prediction_model.pkl')

#############################################################################
target = df.RainTomorrow
X_train, X_val,Y_train, Y_val = train_test_split(features,target,test_size=0.2,stratify=target,random_state=2)
sgd_classifier = SGDClassifier(random_state=42)
# Train the model on the training data
sgd_classifier.fit(X_train, Y_train)
from sklearn.metrics import classification_report
# Make predictions on the validation set
val_predictions = sgd_classifier.predict(X_val)
# Print classification report
print(classification_report(Y_val, val_predictions))
joblib.dump(sgd_classifier, 'Tomorrows_rainfall_prediction_model.pkl')
