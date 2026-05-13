# Cardiac Disease Prediction System ❤️

A machine learning-based desktop application developed to predict the likelihood of cardiac disease using patient health parameters. The system uses **Logistic Regression** for prediction and provides an intuitive graphical interface for user interaction, medical suggestions, and prediction history tracking.

---

## 📌 Features

- 🔐 **User Authentication**
  - User Login & Account Creation
  - Credential storage using MySQL

- 🫀 **Cardiac Disease Prediction**
  - Predicts heart disease probability based on medical parameters
  - Uses **Logistic Regression** for classification

- 📊 **Data Preprocessing**
  - Handles missing values using **SimpleImputer**
  - Feature normalization using **StandardScaler**

- 🖥️ **Interactive GUI**
  - Built with **CustomTkinter**
  - Clean and user-friendly interface
  - Progress bar for prediction loading

- 📖 **Health Suggestions**
  - Personalized health suggestions based on deteriorated health metrics
  - Suggestions for:
    - Cholesterol
    - Blood Pressure
    - Smoking habits
    - HDL / LDL levels

- 📜 **Prediction History**
  - Stores previous prediction inputs in a **MySQL database**
  - Allows users to view historical medical records

- ❓ **Built-in Help Section**
  - Explains all medical parameters required for prediction

---

## 🧠 Machine Learning Workflow

### 1. Dataset Loading
The system reads a cardiac disease dataset from a CSV file.

### 2. Data Preprocessing
- Missing values are handled using:
```python
SimpleImputer(strategy="mean")
```

- Features are standardized using:
```python
StandardScaler()
```

### 3. Model Training
The model is trained using:

```python
LogisticRegression(
    solver='lbfgs',
    max_iter=5000,
    class_weight='balanced'
)
```

### 4. Prediction
The model predicts cardiac disease probability using user-provided medical parameters.

---

## 🩺 Input Parameters

The system uses the following health metrics for prediction:

| Parameter | Description |
|------------|-------------|
| Age | Age of the user |
| Sex | Male / Female |
| Total Cholesterol | Total cholesterol level (mg/dL) |
| LDL | Bad cholesterol level |
| HDL | Good cholesterol level |
| Systolic BP | Upper blood pressure reading |
| Diastolic BP | Lower blood pressure reading |
| Smoking | Smoker / Non-Smoker |
| Diabetes | Yes / No |

---

## 🛠️ Tech Stack

### Frontend / GUI
- Python
- CustomTkinter
- Tkinter

### Machine Learning
- Scikit-learn
- Logistic Regression
- StandardScaler
- SimpleImputer

### Database
- MySQL

### Data Processing
- Pandas
- NumPy

### Additional Libraries
- PIL (Pillow)
- Threading

---

## 🗂️ Project Structure

```text
CardiacDiseasePrediction/
│── root.py
│── sampleLearning.py
│── testSample.py
│── heart_disease_Dataset.csv
│── ecgIcon2.ico
│── aboutFile
│── Total Cholesterol
│── LDL
│── HDL
│── Systolic BP
│── Diastolic BP
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vijay-Junoon/cardiac-disease-prediction.git
cd cardiac-disease-prediction
```

### 2. Install dependencies

```bash
pip install customtkinter mysql-connector-python pillow pandas numpy scikit-learn
```

### 3. Configure MySQL Database

Create a MySQL database:

```sql
CREATE DATABASE HeartMonitor;
```

Create required tables:

```sql
CREATE TABLE userCredentials(
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    ContactNumber VARCHAR(20),
    Email VARCHAR(100),
    Username VARCHAR(100),
    Password VARCHAR(100)
);

CREATE TABLE history(
    Username VARCHAR(100),
    age INT,
    sex INT,
    t_chol FLOAT,
    ldl FLOAT,
    hdl FLOAT,
    s_bp FLOAT,
    d_bp FLOAT
);
```

Update database credentials in the code:

```python
mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="HeartMonitor"
)
```

### 4. Run the Application

```bash
python root.py
```

---


## 🚀 Future Improvements

- Improve prediction accuracy with advanced ML models
- Add visual analytics & health charts
- Deploy as a web application
- Add PDF medical report generation
- Improve security with password hashing
- Add doctor recommendation system

---

## 📈 Learning Outcomes

Through this project, I learned:

- Machine Learning model building using **Logistic Regression**
- Data preprocessing with **StandardScaler** and **SimpleImputer**
- GUI development using **CustomTkinter**
- Database integration using **MySQL**
- Multi-threading for smoother UI performance
- End-to-end ML application development

---

## 👨‍💻 Author

**V Vijay**  
GitHub: https://github.com/Vijay-Junoon  
LinkedIn: https://linkedin.com/in/vijay-developer
