#!/bin/bash

# Yuki Cosplay Platform - Complete Deployment Script
# Deploys entire enterprise infrastructure to GCP

set -e  # Exit on error

PROJECT_ID="gifted-cooler-479623-r7"
REGION="us-central1"
SERVICE_NAME="yuki-api-production"

echo "🚀 Deploying Yuki Cosplay Platform to GCP..."
echo "   Project: $PROJECT_ID"
echo "   Region: $REGION"
echo ""

# =============================================================================
# 1. ENABLE REQUIRED APIS
# =============================================================================
echo "📋 Step 1: Enabling required GCP APIs..."

gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  storage.googleapis.com \
  bigquery.googleapis.com \
  sqladmin.googleapis.com \
  aiplatform.googleapis.com \
  compute.googleapis.com \
  --project=$PROJECT_ID

echo "✅ APIs enabled"
echo ""

# =============================================================================
# 2. CREATE GCS BUCKETS
# =============================================================================
echo "📦 Step 2: Creating GCS buckets..."

# User uploads
gsutil mb -l $REGION -p $PROJECT_ID gs://yuki-user-uploads 2>/dev/null || echo "  Bucket yuki-user-uploads already exists"
gsutil iam ch allUsers:objectViewer gs://yuki-user-uploads

# Generations
gsutil mb -l $REGION -p $PROJECT_ID gs://yuki-cosplay-generations 2>/dev/null || echo "  Bucket yuki-cosplay-generations already exists"
gsutil iam ch allUsers:objectViewer gs://yuki-cosplay-generations

# CDN bucket
gsutil mb -l $REGION -p $PROJECT_ID gs://yuki-cdn 2>/dev/null || echo "  Bucket yuki-cdn already exists"
gsutil iam ch allUsers:objectViewer gs://yuki-cdn

# Knowledge base
gsutil mb -l $REGION -p $PROJECT_ID gs://yuki-knowledge-base 2>/dev/null || echo "  Bucket yuki-knowledge-base already exists"

# Face schemas
gsutil mb -l $REGION -p $PROJECT_ID gs://yuki-face-schemas 2>/dev/null || echo "  Bucket yuki-face-schemas already exists"

echo "✅ GCS buckets ready"
echo ""

# =============================================================================
# 3. CREATE BIGQUERY DATASETS
# =============================================================================
echo "📊 Step 3: Creating BigQuery datasets..."

bq mk --dataset --location=US --project_id=$PROJECT_ID yuki_production 2>/dev/null || echo "  Dataset yuki_production already exists"
bq mk --dataset --location=US --project_id=$PROJECT_ID yuki_prompts 2>/dev/null || echo "  Dataset yuki_prompts already exists"
bq mk --dataset --location=US --project_id=$PROJECT_ID yuki_memory 2>/dev/null || echo "  Dataset yuki_memory already exists"
bq mk --dataset --location=US --project_id=$PROJECT_ID yuki_analytics 2>/dev/null || echo "  Dataset yuki_analytics already exists"

echo "✅ BigQuery datasets ready"
echo ""

# =============================================================================
# 4. BUILD CONTAINER IMAGE
# =============================================================================
echo "🔨 Step 4: Building container image..."

gcloud builds submit --tag gcr.io/$PROJECT_ID/yuki-api --project=$PROJECT_ID

echo "✅ Container image built"
echo ""

# =============================================================================
# 5. DEPLOY TO CLOUD RUN
# =============================================================================
echo "🚢 Step 5: Deploying to Cloud Run..."

gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/yuki-api \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --concurrency 80 \
  --min-instances 1 \
  --max-instances 100 \
  --set-env-vars PROJECT_ID=$PROJECT_ID,REGION=$REGION \
  --project=$PROJECT_ID

echo "✅ Cloud Run service deployed"
echo ""

# =============================================================================
# 6. GET SERVICE URL
# =============================================================================
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
  --region $REGION \
  --project=$PROJECT_ID \
  --format='value(status.url)')

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ DEPLOYMENT COMPLETE!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🌐 API URL: $SERVICE_URL"
echo ""
echo "📌 Endpoints:"
echo "   Health Check:    $SERVICE_URL/"
echo "   Upload Image:    $SERVICE_URL/api/v1/upload"
echo "   Generate:        $SERVICE_URL/api/v1/generate"
echo "   Check Status:    $SERVICE_URL/api/v1/status/{id}"
echo "   Search Prompts:  $SERVICE_URL/api/v1/prompts/search"
echo "   Analytics:       $SERVICE_URL/api/v1/analytics/stats"
echo ""
echo "🔗 Cloud Console:"
echo "   Cloud Run:    https://console.cloud.google.com/run?project=$PROJECT_ID"
echo "   Cloud Storage: https://console.cloud.google.com/storage/browser?project=$PROJECT_ID"
echo "   BigQuery:     https://console.cloud.google.com/bigquery?project=$PROJECT_ID"
echo ""
echo "💡 Next Steps:"
echo "   1. Initialize prompt database:  python prompt_database.py"
echo "   2. Initialize memory system:    python yuki_memory_system.py"
echo "   3. Test API:                    curl $SERVICE_URL/"
echo ""
echo "═══════════════════════════════════════════════════════════════"
