from google.cloud import aiplatform as vertexai
import os
import dotenv

dotenv.load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
BUCKET_URI = f"gs://{BUCKET_NAME}"
ENDPOINT_DISPLAY_NAME = "fraud_detector_endpoint"

PYTORCH_PREDICTION_FRAUD_URI = (
    "us-docker.pkg.dev/vertex-ai/prediction/pytorch-gpu.1-12:latest"
)
MODEL_DISPLAY_NAME = "fraud_detector"
MODEL_DESCRIPTION = "fraud_detector_2_heads_001_lr_128_hidden"

vertexai.init(
    project="fraud-detection", location="europe-west1", staging_bucket=BUCKET_NAME
)

model = vertexai.Model.upload(
    display_name=MODEL_DISPLAY_NAME,
    description=MODEL_DESCRIPTION,
    serving_container_image_uri=PYTORCH_PREDICTION_FRAUD_URI,
    artifact_uri=BUCKET_URI,
)

endpoint = vertexai.Endpoint.create(display_name=ENDPOINT_DISPLAY_NAME)

model.deploy(
    endpoint=endpoint,
    deployed_model_display_name=MODEL_DISPLAY_NAME,
    machine_type="n1-standard-8",
    accelerator_type="NVIDIA_TESLA_P100",
    accelerator_count=1,
    traffic_percentage=100,
    deploy_request_timeout=1200,
    sync=True,
)
