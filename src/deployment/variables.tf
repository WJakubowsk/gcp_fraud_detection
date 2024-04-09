variable "bucket_name" {
  type = string
  description = "Name of the Google Cloud Storage bucket"
}

variable "project_id" {
  type = string
  description = "ID of the Google Cloud project"
}

variable "project_name" {
  type = string
  description = "Name of the Google Cloud project"
}

variable "region" {
  type = string
  description = "Region for resources"
}

variable "zone" {
  type = string
  description = "Zone for resources"
}

variable "member_1" {
  type = string
  description = "Member 1 for IAM binding"
}

variable "member_2" {
  type = string
  description = "Member 2 for IAM binding"
}

variable "member_3" {
  type = string
  description = "Member 3 for IAM binding"
}

variable "db_instance_name" {
  type = string
  description = "Name of the Google Cloud SQL instance"
}

variable "database_name" {
  type = string
  description = "Name of the Google Cloud SQL database"
}