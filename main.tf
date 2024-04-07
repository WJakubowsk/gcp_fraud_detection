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