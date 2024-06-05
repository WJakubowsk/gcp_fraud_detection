# Model deployment on Google Cloud Platform

### Prerequisities:
* gcloud
* docker


### Deployment

1. Create `.env` file in `model_artifacts/` dir and fill it in with necessary env variables (BUCKET_NAME, PROJECT_ID, LOCATION)
<!-- 2. Create `.mar` file with model files by running this command in the `/src/model` dir:
```
torch-model-archiver -f \
    --model-name model \
    --version 1.0 \
    --handler model_artifacts/handler.py \
    --extra-files model_weights.pth,gnn.py \
    --export-path model_artifacts
``` -->
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

<!-- 
4. Run `python deploy.py` script. -->

4. Deploy the API container using GCP's GUI (*Cloud Run* -> *Create service* -> select appropriate image, set 8 CPU and 16 GB RAM -> *Create*).

### How to interact with this API?

Model expects **input** to be in the following form:
```
{
    "input_data": {
    "features": dict,
    "edges": dict
    }
}
```
where *features* and *edges* are dict to be transformed into pandas DataFrame. Simply put, you need to convert your input dataframes into dict form using `to_dict()` method and pass as above.


The **output** of the model is in the following form"
```
{
    "predictions": list
}
```
where *predictions* is a list of binary labels predicted for the input transactions of the same length as number of observations in the *features* DataFrame.