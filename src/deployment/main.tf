terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

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

resource "google_sql_database_instance" "main_db" {
  name             = "fraud-detection-db"
  database_version = "POSTGRES_13"
  region           = "europe-west1"

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_artifact_registry_repository" "docker_model_repo" {
  location      = "europe-west1"
  repository_id = "docker-model-repo"
  format        = "DOCKER"

  docker_config {
    immutable_tags = true
  }
}

resource "google_sql_database" "database" {
  name     = "db_django"
  instance = google_sql_database_instance.main_db.name
}

