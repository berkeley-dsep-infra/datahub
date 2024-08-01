#!/bin/bash
set -euo pipefail

# Define variables
PROJECT_ID="ucb-datahub-2018" # Replace this with your actual GCP project ID
DEPLOYMENT_NAME="ugr-gke-deployment"
CONFIG_PATH="./configs/gke_ugresearch.yaml"

# Set the GCP project context
gcloud config set project "$PROJECT_ID"

# Navigate to the directory where the deploy.sh script is located
cd "$(dirname "$0")"

# Deploy the configuration
gcloud deployment-manager deployments create "$DEPLOYMENT_NAME" --config "$CONFIG_PATH" || \
gcloud deployment-manager deployments update "$DEPLOYMENT_NAME" --config "$CONFIG_PATH"

# To manually delete the deployment, run the following command:
# gcloud deployment-manager deployments delete "$DEPLOYMENT_NAME"

echo "Deployment process completed."
