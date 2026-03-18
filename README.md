# Breast Cancer Detection API

![GCP](https://img.shields.io/badge/GCP-Cloud%20Run-4285F4?style=for-the-badge&logo=googlecloud)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Live-success?style=for-the-badge)

A production-grade MLOps API serving an MLP Neural Network for breast cancer 
detection. Containerized with Docker, stored in Google Artifact Registry, and 
deployed serverless on GCP Cloud Run.

**Live API:** https://breast-cancer-api-130979666829.us-central1.run.app/docs

---

## Architecture
```
POST /predict
     │
     ▼
GCP Cloud Run (serverless container)
     │
     ▼
FastAPI + Pydantic validation (30 input features)
     │
     ▼
StandardScaler.transform()
     │
     ▼
MLPClassifier.predict() + predict_proba()
     │
     ▼
JSON response: diagnosis + confidence + model_used
```

**Registry:** Google Artifact Registry (`us-central1`)  
**Image:** `us-central1-docker.pkg.dev/ayush-mlops-gcp/mlops-repo/breast-cancer-api:latest`

---

## Migration: Azure → GCP

This project was originally deployed on **Azure App Service (B1 plan)** with 
the image stored in **Azure Container Registry (ACR)**. 

The migration to GCP Cloud Run was a deliberate architectural decision:

| Concern | Azure App Service | GCP Cloud Run |
|---|---|---|
| Compute model | Always-on VM | Scales to zero |
| Idle cost | Yes (24/7 billing) | None |
| Cold start | None | ~2-3 seconds |
| Deployment | App Service Plan + Web App | Single gcloud command |

For a bursty, low-traffic inference API, serverless is the correct model. 
The Docker image is unchanged — only the platform it runs on changed.

The original Azure deployment image is preserved in ACR at 
`ayushmlops101.azurecr.io/breast-cancer-api:v1`.

---

## Key Engineering Decisions

**Serialization chain**  
`train.py` fits `StandardScaler` and trains `MLPClassifier` + 
`LogisticRegression`, serializing all three via `joblib`. Models load once 
at container startup (not per-request) to avoid cold-path latency.

**Known limitation**  
The scaler is fit on the full dataset before train/test split — a data 
leakage issue. This affects reported accuracy but not the serving 
architecture. The fix would be to fit the scaler only on training data 
after the split.

**Column rename in main.py**  
Pydantic field names cannot contain spaces. Three `concave_points_*` 
columns use underscores in the API schema but spaces in the training 
data. A rename map is applied before `scaler.transform()` to reconcile 
this.

**Dependency pinning**  
All direct dependencies are pinned to exact versions. `scikit-learn` is 
pinned to `1.8.0` to match the version used during model training — 
version mismatches cause unpickling warnings and potential silent failures.

**Multi-arch build**  
Built with `--platform linux/amd64` on Apple Silicon (ARM64) to target 
Cloud Run's amd64 runtime.

---

## Run Locally
```bash
git clone https://github.com/im-my-tea/gcp-mlops-capstone.git
cd gcp-mlops-capstone

docker build --platform linux/amd64 -t breast-cancer-api .
docker run -p 8080:8080 breast-cancer-api
```

Open `http://localhost:8080/docs` to test via Swagger UI.

---

## Deploy to GCP Cloud Run
```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# Configure Docker auth
gcloud auth configure-docker us-central1-docker.pkg.dev

# Create registry
gcloud artifacts repositories create mlops-repo \
    --repository-format=docker \
    --location=us-central1

# Build and push
docker build --platform linux/amd64 \
    -t us-central1-docker.pkg.dev/YOUR_PROJECT/mlops-repo/breast-cancer-api:latest .

docker push us-central1-docker.pkg.dev/YOUR_PROJECT/mlops-repo/breast-cancer-api:latest

# Deploy
gcloud run deploy breast-cancer-api \
    --image us-central1-docker.pkg.dev/YOUR_PROJECT/mlops-repo/breast-cancer-api:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1
```

---

## API Usage

**Endpoint:** `POST /predict`
```json
{
  "radius_mean": 20.57,
  "texture_mean": 17.77,
  "perimeter_mean": 132.9,
  "area_mean": 1326,
  "smoothness_mean": 0.08474,
  "compactness_mean": 0.07864,
  "concavity_mean": 0.0869,
  "concave_points_mean": 0.07017,
  "symmetry_mean": 0.1812,
  "fractal_dimension_mean": 0.05667,
  "radius_se": 0.5435,
  "texture_se": 0.7339,
  "perimeter_se": 3.398,
  "area_se": 74.08,
  "smoothness_se": 0.005225,
  "compactness_se": 0.01308,
  "concavity_se": 0.0186,
  "concave_points_se": 0.0134,
  "symmetry_se": 0.01389,
  "fractal_dimension_se": 0.003532,
  "radius_worst": 24.99,
  "texture_worst": 23.41,
  "perimeter_worst": 158.8,
  "area_worst": 1956,
  "smoothness_worst": 0.1238,
  "compactness_worst": 0.1866,
  "concavity_worst": 0.2416,
  "concave_points_worst": 0.186,
  "symmetry_worst": 0.275,
  "fractal_dimension_worst": 0.08902
}
```

**Response:**
```json
{
  "diagnosis": "Malignant",
  "confidence": "99.8%",
  "model_used": "MLP Neural Network"
}
```