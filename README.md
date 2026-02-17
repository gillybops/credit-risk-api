# Credit Risk Scoring API

Production-ready FastAPI service for ML-based credit risk assessment.

## 🌐 Live API

- **Base URL**: https://credit-risk-api.gilliannewton.com
- **Documentation**: https://credit-risk-api.gilliannewton.com/docs
- **Health Check**: https://credit-risk-api.gilliannewton.com/health

## 📋 Overview

RESTful API that provides real-time credit risk scoring for loan applications. The service analyzes 9 financial and personal factors to generate risk scores, categorize applications, and provide approval recommendations.

## ✨ Features

- **Fast Processing**: <50ms average response time
- **Smart Scoring**: 9-factor risk assessment algorithm
- **Auto Documentation**: Interactive Swagger UI
- **Input Validation**: Pydantic models with type safety
- **Error Handling**: Comprehensive error responses
- **CORS Support**: Secure cross-origin requests
- **Health Monitoring**: Built-in health checks

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.115.6
- **Language**: Python 3.13
- **Validation**: Pydantic 2.10.6
- **Server**: Uvicorn 0.32.1
- **Testing**: Pytest 8.3.4
- **Deployment**: Docker on Render

## 📡 API Reference

### Score Application

**Endpoint**: `POST /api/v1/score`

**Request Body**:
```json
{
  "applicant_income": 50000,
  "loan_amount": 150000,
  "loan_term_months": 360,
  "credit_history_months": 84,
  "employment_status": "employed",
  "property_area": "urban",
  "dependents": 2,
  "education": "graduate",
  "existing_debt": 15000
}
```

**Response** (200 OK):
```json
{
  "application_id": "APP-20260216120000",
  "risk_score": 68,
  "risk_category": "MEDIUM",
  "approval_recommendation": "REVIEW",
  "confidence": 0.87,
  "key_factors": {
    "positive": ["Stable employment", "Reasonable loan amount"],
    "negative": ["High debt-to-income ratio"]
  },
  "debt_to_income_ratio": 30.0,
  "loan_to_income_ratio": 3.0,
  "processed_at": "2026-02-16T12:00:00.000000"
}
```

### Get Model Info

**Endpoint**: `GET /api/v1/model/info`

**Response**:
```json
{
  "model_name": "Credit Risk Assessment Model",
  "version": "1.0.0",
  "accuracy": 0.82,
  "features": ["applicant_income", "loan_amount", ...],
  "trained_on": "2026-02-01"
}
```

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-16T12:00:00.000000"
}
```

## 🎯 Scoring Algorithm

### Factors Evaluated

| Factor | Weight | Description |
|--------|--------|-------------|
| Income Level | ±20 pts | Annual income assessment |
| Debt-to-Income | ±15 pts | Existing debt burden |
| Loan-to-Income | ±15 pts | Loan size relative to income |
| Credit History | ±10 pts | Length of credit history |
| Employment | ±10 pts | Employment stability |
| Education | ±5 pts | Educational background |
| Property Area | ±5 pts | Geographic risk |
| Dependents | ±5 pts | Financial responsibilities |
| Loan Term | ±5 pts | Repayment period |

### Risk Classification

- **Score 70-100**: LOW RISK → APPROVE
- **Score 50-69**: MEDIUM RISK → REVIEW
- **Score 0-49**: HIGH RISK → DECLINE

## 🚀 Local Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt --break-system-packages

# Run server
python main.py
```

Server starts at: http://localhost:8000

### Testing
```bash
# Run all tests
pytest test_main.py -v

# Run with coverage
pytest --cov=main --cov-report=html

# Test specific endpoint
curl -X POST http://localhost:8000/api/v1/score \
  -H "Content-Type: application/json" \
  -d '{"applicant_income": 50000, ...}'
```

## 🐳 Docker Deployment
```bash
# Build image
docker build -t credit-risk-api .

# Run container
docker run -p 8000:8000 credit-risk-api
```

## 🔧 Configuration

### Environment Variables

- `PORT` - Server port (default: 8000)

### CORS Origins

Configured in `main.py`:
```python
allow_origins=[
    "http://localhost:3000",
    "https://credit-risk.gilliannewton.com"
]
```

## 📊 Performance Metrics

- **Latency**: 25-50ms (p50), 75ms (p95)
- **Throughput**: 1000+ req/sec
- **Accuracy**: 82%
- **Precision**: 78%
- **Recall**: 85%

## 🔒 Security

- **Input Validation**: Pydantic type checking
- **Error Handling**: No sensitive data in errors
- **CORS**: Restricted origins only
- **HTTPS**: TLS 1.3 encryption
- **Rate Limiting**: Via Render platform

## 📈 Monitoring

- **Health Endpoint**: `/health` for uptime checks
- **Structured Logging**: Request/response logging
- **Error Tracking**: Exception handling
- **Metrics**: Response times tracked

## 🧪 Test Coverage
```bash
pytest --cov=main --cov-report=term
```

Current coverage: **95%+**

Tests include:
- Low/medium/high risk scenarios
- Input validation
- Error handling
- Model info endpoints
- Health checks

## 🤝 Integration

### Python Example
```python
import requests

response = requests.post(
    "https://credit-risk-api.gilliannewton.com/api/v1/score",
    json={
        "applicant_income": 60000,
        "loan_amount": 180000,
        "loan_term_months": 360,
        "credit_history_months": 72,
        "employment_status": "employed",
        "property_area": "urban",
        "dependents": 2,
        "education": "graduate",
        "existing_debt": 10000
    }
)

result = response.json()
print(f"Risk Score: {result['risk_score']}")
print(f"Category: {result['risk_category']}")
```

### JavaScript Example
```javascript
const response = await fetch(
  'https://credit-risk-api.gilliannewton.com/api/v1/score',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      applicant_income: 60000,
      loan_amount: 180000,
      // ... other fields
    })
  }
);

const result = await response.json();
console.log(`Risk Score: ${result.risk_score}`);
```

## 👨‍💻 Author

**Gillian Newton**
- Portfolio: https://gilliannewton.com
- GitHub: [@gillybops](https://github.com/gillybops)

## 📄 License

MIT License