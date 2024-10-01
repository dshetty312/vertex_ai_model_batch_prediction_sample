from google.cloud import aiplatform

# Set your GCP project ID, region, and model details
PROJECT_ID = 'your-project-id'
REGION = 'us-central1'
MODEL_NAME = 'titanic_model'
JOB_NAME = 'titanic_batch_prediction'
INPUT_URI = f"gs://{BUCKET_NAME}/input/batch_predict_input.csv"
OUTPUT_URI = f"gs://{BUCKET_NAME}/output/"

# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location=REGION)

# Get the model resource
model = aiplatform.Model(model_name=MODEL_NAME)

# Create and run batch prediction job
batch_prediction_job = model.batch_predict(
    job_display_name=JOB_NAME,
    gcs_source=INPUT_URI,
    gcs_destination_prefix=OUTPUT_URI,
    sync=False
)

print(f"Batch prediction job created: {batch_prediction_job.resource_name}")
print(f"Job state: {batch_prediction_job.state}")

# Wait for the job to complete
batch_prediction_job.wait()

print(f"Batch prediction job completed with state: {batch_prediction_job.state}")
print(f"Output files can be found in: {OUTPUT_URI}")
