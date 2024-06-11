terraform {
    backend "gcs" {
        bucket  = "bucket-tfstate-fraud-detection"
        prefix  = "terraform/state"
    }
}