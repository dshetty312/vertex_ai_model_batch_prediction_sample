import pandas as pd
import numpy as np
from google.cloud import storage
import io

# Set up Google Cloud Storage client
client = storage.Client()
bucket = client.bucket('your-bucket-name')

# Function to read CSV from GCS
def read_csv_from_gcs(blob_name):
    blob = bucket.blob(blob_name)
    content = blob.download_as_text()
    return pd.read_csv(io.StringIO(content))

# Read the original input data
original_data = read_csv_from_gcs('input/batch_predict_input.csv')

# Read the prediction results
predictions = read_csv_from_gcs('output/prediction_results.csv')

# Convert prediction probabilities from string to list of floats
predictions['prediction_probabilities'] = predictions['prediction_probabilities'].apply(eval)

# Extract survival probability
predictions['survival_probability'] = predictions['prediction_probabilities'].apply(lambda x: x[1])

# Combine original data with predictions
combined_data = pd.concat([original_data, predictions], axis=1)

# Perform some analysis

# 1. Overall survival rate
overall_survival_rate = combined_data['predicted_class'].mean()
print(f"Predicted overall survival rate: {overall_survival_rate:.2%}")

# 2. Survival rate by passenger class
survival_by_class = combined_data.groupby('Pclass')['predicted_class'].mean()
print("\nPredicted survival rate by passenger class:")
print(survival_by_class)

# 3. Average survival probability by sex
avg_survival_prob_by_sex = combined_data.groupby('Sex')['survival_probability'].mean()
print("\nAverage survival probability by sex:")
print(avg_survival_prob_by_sex)

# 4. Top 5 passengers with highest survival probability
top_survivors = combined_data.nlargest(5, 'survival_probability')
print("\nTop 5 passengers with highest survival probability:")
print(top_survivors[['Pclass', 'Sex', 'Age', 'Fare', 'survival_probability']])

# 5. Correlation between fare and survival probability
fare_survival_corr = combined_data['Fare'].corr(combined_data['survival_probability'])
print(f"\nCorrelation between fare and survival probability: {fare_survival_corr:.2f}")

# 6. Save the combined data with predictions for further analysis
combined_data.to_csv('titanic_with_predictions.csv', index=False)
print("\nCombined data with predictions saved to 'titanic_with_predictions.csv'")
