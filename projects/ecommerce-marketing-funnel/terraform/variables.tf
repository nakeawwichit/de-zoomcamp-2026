variable "project_id" {
  description = "GCP project id"
  type        = string
}

variable "region" {
  description = "GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "bq_location" {
  description = "BigQuery dataset location"
  type        = string
  default     = "US"
}

variable "bucket_name" {
  description = "GCS bucket name for raw data lake"
  type        = string
}

variable "bq_dataset_staging" {
  description = "BigQuery staging dataset id"
  type        = string
  default     = "ecom_staging"
}

variable "bq_dataset_mart" {
  description = "BigQuery mart dataset id"
  type        = string
  default     = "ecom_mart"
}

variable "service_account_id" {
  description = "Service account id without domain"
  type        = string
  default     = "ecom-funnel-pipeline"
}
