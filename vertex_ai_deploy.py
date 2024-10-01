from google.cloud import aiplatform
from google.cloud import storage

# Set your GCP project ID and region
PROJECT_ID = 'your-project-id'
REGION = 'us-central1'
BUCKET_NAME = 'your-bucket-name'
MODEL_DIR = 'models/titanic'
MODEL_NAME = 'titanic_model'

# Upload model to GCS
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob(f"{MODEL_DIR}/{MODEL_NAME}.joblib")
blob.upload_from_filename('titanic_model.joblib')

# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location=REGION)

# Create and deploy model
model = aiplatform.Model.upload(
    display_name=MODEL_NAME,
    artifact_uri=f"gs://{BUCKET_NAME}/{MODEL_DIR}",
    serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-23:latest"
)

endpoint = model.deploy(
    machine_type="n1-standard-2",
)

print(f"Model deployed to endpoint: {endpoint.resource_name}")
