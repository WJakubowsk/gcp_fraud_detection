terraform {
    backend "gcs" {
        bucket  = "13245768-bucket-tfstate"
        prefix  = "terraform/state"
    }
}