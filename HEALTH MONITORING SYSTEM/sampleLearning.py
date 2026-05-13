import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Loading dataset
genDataset = pd.read_csv("heart_disease_Dataset.csv")

# Creating feature and target matrices
genX = genDataset.iloc[:, :-1].values  # Features
genY = genDataset.iloc[:, -1].values   # Target

# Handling missing data
genImputer = SimpleImputer(missing_values=np.nan, strategy="mean")
genX = genImputer.fit_transform(genX)

# Splitting the dataset
genX_train, genX_test, genY_train, genY_test = train_test_split(genX, genY, test_size=0.25, stratify=genY, random_state=1)

# Feature Scaling
scaler = StandardScaler()
genX_train_scaled = scaler.fit_transform(genX_train)
genX_test_scaled = scaler.transform(genX_test)

# Creating and training the logistic regression model
genModel = LogisticRegression(solver='lbfgs', max_iter=5000, class_weight='balanced')
genModel.fit(genX_train_scaled, genY_train)

# Predictions on test data
genY_test_prediction = genModel.predict(genX_test_scaled)

# Accuracy calculation
print("Accuracy on test data:", accuracy_score(genY_test, genY_test_prediction))

# Classification Report
#print("\nClassification Report:\n", classification_report(genY_test, genY_test_prediction))

# Confusion Matrix
"""cm = confusion_matrix(genY_test, genY_test_prediction)
sns.heatmap(cm, annot=True, fmt='d', cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()"""

# Predicting for a new input
input_data = (63, 1, 260.0, 170.0, 35.0, 152.0, 96.0, 1, 1)
input_data_array = np.asarray(input_data).reshape(1, -1)  # Reshape to 2D

# Scaling the new input data using the previously fitted scaler
input_data_scaled = scaler.transform(input_data_array)

# Making a prediction
prediction = genModel.predict(input_data_scaled)
print("Predicted class for the new input:", prediction[0])
