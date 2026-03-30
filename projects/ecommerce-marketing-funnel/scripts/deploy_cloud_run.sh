#!/usr/bin/env bash
# Deploy Streamlit dashboard to Google Cloud Run (public URL for peer review / homework).
# Prerequisites: gcloud CLI, Docker (or use Cloud Build via --source), .env with GCP_PROJECT_ID, etc.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

PROJECT="${GCP_PROJECT_ID:?Set GCP_PROJECT_ID in .env}"
REGION="${GCP_REGION:-us-central1}"
SERVICE="${CLOUD_RUN_SERVICE:-ecom-marketing-dashboard}"
MART="${BQ_DATASET_MART:-ecom_mart}"
SA_EMAIL="${CLOUD_RUN_SERVICE_ACCOUNT:-ecom-funnel-pipeline@${PROJECT}.iam.gserviceaccount.com}"

echo "Project: ${PROJECT}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE}"
echo "Service account (BigQuery): ${SA_EMAIL}"

gcloud config set project "${PROJECT}"

gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  --project "${PROJECT}"

gcloud run deploy "${SERVICE}" \
  --quiet \
  --source "${ROOT}/dashboard" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --service-account "${SA_EMAIL}" \
  --set-env-vars "GCP_PROJECT_ID=${PROJECT},BQ_DATASET_MART=${MART}" \
  --memory 1Gi \
  --timeout 300 \
  --max-instances 5 \
  --project "${PROJECT}"

echo ""
echo "Dashboard URL:"
gcloud run services describe "${SERVICE}" \
  --region "${REGION}" \
  --project "${PROJECT}" \
  --format='value(status.url)'
