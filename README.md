# Azure Cloud-Native AI Inference API ☁️ 🐳

![Azure](https://img.shields.io/badge/Azure-App%20Service-0078D4?style=for-the-badge&logo=microsoftazure)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker)
![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-009688?style=for-the-badge&logo=fastapi)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

![Demo](demo_screenshot.png)

A production-grade MLOps pipeline that serves a Neural Network for breast cancer detection. The application is containerized using **Docker**, stored in **Azure Container Registry (ACR)**, and deployed to a serverless **Azure Web App for Containers**.

## 🏗️ Architecture
**User (JSON)** -> **Azure App Service (Linux)** -> **Docker Container** -> **FastAPI** -> **Scikit-Learn Model**

## 🚀 Key Engineering Features

### 1. Cloud-Native Deployment (Azure)
- **Infrastructure:** Deployed on Azure App Service (Linux Plan) for horizontal scalability.
- **Registry:** Private images secured in **Azure Container Registry (ACR)**.
- **Security:** Managed Identity and Admin credentials injected via App Service Configuration, ensuring no hardcoded secrets in the codebase.

### 2. Advanced Containerization
- **Multi-Architecture Build:** Implemented `docker buildx` to cross-compile images on Apple Silicon (ARM64) for production Linux servers (AMD64).
- **Optimization:** Used `python:3.9-slim` to reduce image size and attack surface.
- **Port Mapping:** Custom binding to port 80 to adhere to Azure's routing requirements.

### 3. Robust Backend (FastAPI)
- **Strict Validation:** Implemented **Pydantic** models to validate 30+ input features before inference, preventing runtime crashes.
- **Preprocessing Pipeline:** Integrated `StandardScaler` deserialization to ensure production data matches training distribution.
- **Error Handling:** Graceful HTTP 500/422 handling for schema mismatches.

## 🛠️ How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/im-my-tea/azure-mlops-capstone.git
   cd azure-mlops-capstone
   ```

2. **Build the Docker Image**
   ```bash
   docker build -t breast-cancer-api .
   ```

3. **Run Container**
   ```bash
   docker run -p 8000:80 breast-cancer-api
   ```

4. **Access Swagger UI**
   Navigate to `http://localhost:8000/docs` to test the API endpoints.

## ☁️ How to Deploy (Azure CLI)

```bash
# 1. Login to Azure
az login

# 2. Build & Push to ACR (Cross-platform)
docker buildx build --platform linux/amd64 -t <your-registry>.azurecr.io/api:v1 --push .

# 3. Deploy to Web App
az webapp create --resource-group <your-rg> --plan <your-plan> --name <your-app-name> --deployment-container-image-name <your-registry>.azurecr.io/api:v1
```

## 📊 API Usage

**Endpoint:** `POST /predict`

**Payload:**
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