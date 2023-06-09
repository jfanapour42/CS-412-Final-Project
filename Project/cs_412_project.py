# -*- coding: utf-8 -*-
"""CS_412_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AIWj1VlJg-Yu0WKcb8rU-FxJs9U5nqk7
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import cv2
import numpy as np
import statistics
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
style.use('ggplot')
from IPython import display
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras import layers
import os
import tempfile

from sklearn import svm
from sklearn import metrics
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import make_column_selector as selector
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold

#from google.colab import drive
from google.colab import drive
drive.mount('/content/drive')

path = './drive/MyDrive/CS_412/Project/'

heart_disease = pd.read_csv(path + "heart_2020_cleaned.csv")

heart_disease.shape

heart_disease.head(10)

heart_disease.columns

heart_disease.dtypes

numOfPositive = heart_disease['HeartDisease'].value_counts()['Yes']
numOfNegative = heart_disease['HeartDisease'].value_counts()['No']
print("Number of people with heart disease {}".format(numOfPositive))
print("Number of people whom don't have heart disease {}".format(numOfNegative))

perc = (numOfPositive/(numOfPositive+numOfNegative))*100
print("Percentage of people with heart disease: %.2f%%" % perc)

categorical_columns_selector = selector(dtype_include=object)
categorical_columns = categorical_columns_selector(heart_disease)
categorical_columns

data_categorical = heart_disease[categorical_columns]
data_categorical.head()

HeartDisease_column = data_categorical[['HeartDisease']]

encoder = OrdinalEncoder()
heartdisease_encoded = encoder.fit_transform(HeartDisease_column)
heartdisease_encoded[:,0:10]

encoder.categories_

encoder = OrdinalEncoder(categories=[['No', 'Yes'], ['No', 'Yes'], ['No', 'Yes'], ['No', 'Yes'],
                                     ['No', 'Yes'], ['Female', 'Male'], 
                                     ['18-24', '25-29','30-34', '35-39', '40-44', '45-49', '50-54',
                                      '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older'],
                                     ['American Indian/Alaskan Native', 'Asian', 'Black', 'Hispanic',
                                      'White', 'Other'],
                                     ['No', 'Yes (during pregnancy)', 'No, borderline diabetes', 'Yes'],
                                     ['No', 'Yes'],
                                     ['Poor', 'Fair', 'Good', 'Very good', 'Excellent'],
                                     ['No', 'Yes'], ['No', 'Yes'], ['No', 'Yes']])

data_encoded = encoder.fit_transform(data_categorical)
data_encoded[:5]

encoder.categories_

for idx, col in enumerate(categorical_columns):
  heart_disease[col] = pd.Series(data_encoded[:, idx])

heart_disease.head(10)

yData = heart_disease['HeartDisease'].to_numpy()
xData = heart_disease.drop(columns=['HeartDisease'])

xTrain, xTest , yTrain, yTest = train_test_split(xData, yData, test_size = 0.20)

treeModel = tree.DecisionTreeClassifier()
treeModel.fit(xTrain, yTrain)

text_representation = tree.export_text(treeModel)
print(text_representation)

# Predict
y_train_predict = treeModel.predict(xTrain)
y_test_predict = treeModel.predict(xTest)

#Display the outcome of classification
print("Training accuracy: " + str(metrics.accuracy_score(yTrain, y_train_predict)))
print("Testing accuracy: " + str(metrics.accuracy_score(yTest, y_test_predict)))
print("\n")
print(metrics.classification_report(yTest, y_test_predict))

mat = metrics.confusion_matrix(yTest, y_test_predict)
labels = ['Negative', 'Positive']

sns.heatmap(mat, square=True, annot=True, fmt='d', cbar=False, cmap='Blues',
            xticklabels=labels, yticklabels=labels)
 
plt.xlabel('Predicted label')
plt.ylabel('Actual label')

# define model
treeModel = DecisionTreeClassifier()
# define evaluation procedure
rskf = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
# evaluate model
scores = cross_val_score(treeModel, xData, yData, scoring='roc_auc', cv=rskf, n_jobs=-1)
# summarize performance
print('Mean ROC AUC: %.3f' % statistics.mean(scores))

XGBModel = xgb.XGBClassifier()

# Fit
XGBModel.fit(xTrain, yTrain)

# Predict
y_predict = XGBModel.predict(xTest)

print(metrics.classification_report(yTest, y_predict))

mat = metrics.confusion_matrix(yTest, y_predict)
labels = ['Negative', 'Positive']

sns.heatmap(mat, square=True, annot=True, fmt='d', cbar=False, cmap='Blues',
            xticklabels=labels, yticklabels=labels)
 
plt.xlabel('Predicted label')
plt.ylabel('Actual label')

'''#Takes too long to execute
#infeasible for data size

# clf is a non-linear svm classifier
clf = svm.SVC(kernel = 'rbf')

# Fit data
clf.fit(xTrain, yTrain)

# Predict
y_train_predict = clf.predict(xTrain)
y_test_predict = clf.predict(xTest)

#Display the outcome of classification
print("Training accuracy: " + str(metrics.accuracy_score(yTrain, y_train_predict)))
print("Testing accuracy: " + str(metrics.accuracy_score(yTest, y_test_predict)))
print("\n")
print(metrics.classification_report(yTest, y_test_predict))
print(metrics.confusion_matrix(yTest, y_test_predict))'''

LRModel = LinearRegression(fit_intercept=True)
LRModel.fit(xTrain, yTrain)

# Predict
y_train_predict = LRModel.predict(xTrain)
y_test_predict = LRModel.predict(xTest)

# Print Coefficients
print("Coefficients: \n")
for i in range(len(LRModel.coef_)):
  print(xData.columns[i], " ", LRModel.coef_[i])

# Print Intercept
print("Intercept: ", LRModel.intercept_)

# Print R-squared
print('\n')
print('R-squared for training: %.2f' % r2_score(yTrain, y_train_predict))
print('R-squared for testing: %.2f' % r2_score(yTest, y_test_predict))

# Print mean squared error
print('mean squared error for training: %.2f'% mean_squared_error(yTrain, y_train_predict))
print('mean squared error for testing: %.2f'% mean_squared_error(yTest, y_test_predict))

selector = RFECV(estimator = LinearRegression(fit_intercept=True), step=1, cv=5, scoring='neg_mean_squared_error')
selector = selector.fit(xData, yData)
f = selector.get_support(True) #the most important features
best_features = [xData.columns[x] for x in f]
print(best_features)

print(f)

best_xData = xData[best_features]

best_xTrain, best_xTest , best_yTrain, best_yTest = train_test_split(best_xData, yData, test_size = 0.20)

# Build model
best_LRModel = LinearRegression(fit_intercept=True)
best_LRModel.fit(best_xTrain, best_yTrain)

# Predict
y_train_predict = best_LRModel.predict(best_xTrain)
y_test_predict = best_LRModel.predict(best_xTest)

# Print Coefficients
print("Coefficients: \n")
for i in range(len(best_LRModel.coef_)):
  print(best_xData.columns[i], " ", best_LRModel.coef_[i])

# Print Intercept
print("Intercept: ", best_LRModel.intercept_)

# Print R-squared
print('\n')
print('R-squared for training: %.2f' % r2_score(best_yTrain, y_train_predict))
print('R-squared for testing: %.2f' % r2_score(best_yTest, y_test_predict))

# Print mean squared error
print('mean squared error for training: %.2f'% mean_squared_error(best_yTrain, y_train_predict))
print('mean squared error for testing: %.2f'% mean_squared_error(best_yTest, y_test_predict))

logModel = LogisticRegression() 
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=1) 
lst_accu_stratified = []

for train_index, test_index in skf.split(xData, yData): 
    X_train_fold, X_test_fold = xData.iloc[train_index], xData.iloc[test_index] 
    y_train_fold, y_test_fold = yData[train_index], yData[test_index]
    logModel.fit(X_train_fold, y_train_fold) 
    lst_accu_stratified.append(logModel.score(X_test_fold, y_test_fold))

print('Maximum Accuracy',max(lst_accu_stratified)) 
print('Minimum Accuracy:',min(lst_accu_stratified)) 
print('Overall Accuracy:',statistics.mean(lst_accu_stratified))

NNModel = tf.keras.Sequential()
NNModel.add(layers.Dense(512, activation='relu', input_dim=17))
NNModel.add(layers.Dense(512, activation='relu'))
NNModel.add(layers.Dense(1, activation='sigmoid'))
NNModel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
NNModel.summary()

hist = NNModel.fit(xTrain, yTrain, validation_data=(xTest, yTest), epochs=10, batch_size=100)

sns.set()
 
acc = hist.history['accuracy']
val = hist.history['val_accuracy']
epochs = range(1, len(acc) + 1)
 
plt.plot(epochs, acc, '-', label='Training accuracy')
plt.plot(epochs, val, ':', label='Validation accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.plot()

y_predict = NNModel.predict(xTest) > perc/100 # 0.0856              #0.5
mat = metrics.confusion_matrix(yTest, y_predict)
labels = ['Negative', 'Positive']
 
print(metrics.classification_report(yTest, y_predict))

sns.heatmap(mat, square=True, annot=True, fmt='d', cbar=False, cmap='Blues',
            xticklabels=labels, yticklabels=labels)
 
plt.xlabel('Predicted label')
plt.ylabel('Actual label')

xTrain2, xTest2, yTrain2, yTest2 = train_test_split(xData, yData, test_size=0.2)
xTrain2, xVal, yTrain2, yVal = train_test_split(xTrain2, yTrain2, test_size=0.2)

scaler = StandardScaler()
xTrain2 = scaler.fit_transform(xTrain2)

xVal = scaler.transform(xVal)
xTest2 = scaler.transform(xTest2)

METRICS = [
      keras.metrics.TruePositives(name='tp'),
      keras.metrics.FalsePositives(name='fp'),
      keras.metrics.TrueNegatives(name='tn'),
      keras.metrics.FalseNegatives(name='fn'), 
      keras.metrics.BinaryAccuracy(name='accuracy'),
      keras.metrics.Precision(name='precision'),
      keras.metrics.Recall(name='recall'),
      keras.metrics.AUC(name='auc'),
      keras.metrics.AUC(name='prc', curve='PR'), # precision-recall curve
]

'''NNModel2 = tf.keras.Sequential()
NNModel2.add(layers.Dense(512, activation='relu', input_dim=17))
NNModel2.add(layers.Dense(512, activation='relu'))
NNModel2.add(layers.Dense(1, activation='sigmoid'))
NNModel2.compile(optimizer='adam', loss='binary_crossentropy', metrics=METRICS)
NNModel2.summary()'''

'''layers.Dense(
            16, activation='relu',
            input_shape=(xData.shape[-1],)),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid',
                          bias_initializer=output_bias),'''

def make_model(metrics=METRICS, output_bias=None):
  if output_bias is not None:
    output_bias = tf.keras.initializers.Constant(output_bias)
  model = keras.Sequential(
      [
        layers.Dense(512, activation='relu', input_shape=(xData.shape[-1],)),
        layers.Dense(512, activation='relu'),
        layers.Dense(1, activation='sigmoid', bias_initializer=output_bias)
      ]
  )

  model.compile(
      optimizer=keras.optimizers.Adam(learning_rate=1e-3),
      loss=keras.losses.BinaryCrossentropy(),
      metrics=metrics)

  return model

EPOCHS = 100
BATCH_SIZE = 2048

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_prc', 
    verbose=1,
    patience=10,
    mode='max',
    restore_best_weights=True)

NNModel2 = make_model(output_bias=perc/100)
NNModel2.summary()

initial_weights = os.path.join(tempfile.mkdtemp(), 'initial_weights')
NNModel2.save_weights(initial_weights)

NNModel2.load_weights(initial_weights)
hist = NNModel2.fit(
    xTrain2,
    yTrain2,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    callbacks=[early_stopping],
    validation_data=(xVal, yVal))

mpl.rcParams['figure.figsize'] = (12, 10)
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

def plot_metrics(history):
  metrics = ['loss', 'prc', 'precision', 'recall']
  for n, metric in enumerate(metrics):
    name = metric.replace("_"," ").capitalize()
    plt.subplot(2,2,n+1)
    plt.plot(history.epoch, history.history[metric], color=colors[0], label='Train')
    plt.plot(history.epoch, history.history['val_'+metric],
             color=colors[0], linestyle="--", label='Val')
    plt.xlabel('Epoch')
    plt.ylabel(name)
    if metric == 'loss':
      plt.ylim([0, plt.ylim()[1]])
    elif metric == 'auc':
      plt.ylim([0.8,1])
    else:
      plt.ylim([0,1])

    plt.legend()

plot_metrics(hist)

#hist = NNModel2.fit(xTrain, yTrain, validation_data=(xTest, yTest), epochs=10, batch_size=100)

sns.set()
mpl.rcParams['figure.figsize'] = (6, 5)
 
acc = hist.history['accuracy']
val = hist.history['val_accuracy']
epochs = range(1, len(acc) + 1)
 
plt.plot(epochs, acc, '-', label='Training accuracy')
plt.plot(epochs, val, ':', label='Validation accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.plot()

y_predict = NNModel2.predict(xTest2) > perc/100
mat = metrics.confusion_matrix(yTest2, y_predict)
labels = ['Negative', 'Positive']
 
print(metrics.classification_report(yTest2, y_predict))

sns.heatmap(mat, square=True, annot=True, fmt='d', cbar=False, cmap='Blues',
            xticklabels=labels, yticklabels=labels)
 
plt.xlabel('Predicted label')
plt.ylabel('Actual label')

train_predictions_baseline = NNModel2.predict(xTrain2, batch_size=BATCH_SIZE)
test_predictions_baseline = NNModel2.predict(xTest2, batch_size=BATCH_SIZE)

def plot_cm(labels, predictions, p=0.5):
  cm = metrics.confusion_matrix(labels, predictions > p)
  plt.figure(figsize=(5,5))
  sns.heatmap(cm, annot=True, fmt="d")
  plt.title('Confusion matrix @{:.2f}'.format(p))
  plt.ylabel('Actual label')
  plt.xlabel('Predicted label')

  print('Healthy Patient identified (True Negatives): ', cm[0][0])
  print('Healthy Patient Incorrectly Diagnosed (False Positives): ', cm[0][1])
  print('Heart Disease Missed (False Negatives): ', cm[1][0])
  print('Heart Disease Detected (True Positives): ', cm[1][1])
  print('Total Patients: ', np.sum(cm[1]))

results = NNModel2.evaluate(xTest2, yTest2,
                                  batch_size=BATCH_SIZE, verbose=0)
for name, value in zip(NNModel2.metrics_names, results):
  print(name, ': ', value)
print()

plot_cm(yTest2, test_predictions_baseline, perc/100)

from sklearn.neighbors import KNeighborsClassifier
KNNModel = KNeighborsClassifier(n_neighbors=5)

# Fit data
KNNModel.fit(xTrain, yTrain)

# Predict
y_train_predict = KNNModel.predict(xTrain)
y_test_predict = KNNModel.predict(xTest)


#Display the outcome of classification
print("Training accuracy: " + str(metrics.accuracy_score(yTrain, y_train_predict)))
print("Testing accuracy: " + str(metrics.accuracy_score(yTest, y_test_predict)))
print("\n")
print(metrics.classification_report(yTest, y_test_predict))
plot_cm(yTest2, y_test_predict)

"""## References



*   https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease
*   https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features
*   https://inria.github.io/scikit-learn-mooc/python_scripts/03_categorical_pipeline.html
*   https://stackoverflow.com/questions/72170947/how-to-use-ordinalencoder-to-set-custom-order
*   https://www.projectpro.io/recipes/explain-stratified-k-fold-cross-validation
*   https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html
*   https://machinelearningmastery.com/cost-sensitive-decision-trees-for-imbalanced-classification/
*   https://towardsdatascience.com/getting-started-with-xgboost-in-scikit-learn-f69f5f470a97
*   https://www.atmosera.com/blog/binary-classification-with-neural-networks/
*   https://towardsdatascience.com/beginners-guide-to-xgboost-for-classification-problems-50f75aac5390
*   https://www.tensorflow.org/tutorials/structured_data/imbalanced_data

https://www.cdc.gov/nchs/fastats/leading-causes-of-death.htm

https://www.who.int/news-room/fact-sheets/detail/the-top-10-causes-of-death

https://www.cdc.gov/chronicdisease/resources/publications/factsheets/heart-disease-stroke.htm#:~:text=Leading%20risk%20factors%20for%20heart,unhealthy%20diet%2C%20and%20physical%20inactivity.
"""