# Azure Cloud-Native AI Inference API ☁️ 🐳

![Azure](https://img.shields.io/badge/Azure-App%20Service-0078D4?style=for-the-badge&logo=microsoftazure)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker)
![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-009688?style=for-the-badge&logo=fastapi)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

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