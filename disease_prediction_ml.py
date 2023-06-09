# -*- coding: utf-8 -*-
"""Disease Prediction ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J7abRmdf9NcEeodzAsRdWU-gbdBzb1Yo
"""

# Importing the necessary libraries

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display
pd.set_option('display.max_columns', None)

import os
root_dir = "/content/drive/My Drive"
from google.colab import drive
drive.mount('/content/drive')
project_folder = "/Colab Notebooks/"
os.chdir(root_dir + project_folder)

# Importing the dataset
train = pd.read_csv("Training.csv")
train = train.dropna(axis=1)
test = pd.read_csv("Testing.csv")
train = train.dropna(axis=1)


# Loading the dataset
X_train = train.drop('prognosis',axis=1)  # features (symptoms)
y_train = train['prognosis']  # target variable (disease)
X_test = test.drop('prognosis',axis=1)
y_test = test['prognosis']

"""##                                                                _Exploratory Data Analysis_"""

## No of occurences of each symptom in this dataset
print(X_train.apply(pd.Series.value_counts))

# Count the number of occurrences of '1' in each column and sort in descending order
symptom_counts = X_train.sum().sort_values(ascending=False)

# Select the top 20 symptoms
top_20_symptoms = symptom_counts[:20]

# Create a barplot of the top 20 symptoms
plt.figure(figsize=(10, 6))
plt.bar(top_20_symptoms.index, top_20_symptoms.values)
plt.xticks(rotation=90)
plt.xlabel('Symptom')
plt.ylabel('Count')
plt.title('Top 20 Symptoms by Occurrence')
plt.show()

print("The barplot shows top 20 symptoms in decreasing order. Top 5 of them include fatigue, vomiting, high fever, nausea and loss of apetite.")

## No of unique diseases as identified from the prognosis column
len(y_train.unique())
print("The number of unique diseases is 41")

## No of values for each prognosis
sns.countplot(x="prognosis", data=train)
plt.show()
print("As seen from the graph, the number of values for each prognosis is 120.")

# Calculate the correlation matrix
corr_matrix = X_train.corr()

# Plot the correlation matrix using a heatmap
sns.heatmap(corr_matrix, cmap='coolwarm', center=0, square=True, annot=False)

# Show the plot
plt.show()

"""## _K-Means Clustering_"""

### Using K-means clustering to find out diseases that are similar

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


# Determine the optimal number of clusters using silhouette score
silhouette_scores = []
for k in range(2, 12):
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X_train)
    score = silhouette_score(X_train, kmeans.labels_)
    silhouette_scores.append(score)

# Plot the silhouette scores for each number of clusters
plt.plot(range(2, 12), silhouette_scores)
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette score')
plt.show()

# Choose the number of clusters with the highest silhouette score and then perform K-means clustering
kmeans = KMeans(n_clusters=9, random_state=0).fit(X_train)

# Add the cluster labels to the dataset
train['cluster'] = kmeans.labels_

# Print the number of data points in each cluster
print(train['cluster'].value_counts())
train


## Grouping the diseases with similar clusters
cluster_counts = train.groupby('cluster')['prognosis'].value_counts()

# Print the count of each cluster
print(cluster_counts)
print('\n')
print("We can see the diseases grouped based on cluster assignment. This means that the symptoms for the diseases belonging to the same cluster are likely to be similar.")

test['clusters'] = kmeans.predict(X_test)
test

"""## _Random Forest Model_"""

### Building a predictive model using Random Forest Method

# Creating a random forest classifier with 100 trees
rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Training the random forest classifier
rf.fit(X_train, y_train)

# Making predictions on the testing set
y_pred1 = rf.predict(X_test)

# Evaluating the performance of the random forest classifier
accuracy_rf = accuracy_score(y_test, y_pred1)
precision_rf = precision_score(y_test, y_pred1,average='weighted')
recall_rf = recall_score(y_test, y_pred1,average='weighted')
f1_rf = f1_score(y_test, y_pred1,average='weighted')

print('Accuracy with Random Forest method:', accuracy_rf)
print('Precision with Random Forest method:', precision_rf)
print('Recall with Random Forest method:', recall_rf)
print('F1 with Random Forest method:', f1_rf)
print('\n')

## Getting prediction probabilities for each column using Random Forest classifier
rf_pred_prob = rf.predict_proba(X_test)

#print(y_pred_prob)

# Get the labels of each prognosis value
rf_prognosis_labels = rf.classes_

# Create a pandas DataFrame to store the predicted probabilities and their labels
pred_rf = pd.DataFrame(rf_pred_prob, columns=rf_prognosis_labels)

display(pred_rf)

"""## _Multinomial Logistic Regression_"""

# Create and train a multinomial logistic regression model
mlr = LogisticRegression(multi_class='multinomial', solver='lbfgs')
mlr.fit(X_train, y_train)

# Predict the output variable for the testing dataset
y_pred3 = mlr.predict(X_test)

# Calculate accuracy of the model
accuracy_mlr = accuracy_score(y_test, y_pred3)
precision_mlr = precision_score(y_test, y_pred3,average='weighted')
recall_mlr = recall_score(y_test, y_pred3,average='weighted')
f1_mlr = f1_score(y_test, y_pred3,average='weighted')

print('Accuracy for Multinomial Logistic Regression:', accuracy_mlr)
print('Precision with Multinomial Logistic Regression:', precision_mlr)
print('Recall with Multinomial Logistic Regression:', recall_mlr)
print('F1 with Multinomial Logistic Regression:', f1_mlr)
print('\n')

## Getting prediction probabilities for each column using Multiple Logistic Regression classifier
mlr_pred_prob = mlr.predict_proba(X_test)

#print(y_pred_prob)

# Get the labels of each prognosis value
mlr_prognosis_labels = mlr.classes_

# Create a pandas DataFrame to store the predicted probabilities and their labels
pred_mlr = pd.DataFrame(mlr_pred_prob, columns=mlr_prognosis_labels)
merged_df = pd.concat([X_train,pred_mlr],axis=1)
display(merged_df)

"""## _CART Model_"""

### Building a predictive model using CART Method
dtc = DecisionTreeClassifier(random_state=0)
dtc.fit(X_train, y_train)

# Predict the output variable for the testing dataset
y_pred4 = dtc.predict(X_test)

# Calculate accuracy of the model
accuracy_dt = accuracy_score(y_test, y_pred4)
precision_dt = precision_score(y_test, y_pred4,average='weighted')
recall_dt = recall_score(y_test, y_pred4,average='weighted')
f1_dt = f1_score(y_test, y_pred4,average='weighted')

print('Accuracy for CART:', accuracy_dt)
print('Precision with CART:', precision_dt)
print('Recall with CART:', recall_dt)
print('F1 with CART:', f1_dt)

## Getting prediction probabilities for each column using Decision Tree classifier
dtc_pred_prob = dtc.predict_proba(X_test)

#print(y_pred_prob)

# Get the labels of each prognosis value
dtc_prognosis_labels = dtc.classes_

# Create a pandas DataFrame to store the predicted probabilities and their labels
pred_dtc = pd.DataFrame(dtc_pred_prob, columns=dtc_prognosis_labels)

display(pred_dtc)

"""## _KNN Algorithm_"""

## Building a predictive model using K Nearest Neighbors
# define the KNN classifier with k=5
knn = KNeighborsClassifier(n_neighbors=5)

# Train the KNN classifier and make predictions on the test set
knn.fit(X_train, y_train)
y_pred5 = knn.predict(X_test)

# Evaluating the performance of the KNN classifier using accuracy score
accuracy_knn = accuracy_score(y_test, y_pred5)
precision_knn = precision_score(y_test, y_pred5,average='weighted')
recall_knn = recall_score(y_test, y_pred5,average='weighted')
f1_knn = f1_score(y_test, y_pred5,average='weighted')

print('Accuracy with KNN:', accuracy_knn)
print('Precision with KNN:', precision_knn)
print('Recall with KNN:', recall_knn)
print('F1 with KNN:', f1_knn)
print('\n')

## Getting prediction probabilities for each column using KNN Classifier
knn_pred_prob = knn.predict_proba(X_test)

#print(y_pred_prob)

# Get the labels of each prognosis value
knn_prognosis_labels = knn.classes_

# Create a pandas DataFrame to store the predicted probabilities and their labels
pred_knn = pd.DataFrame(knn_pred_prob, columns=knn_prognosis_labels)

display(pred_knn)