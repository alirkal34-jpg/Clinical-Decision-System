# ❤️ Clinical Decision Support System - Cardiovascular Risk Assessment

![Docker](https://img.shields.io/badge/Container-Docker-blue?logo=docker&logoColor=white) 
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?logo=streamlit&logoColor=white) 
![Python](https://img.shields.io/badge/Language-Python_3.9-yellow?logo=python&logoColor=white) 
![Status](https://img.shields.io/badge/Deployment-Ready-success)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> A containerized **Clinical Decision Support System (CDSS)** engineered to predict cardiovascular health metrics in real-time, built with **Streamlit** and deployed via **Docker**.

## 📋 Table of Contents
- [Overview](#overview)
- [The Engineering Context](#the-engineering-context)
- [Features](#features)
- [Screenshots](#screenshots)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Risk Calculation Model](#risk-calculation-model)
- [Docker Deployment](#docker-deployment)
- [Dataset](#dataset)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🎯 Overview

This **Clinical Decision Support System (CDSS)** provides real-time cardiovascular risk assessment for healthcare professionals. The system processes patient vitals (age, BMI, blood pressure) and generates instant risk predictions with actionable insights.

### Key Highlights
✅ **70,000+ Patient Records** analyzed from cardiovascular disease dataset  
✅ **Real-time Risk Prediction** with interactive gauge visualization  
✅ **Dockerized Architecture** ensuring reproducible deployment  
✅ **Advanced Risk Model** with feature-weighted scoring  
✅ **Clinical-Grade UI** designed for medical professionals  

---

## 🩺 The Engineering Context

In healthcare informatics, **reproducibility and isolation are critical**. "It works on my machine" is not acceptable when dealing with medical algorithms.

This project solves dependency hell by fully **containerizing the application environment**, ensuring that the risk calculation model runs identically on any server, laptop, or cloud instance.

### Why Docker?
- ✅ **Consistent Environment**: Same runtime on dev, staging, and production
- ✅ **Dependency Isolation**: No conflicts with host system packages
- ✅ **Easy Deployment**: Single command deployment to any infrastructure
- ✅ **Scalability**: Ready for Kubernetes orchestration

---

## ⚡ Features

### 🏥 Clinical Features
- **Real-time Risk Assessment**: Instant cardiovascular risk calculation (0-100%)
- **Multi-Factor Analysis**: BMI, blood pressure, age, gender, lifestyle factors
- **Risk Categorization**: LOW (<30%), MODERATE (30-60%), HIGH (>60%)
- **Actionable Recommendations**: Personalized health advice based on risk profile
- **Visual Risk Indicators**: Color-coded gauge charts for quick interpretation

### 🛠 Technical Features
- **Dockerized Architecture**: Fully isolated runtime environment
- **Interactive Dashboard**: Built with Streamlit for real-time interaction
- **Data Visualization**: Correlation heatmaps, risk distribution charts
- **Reproducible Environment**: `.devcontainer` configuration for standardized development
- **Scalable Design**: Ready for production deployment

### 📊 Data Insights
- **70,000+ Patient Records**: Comprehensive cardiovascular disease dataset
- **Feature Correlation Analysis**: Identifies key risk factors
- **Statistical Validation**: Evidence-based risk scoring model

---

## 📸 Screenshots

### Low Risk Patient (17% - HEALTHY)
<img width="1579" height="811" alt="image" src="https://github.com/user-attachments/assets/b93757a6-34fb-48a7-aac9-b922206de9a7" />



*Patient: Age 30, BMI 22.5, BP 132/79 - Normal cardiovascular health*

### High Risk Patient (67% - CRITICAL)
<img width="1575" height="811" alt="image" src="https://github.com/user-attachments/assets/f2b98403-cb6f-45a9-8fbc-644fb0100413" />



*Patient: Age 50, BMI 22.5, BP 218/79 - Elevated blood pressure indicating high risk*

### Clinical Risk Weights (ESC/AHA Guidelines)
<img width="1576" height="879" alt="image" src="https://github.com/user-attachments/assets/e5cdda0b-fc7c-4d95-89ba-b8b500a8ab81" />


*Evidence-based risk factor contributions based on clinical guidelines*

### Technical Risk Model Details

<img width="1433" height="831" alt="image" src="https://github.com/user-attachments/assets/a7a867de-2b2a-4cb4-a0ad-f9f8d649435d" />

*Advanced risk calculation model with weighted features and clinical thresholds*

---

## 🛠 Technology Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit 1.24+ |
| **Backend** | Python 3.9+ |
| **Containerization** | Docker, Docker Compose |
| **Data Processing** | pandas, numpy |
| **Visualization** | plotly, matplotlib, seaborn |
| **Development** | VS Code DevContainers |

### Core Dependencies
```txt
streamlit>=1.24.0
pandas>=1.5.0
numpy>=1.23.0
plotly>=5.14.0
scikit-learn>=1.2.0
```

---

## 📁 Project Structure

```
Clinical-Decision-System/
│
├── Clinical-Decision-System-main/
│   ├── cardio-dashboard/
│   │   ├── app.py                      # Main Streamlit application
│   │   ├── risk_model.py               # Risk calculation engine
│   │   ├── data/
│   │   │   └── cardio_train.csv        # 70,000+ patient records
│   │   ├── models/
│   │   │   └── risk_calculator.pkl     # Trained risk model
│   │   └── utils/
│   │       ├── visualization.py        # Chart generation
│   │       └── preprocessing.py        # Data processing utilities
│   │
│   ├── .devcontainer/
│   │   └── devcontainer.json           # VS Code container config
│   │
│   └── requirements.txt                # Python dependencies
│
├── Dockerfile                          # Multi-stage Docker build
├── docker-compose.yml                  # Container orchestration
├── .gitignore                          # Git ignore rules
├── LICENSE                             # MIT License
└── README.md                           # This file
```

---

## 🚀 Installation

### Prerequisites
- **Docker Desktop** (or Docker Engine + Docker Compose)
- **Git** (for cloning)
- **4GB RAM** minimum
- **2GB disk space**

### Option 1: Docker Deployment (Recommended)

#### Step 1: Clone the Repository
```bash
git clone https://github.com/alirkal34-jpg/Clinical-Decision-System.git
cd Clinical-Decision-System/Clinical-Decision-System-main
```

#### Step 2: Build Docker Image
```bash
docker build -t cardio-cdss:latest .
```

#### Step 3: Run Container
```bash
docker run -p 8501:8501 cardio-cdss:latest
```

#### Step 4: Access Dashboard
Open browser: **http://localhost:8501**

### Option 2: Docker Compose (For Multi-Service Setup)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: Local Development (Without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd Clinical-Decision-System-main
pip install -r requirements.txt

# Run Streamlit app
cd cardio-dashboard
streamlit run app.py
```

---

## 💻 Usage

### Basic Workflow

1. **Launch the Dashboard**
   ```bash
   docker run -p 8501:8501 cardio-cdss:latest
   ```

2. **Access Web Interface**
   - Navigate to: `http://localhost:8501`
   - Dashboard loads automatically

3. **Input Patient Data**
   - **Demographics**: Age, Gender
   - **Clinical Vitals**: 
     - BMI (Body Mass Index)
     - Systolic Blood Pressure (mmHg)
     - Diastolic Blood Pressure (mmHg)
   - **Lifestyle Factors**: Smoking, Alcohol, Physical Activity

4. **View Risk Assessment**
   - **Risk Score**: 0-100% cardiovascular disease probability
   - **Risk Level**: LOW / MODERATE / HIGH / CRITICAL
   - **Visual Gauge**: Color-coded risk indicator
   - **Recommendations**: Personalized health advice

5. **Analyze Data**
   - View correlation heatmaps
   - Explore risk distribution charts
   - Compare patient against dataset statistics

### Example Use Cases

#### Case 1: Low Risk Patient
```
Input:
- Age: 30
- BMI: 22.5 (Normal)
- BP: 132/79 (Borderline)
- Smoking: No
- Exercise: Regular

Output:
- Risk Score: 17%
- Level: HEALTHY (Low Risk)
- Recommendation: Continue healthy habits
```

#### Case 2: High Risk Patient
```
Input:
- Age: 50
- BMI: 22.5 (Normal)
- BP: 218/79 (Stage 3 Hypertension)
- Smoking: Yes
- Exercise: Sedentary

Output:
- Risk Score: 67%
- Level: CRITICAL (Urgent)
- Recommendation: Immediate medical intervention
```

---

## 🔬 Risk Calculation Model

### Evidence-Based Scoring Algorithm

The system implements **ESC/AHA (European Society of Cardiology / American Heart Association)** clinical guidelines for cardiovascular risk assessment.

#### Clinical Risk Weights

| Risk Factor | Weight | Clinical Threshold |
|------------|--------|-------------------|
| **Age > 60** | +25% | Leading demographic factor |
| **Hypertension Stage 3** | +22% | BP >180/110 mmHg |
| **Smoking** | +20% | Leading preventable cause |
| **Very High Cholesterol** | +18% | Severe dyslipidemia |
| **Very High Glucose** | +16% | Diabetes indicator |
| **Obesity** | +15% | BMI ≥ 30 kg/m² |
| **Physical Inactivity** | +12% | Sedentary lifestyle |
| **Alcohol Use** | +10% | Regular consumption |

#### Model Improvements
1. ✅ **Lifestyle factors** (smoking, alcohol, exercise) now properly weighted
2. ✅ **Obesity penalized** by 15% to reflect cardiovascular strain
3. ✅ **BMI capped at 95%** to avoid unrealistic predictions
4. ✅ **Age-delayed effects** for patients over 60
5. ✅ **Blood pressure staging** aligned with AHA guidelines

#### Risk Level Classification
| Risk Score | Category | Color | Recommendation |
|-----------|----------|-------|----------------|
| **0-30%** | LOW | 🟢 Green | Routine check-ups recommended |
| **30-50%** | MODERATE | 🟡 Yellow | Lifestyle changes needed |
| **50-70%** | HIGH | 🟠 Orange | Medical intervention advised |
| **70-100%** | CRITICAL | 🔴 Red | Urgent cardiology referral |

---

## 🐳 Docker Deployment

### Dockerfile Overview
```dockerfile
# Multi-stage build for optimized image size
FROM python:3.9-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY Clinical-Decision-System-main/cardio-dashboard/ /app/
WORKDIR /app

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Start application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose Configuration
```yaml
version: '3.8'

services:
  cdss-dashboard:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./Clinical-Decision-System-main/cardio-dashboard/data:/app/data
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_PORT=8501
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Production Deployment

#### AWS ECS
```bash
# Build and push to ECR
docker tag cardio-cdss:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/cardio-cdss:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/cardio-cdss:latest

# Deploy to ECS
aws ecs update-service --cluster cdss-cluster --service cdss-service --force-new-deployment
```

#### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cardio-cdss
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cardio-cdss
  template:
    metadata:
      labels:
        app: cardio-cdss
    spec:
      containers:
      - name: streamlit
        image: cardio-cdss:latest
        ports:
        - containerPort: 8501
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

---

## 📊 Dataset

### Cardiovascular Disease Dataset

**Source**: Kaggle Cardiovascular Disease Dataset  
**Records**: 70,000 patients  
**Features**: 12 clinical and lifestyle variables  

#### Feature Description

| Feature | Type | Description | Range/Values |
|---------|------|-------------|--------------|
| **age** | Integer | Patient age (days) | 10,950 - 25,000 days |
| **gender** | Binary | 1 = Female, 2 = Male | {1, 2} |
| **height** | Integer | Height in cm | 55 - 250 cm |
| **weight** | Float | Weight in kg | 10 - 200 kg |
| **ap_hi** | Integer | Systolic BP | 0 - 200 mmHg |
| **ap_lo** | Integer | Diastolic BP | 0 - 150 mmHg |
| **cholesterol** | Categorical | 1=Normal, 2=Above, 3=High | {1, 2, 3} |
| **gluc** | Categorical | 1=Normal, 2=Above, 3=High | {1, 2, 3} |
| **smoke** | Binary | 0=No, 1=Yes | {0, 1} |
| **alco** | Binary | Alcohol intake | {0, 1} |
| **active** | Binary | Physical activity | {0, 1} |
| **cardio** | Binary | **Target**: CVD presence | {0, 1} |

#### Dataset Statistics
- **Prevalence**: ~50% cardiovascular disease
- **Age Range**: 30-65 years (converted from days)
- **Gender Distribution**: ~65% Female, 35% Male
- **Data Quality**: Pre-cleaned, no missing values

#### Data Preprocessing
```python
# BMI Calculation
df['bmi'] = df['weight'] / (df['height'] / 100) ** 2

# Age Conversion
df['age_years'] = df['age'] / 365

# Outlier Removal
df = df[(df['ap_hi'] > 0) & (df['ap_hi'] < 250)]
df = df[(df['ap_lo'] > 0) & (df['ap_lo'] < 200)]
```

---

## 🔮 Future Improvements

### Short-term Goals
- [ ] **ML Model Integration**: Replace rule-based scoring with Random Forest/XGBoost
- [ ] **User Authentication**: Add login system for multi-user support
- [ ] **PDF Report Generation**: Export patient risk assessments
- [ ] **API Endpoint**: RESTful API for external integrations
- [ ] **Database Integration**: PostgreSQL for patient history tracking

### Long-term Goals
- [ ] **Multi-Language Support**: Spanish, French, Arabic translations
- [ ] **Mobile App**: Flutter/React Native companion app
- [ ] **FHIR Integration**: HL7 FHIR standard compliance
- [ ] **AI Explainability**: SHAP values for model interpretability
- [ ] **Federated Learning**: Privacy-preserving multi-hospital training

### Research Directions
- [ ] **ECG Integration**: Analyze electrocardiogram data
- [ ] **Time-Series Prediction**: Forecast risk progression over time
- [ ] **Multi-Modal Learning**: Combine vitals + imaging + genomics

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute
1. 🐛 **Report bugs** via GitHub Issues
2. 💡 **Suggest features** or improvements
3. 📖 **Improve documentation**
4. 🔧 **Submit pull requests**

### Development Process
```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/AmazingFeature

# 3. Commit your changes
git commit -m 'Add some AmazingFeature'

# 4. Push to the branch
git push origin feature/AmazingFeature

# 5. Open a Pull Request
```

### Code Style
- Follow **PEP 8** guidelines
- Add **docstrings** to functions
- Write **unit tests** for new features
- Update **documentation**

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Ali Rubar Kal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
aUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
tHE SOFTWARE.
```

---

## 📧 Contact

**Ali Rubar Kal**  
GitHub: [@alirkal34-jpg](https://github.com/alirkal34-jpg)  
Project Link: [Clinical-Decision-System](https://github.com/alirkal34-jpg/Clinical-Decision-System)

---

## 🙏 Acknowledgments

- **Kaggle Cardiovascular Disease Dataset** for providing high-quality medical data
- **Streamlit** community for excellent documentation and support
- **Docker** for revolutionizing application deployment
- **Healthcare professionals** who provided clinical validation
- **ESC/AHA** for evidence-based cardiovascular risk guidelines

---

## 📚 References

1. [Kaggle Cardiovascular Disease Dataset](https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset)
2. [American Heart Association - Blood Pressure Guidelines](https://www.heart.org/en/health-topics/high-blood-pressure)
3. [ESC Guidelines on Cardiovascular Disease Prevention](https://www.escardio.org/)
4. [WHO - Cardiovascular Diseases (CVDs)](https://www.who.int/health-topics/cardiovascular-diseases)
5. [Streamlit Documentation](https://docs.streamlit.io/)
6. [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

<div align="center">

**Made with ❤️ for Healthcare Innovation**

[Report Bug](https://github.com/alirkal34-jpg/Clinical-Decision-System/issues) · [Request Feature](https://github.com/alirkal34-jpg/Clinical-Decision-System/issues) · [View Screenshots](#screenshots)

⭐ **Star this repo if you find it useful!** ⭐

</div>
