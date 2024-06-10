# Model deployment on Google Cloud Platform

### Prerequisities:
* gcloud
* docker


### Deployment

1. Fill the code in with necessary variables (PROJECT_ID, LOCATION etc.)

2. Authenticate to GCP services:
```
gcloud auth login
gcloud set project <YOUR_PROJECT_ID>
gcloud auth configure-docker <YOUR_REGION>-docker.pkg.dev
gcloud services enable artifactregistry.googleapis.com
gcloud artifacts repositories create docker-model-repo \
    --repository-format=docker \
    --location=<YOUR_REGION>

```

3. Build and push docker image to Cloud Container Registry:
```
docker build -t YOUR_REGION-docker.pkg.dev/YOUR_PROJECT_NAME/docker-model-repo/fraud-detector-api .
docker push YOUR_REGION-docker.pkg.dev/YOUR_PROJECT_NAME/docker-model-repo/fraud-detector-api

```

4. Deploy the API container using GCP's GUI (*Cloud Run* -> *Create service* -> select appropriate image, set 8 CPU and 16 GB RAM -> *Create*).

### How to interact with this API?

Model expects **input** to be in the following form:
```
{
    "indices": list
}
```
where *indices* is a list of transaction ids (`txId`), for which the model shall return fraud prediction.

The **output** of the model is in the following form"
```
{
    "predictions": list
}
```
where *predictions* is a list of binary labels predicted for the input transactions of the same length as *indices*.
