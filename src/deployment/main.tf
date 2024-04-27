terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

# Bucket for terraform state
resource "google_storage_bucket" "default" {
  name          = var.bucket_name
  force_destroy = false
  location      = var.region
  storage_class = "STANDARD"
  versioning {
    enabled = true
  }

  depends_on = [
    google_project_iam_binding.default
  ]
}

resource "google_project_iam_binding" "default" {
  project = var.project_id
  role    = "roles/storage.admin"
  members = [
    var.member_1,
    var.member_2,
    var.member_3
  ]
}

# Cloud Run
#resource "google_cloud_run_v2_service" "default" {
#  name     = "cloudrun-service"
#  location = var.region
#  ingress = "INGRESS_TRAFFIC_ALL"
#
#  template {
#    containers {
#      image = "us-docker.pkg.dev/cloudrun/container/hello"
#    }
#  }
#}
#
## Endpoint for the model
#resource "google_vertex_ai_endpoint" "default" {
#  name = "fraud-detection-endpoint"
#  display_name = "fraud-detection-endpoint"
#  description  = "Vertex AI endpoint for fraud detection model"
#  location     = var.region
#
#  # TODO: probably need to include network settings here to be accessible from the VMs
#}
#
## Spanner instance
#resource "google_spanner_instance" "default" {
#  name          = "fraud-detection-spanner"
#  config        = "regional-europe-west1"
#  display_name  = "fraud-detection-spanner"
#  num_nodes     = 1
#  project       = var.project_name
#}