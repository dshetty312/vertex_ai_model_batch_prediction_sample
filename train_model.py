from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the prepared data
X_train = pd.read_csv('X_train.csv')
y_train = pd.read_csv('y_train.csv')['Survived']
X_test = pd.read_csv('X_test.csv')
y_test = pd.read_csv('y_test.csv')['Survived']

# Create and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.2f}")

# Save the model
joblib.dump(model, 'titanic_model.joblib')
