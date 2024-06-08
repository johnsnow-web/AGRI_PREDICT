import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib

# Load data from CSV
df = pd.read_csv('plant_weather_pesticide_data.csv')

# Combine pesticide_suggestion and pesticide_name into a single target column for training
df['pesticide_combined'] = df['pesticide_suggestion'] + " (" + df['pesticide_name'] + ")"

# Check for NaN values in 'temperature' and 'humidity' columns
if df[['temperature', 'humidity']].isna().any().any():
    print("Dataset contains NaN values. Handling NaNs...")
    df = df.dropna(subset=['temperature', 'humidity'])

X = df[['temperature', 'humidity']]
y = df['pesticide_combined']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating a pipeline with StandardScaler and DecisionTreeClassifier
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', DecisionTreeClassifier())
])

# Fitting the pipeline on the training data
pipeline.fit(X_train, y_train)

# Making predictions on the test data
y_pred = pipeline.predict(X_test)

# Calculating accuracy on the test data
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy on test set:", accuracy)

# Saving the trained model
joblib.dump(pipeline, 'pesticide_model.pkl')

print("Model training completed and saved as pesticide_model.pkl")
