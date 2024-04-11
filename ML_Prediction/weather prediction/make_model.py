import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from sklearn.linear_model import SGDClassifier
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('weatherHistory.csv')

#df.dropna(axis=0,inplace=True)


'''
print(df.head())

print(df.shape)

print(df.info())
print(df.describe().T)
print(df.isnull().sum())

'''
print(df.columns)
print(df.dtypes)
df.drop_duplicates(inplace=True,keep='first')
'''for col in df.columns:
   
  # Checking if the column contains
  # any null values
  if df[col].isnull().sum() > 0:
    print(df[col].isnull().sum())
   # val = df[col].mean()
    #df[col] = df[col].fillna(val)
     
#print(df.isnull().sum().sum())
#print(df.groupby('RainToday').mean())'''

features = list(df.select_dtypes(include = np.number).columns)

print(features)#['Temperature (C)', 'Apparent Temperature (C)', 'Humidity', 'Wind Speed (km/h)', 'Wind Bearing (degrees)', 'Visibility (km)', 'Loud Cover', 'Pressure (millibars)']

df.drop(['Temperature (C)', 'Apparent Temperature (C)','Loud Cover',], axis=1, inplace=True)#highly correlated
features = df.drop(['Summary','Precip Type','Formatted Date','Daily Summary'], axis=1)
target = df['Summary']
print(features.columns)


X_train, X_val,Y_train, Y_val = train_test_split(features,target,test_size=0.2,random_state=2)
sgd_classifier = SGDClassifier(max_iter=1000,shuffle=True,tol=10,learning_rate='optimal',loss='perceptron',alpha=0.5,penalty='elasticnet',random_state=2)
# Train the model on the training data
sgd_classifier.fit(X_train, Y_train)
from sklearn.metrics import classification_report
# Make predictions on the validation set
val_predictions = sgd_classifier.predict(X_val)
# Print classification report
print(classification_report(Y_val, val_predictions))
joblib.dump(sgd_classifier, 'model.pkl')
