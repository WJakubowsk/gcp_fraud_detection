# GCP Fraud Detection

## Overview

This project focuses on developing a machine learning pipeline for detecting fraudulent transactions using Graph Neural Networks (GNN) and deploying the solution on Google Cloud Platform (GCP).

## Features

![Diagram architecture](architecture.svg)

- **Graph Neural Networks (GNN):** Utilizes advanced GNN models to analyze transaction data and detect potential fraud.
- **Google Cloud Platform Deployment:** Implements the machine learning pipeline on GCP for scalability and efficiency.
- **Data Handling:** Processes and manages transaction data for training and inference.
- **Web Application:** Presents in esthetic manner all key findings of model using user-friendly web interface with React and Django components.

## Project Structure

- **data/**: Contains datasets used for training and evaluation.
- **src/**: Source code for data preprocessing, model training, and deployment scripts:
    - **app/**: Code for the app, including:
        - *frontend/*: files related to React frontend, together with CSS files for esthetics and frontend deployment as web UI gate to app.
        - *backend/*: files related to Django backend component of the application, along with models for data and views for website and cloud deployment.
    - **deployment/**: files related to deployment of Google Cloud Components using Terraform.
    - **model/**: files related to GNN model comprising data engineering, machine learning and MLOps.
- **.github/**: Workflow configurations for CI/CD.

## Technologies

- Frontend: React, Vite,
- Backend: Django, Uvicorn,
- ML: PyTorch, Flask,
- Infra: Docker, Terraform,
- Cloud: GCP Cloud Run, Cloud SQL, Artifact Registry.

## Usage

1. Prepare your dataset and place it in the `data/` directory.
2. Deploy infrastructure using Terraform and `deployment/` files. 
3. Train the model:
   ```sh
   python src/model/train.py
   ```
4. Deploy the model to GCP - follow guidelines of README in the **model/** subdirectory.

## Contributors

- Julia Przybytniowska (Frontend)
- Mikołaj Gałkowski (Backend)
- Wiktor Jakubowski (ML)
