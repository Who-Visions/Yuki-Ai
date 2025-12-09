# Yuki Cosplay Platform - Enterprise Production Architecture

## 🏗️ **Infrastructure Overview**

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS (NATIONWIDE)                       │
│                     Different Regions / ISPs                     │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CLOUD CDN + LOAD BALANCER                      │
│           (Global distribution, < 50ms latency)                  │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CLOUD RUN (Auto-scale)                      │
│                    yuki-api-production                           │
│         FastAPI Backend - Handles 1000+ concurrent users         │
└──────┬──────────┬───────────┬──────────────┬────────────────────┘
       │          │           │              │
       ▼          ▼           ▼              ▼
   ┌──────┐  ┌────────┐  ┌────────┐  ┌──────────────┐
   │ GCS  │  │BigQuery│  │Cloud   │  │  Gemini API  │
   │Images│  │Analytics│ │ SQL DB │  │  (Vertex AI) │
   └──────┘  └────────┘  └────────┘  └──────────────┘
```

---

## 📦 **GCP Services Used**

### **1. Cloud Run** (Serverless API)
- **Auto-scaling**: 0 to 1000+ instances
- **Region**: us-central1 (Iowa) - lowest latency
- **Multi-region**: Deploy to us-east1, europe-west1, asia-east1 for global coverage
- **Cost**: Pay only for requests
- **URL**: `https://yuki-api-xxxxx.run.app`

### **2. Cloud CDN** (Content Delivery)
- **Global edge locations**: Serve images from nearest POP
- **Cache-Control**: 1 year for generated images
- **Custom domain**: `cdn.yukicosplay.com`
- **SSL**: Auto-provisioned certificates
- **Cost**: ~$0.08/GB egress

### **3. Cloud Storage** (Object Storage)
- **Buckets**:
  - `yuki-user-uploads` - User-uploaded source images
  - `yuki-cosplay-generations` - Generated cosplays
  - `yuki-cdn` - Public CDN-enabled bucket
  - `yuki-knowledge-base` - MD files, guides
  - `yuki-face-schemas` - Face math data
  
- **Lifecycle**: Auto-delete uploads after 30 days
- **Versioning**: Enabled for safety
- **Cost**: $0.02/GB/month

### **4. BigQuery** (Analytics & Search)
- **Datasets**:
  - `yuki_production` - User data, generations
  - `yuki_prompts` - Prompt library
  - `yuki_memory` - Learning system
  - `yuki_analytics` - Usage analytics
  
- **Partitioning**: By date for performance
- **Cost**: $5/TB scanned (very cheap for queries)

### **5. Cloud SQL** (Relational DB)
- **Instance**: MySQL 8.0, High Availability
- **Size**: db-n1-standard-2 (2 vCPU, 7.5GB RAM)
- **Region**: us-central1 with read replica in us-east1
- **Auto-backup**: Daily snapshots
- **Cost**: ~$100/month for HA setup

### **6. Vertex AI** (Gemini Models)
- **Models**:
  - `gemini-3-pro-preview` - Orchestration
  - `gemini-3-pro-image-preview` - Image generation
  - `gemini-2.5-flash` - Fast operations
  
- **Quota**: Request increase for production
- **Cost**: Per-token pricing

### **7. Cloud Armor** (DDoS Protection)
- **WAF rules**: Rate limiting, IP filtering
- **Cost**: ~$50/month base

### **8. Cloud Monitoring** (Observability)
- **Logs**: All Cloud Run logs
- **Metrics**: Latency, errors, usage
- **Alerts**: Email/SMS for downtime
- **Cost**: Included in GCP

---

## 🚀 **Deployment Steps**

### **Prerequisites**
```bash
cd c:\Yuki_Local

# Install dependencies
pip install -r requirements.txt

# Set project
gcloud config set project gifted-cooler-479623-r7
```

### **1. Create Requirements**
```bash
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
google-cloud-storage==2.10.0
google-cloud-bigquery==3.13.0
google-cloud-aiplatform==1.38.0
google-generativeai==0.3.0
pydantic==2.5.0
python-multipart==0.0.6
```

### **2. Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY yuki_api.py .
COPY yuki_memory_system.py .
COPY yuki_cloud_brain.py .

CMD exec uvicorn yuki_api:app --host 0.0.0.0 --port $PORT
```

### **3. Build & Deploy to Cloud Run**
```bash
# Build container
gcloud builds submit --tag gcr.io/gifted-cooler-479623-r7/yuki-api

# Deploy to Cloud Run
gcloud run deploy yuki-api-production \
  --image gcr.io/gifted-cooler-479623-r7/yuki-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --concurrency 80 \
  --min-instances 1 \
  --max-instances 100 \
  --set-env-vars PROJECT_ID=gifted-cooler-479623-r7
```

### **4. Create GCS Buckets**
```bash
# User uploads
gsutil mb -l us-central1 gs://yuki-user-uploads
gsutil iam ch allUsers:objectViewer gs://yuki-user-uploads

# Generations (CDN-enabled)
gsutil mb -l us-central1 gs://yuki-cosplay-generations
gsutil iam ch allUsers:objectViewer gs://yuki-cosplay-generations

# Knowledge base
gsutil mb -l us-central1 gs://yuki-knowledge-base
```

### **5. Setup BigQuery**
```bash
# Create datasets
bq mk --dataset --location=US yuki_production
bq mk --dataset --location=US yuki_prompts
bq mk --dataset --location=US yuki_memory

# Tables will be created automatically by API
```

### **6. Enable Cloud CDN**
```bash
# Create backend bucket
gcloud compute backend-buckets create yuki-cdn-backend \
  --gcs-bucket-name=yuki-cosplay-generations \
  --enable-cdn

# Create URL map
gcloud compute url-maps create yuki-cdn-lb \
  --default-backend-bucket=yuki-cdn-backend

# Create HTTP proxy
gcloud compute target-http-proxies create yuki-cdn-proxy \
  --url-map=yuki-cdn-lb

# Create forwarding rule
gcloud compute forwarding-rules create yuki-cdn-rule \
  --global \
  --target-http-proxy=yuki-cdn-proxy \
  --ports=80
```

### **7. Custom Domain (Optional)**
```bash
# Map custom domain
gcloud run domain-mappings create \
  --service yuki-api-production \
  --domain api.yukicosplay.com \
  --region us-central1
```

---

##  **Architecture Benefits**

✅ **Zero Local Dependencies** - 100% cloud-native  
✅ **Auto-Scaling** - Handle 10 users or 10,000 users  
✅ **Global Distribution** - CDN serves images from nearest edge  
✅ **High Availability** - Multi-region deployment  
✅ **Cost-Efficient** - Pay only for what you use  
✅ **Enterprise Security** - Cloud Armor protection  
✅ **Monitoring** - Real-time metrics and alerts  
✅ **Disaster Recovery** - Auto-backups and versioning  

---

## 💰 **Cost Estimate (Monthly)**

| Service | Usage | Cost |
|---------|-------|------|
| Cloud Run | 1M requests/month | $50 |
| Cloud Storage | 100GB images | $2 |
| BigQuery | 1TB queries | $5 |
| Cloud CDN | 500GB egress | $40 |
| Cloud SQL | HA MySQL | $100 |
| Vertex AI (Gemini) | 10K generations | $200 |
| **Total** | | **~$400/month** |

**Revenue Model**:
- Free tier: 10 generations/month
- Pro: $19.99/month (unlimited)
- Enterprise: Custom pricing

**Break-even**: ~100 paying users

---

## 🔐 **Security**

1. **API Key Authentication** (for frontend)
2. **Rate Limiting** - 100 req/min per user
3. **Cloud Armor** - DDoS protection
4. **IAM Roles** - Least privilege access
5. **VPC Service Controls** - Network isolation
6. **Encryption** - At rest and in transit

---

## 📈 **Monitoring & Analytics**

### **Real-Time Dashboards**
```sql
-- Active users (last 24h)
SELECT COUNT(DISTINCT user_id)
FROM `yuki_production.generations`
WHERE timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)

-- Average processing time
SELECT AVG(processing_time_seconds) as avg_time
FROM `yuki_production.generations`
WHERE status = 'completed'

-- Success rate
SELECT 
  SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) / COUNT(*) * 100 as success_rate
FROM `yuki_production.generations`
```

---

## 🌍 **Multi-Region Deployment**

For global users, deploy to multiple regions:

```bash
# US East
gcloud run deploy yuki-api-useast \
  --image gcr.io/gifted-cooler-479623-r7/yuki-api \
  --region us-east1

# Europe
gcloud run deploy yuki-api-europe \
  --image gcr.io/gifted-cooler-479623-r7/yuki-api \
  --region europe-west1

# Asia
gcloud run deploy yuki-api-asia \
  --image gcr.io/gifted-cooler-479623-r7/yuki-api \
  --region asia-east1
```

Add **Cloud Load Balancing** to route users to nearest region.

---

## 🎯 **Next Steps**

1. ✅ Deploy API to Cloud Run
2. ✅ Setup CDN for image delivery
3. ✅ Initialize BigQuery datasets
4. ☐ Build React frontend
5. ☐ Setup authentication (Firebase Auth)
6. ☐ Add payment processing (Stripe)
7. ☐ Launch MVP to beta users

---

**Built for Scale. Powered by GCP. Ready for Enterprise.**

