variable "bucket_name" {
  description = "Name of the Google Cloud Storage bucket"
  default     = "13245768-bucket-tfstate"
}

variable "project_id" {
  description = "ID of the Google Cloud project"
  default     = "1008128037393"
}

variable "region" {
  description = "Region for resources"
  default     = "europe-west1"
}