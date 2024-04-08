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

# THIS WORKS BUT COMMENTED OUT FOR NOW - VMs + Load Balancer + Autoscaler
# --------------------------------------------------------------------------------------
# resource "google_compute_network" "vpc_network" {
#   name = "vpc-fraud-detection-network"
# }
# resource "google_compute_autoscaler" "autoscaler" {
#   name   = "autoscaler"
#   project = var.project_name
#   zone   = var.zone
#   target = google_compute_instance_group_manager.group_manager.self_link

#   autoscaling_policy {
#     max_replicas    = 4
#     min_replicas    = 2
#     cooldown_period = 60

#     cpu_utilization {
#       target = 0.5
#     }
#   }
# }

# TODO: HERE I THINK WE SHOULD CHANGE SOURCE_IMAGE TO A CUSTOM IMAGE IN THE FUTURE
# resource "google_compute_instance_template" "template" {
#   name           = "instance-template"
#   machine_type   = "e2-micro"
#   can_ip_forward = false
#   project = var.project_name
#   tags = ["allow-lb-service"]

#   disk {
#     source_image = data.google_compute_image.centos_7.self_link
#   }

#   network_interface {
#     network = google_compute_network.vpc_network.name
#   }

#   service_account {
#     scopes = ["userinfo-email", "compute-ro", "storage-ro"]
#   }
# }

# resource "google_compute_target_pool" "target_pool" {
#   name = "fraud-detection-target-pool"
#   project = var.project_name
#   region = var.region
# }

# resource "google_compute_instance_group_manager" "group_manager" {
#   name = "fraud-detection-instance-group-manager"
#   zone = var.zone
#   project = var.project_name
#   version {
#     instance_template  = google_compute_instance_template.template.self_link
#     name               = "primary"
#   }

#   target_pools       = [google_compute_target_pool.target_pool.self_link]
#   base_instance_name = "terraform"
# }

# data "google_compute_image" "centos_7" {
#   family  = "centos-7"
#   project = "centos-cloud"
# }

# module "lb" {
#   source  = "GoogleCloudPlatform/lb/google"
#   version = "2.2.0"
#   region       = var.region
#   name         = "load-balancer"
#   service_port = 80
#   target_tags  = ["fraud-detection-target-pool"]
#   network      = google_compute_network.vpc_network.name
# }
# --------------------------------------------------------------------------------------

# Endpoint for the model
# resource "google_vertex_ai_endpoint" "default" {
#   name = "fraud-detection-endpoint"
#   display_name = "fraud-detection-endpoint"
#   description  = "Vertex AI endpoint for fraud detection model"
#   location     = var.region

#   # TODO: probably need to include network settings here to be accessible from the VMs
# }
# --------------------------------------------------------------------------------------


# TODO: (NEEDS FIX) THIS IS PROBLEMATIC CURRENTLY
# resource "google_sql_database_instance" "instance" {
#   name = var.db_instance_name
#   project = var.project_id
#   database_version = "MYSQL_8_0"
#   region = var.region
#   settings {
#     tier = "db-f1-micro"
#   }
# }
