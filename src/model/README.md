# Model deployment on Google Cloud Platform as Vertex AI endpoint

### Prerequisities:
* Gcloud CLI (with gsutil functionality)
* google-cloud-aiplatform (install through PIP)
* torch-model-archiver

### Deployment

1. Create `.env` file in `model_artifacts/` dir and fill it in with necessary env variables (BUCKET_NAME, PROJECT_ID, LOCATION)
2. Create `.mar` file with model files by running this command in the `/src/model` dir:
```
torch-model-archiver -f 
    --model-name fraud_detector 
    --version 1.2  
    --handler model_artifacts/handler.py 
    --export-path model_artifacts
```

3. Push the model artifacts .mar file to Cloud Storage using the following command (change *STORAGE NAME* accordingly):
```
gsutil cp -r model_artifacts gs://<STORAGE_NAME>
```

4. Run `python deploy.py` script.