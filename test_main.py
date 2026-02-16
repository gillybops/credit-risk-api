import pytest
from fastapi.testclient import TestClient
from main import app, LoanApplication

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_score_application_high_risk():
    """Test scoring a high-risk application"""
    application = {
        "applicant_income": 20000,
        "loan_amount": 200000,
        "loan_term_months": 360,
        "credit_history_months": 6,
        "employment_status": "unemployed",
        "property_area": "rural",
        "dependents": 4,
        "education": "not_graduate",
        "existing_debt": 15000
    }
    
    response = client.post("/api/v1/score", json=application)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "risk_category" in data
    assert data["risk_category"] == "HIGH"
    assert data["approval_recommendation"] == "DECLINE"

def test_score_application_low_risk():
    """Test scoring a low-risk application"""
    application = {
        "applicant_income": 100000,
        "loan_amount": 150000,
        "loan_term_months": 180,
        "credit_history_months": 96,
        "employment_status": "employed",
        "property_area": "urban",
        "dependents": 1,
        "education": "graduate",
        "existing_debt": 5000
    }
    
    response = client.post("/api/v1/score", json=application)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert data["risk_category"] == "LOW"
    assert data["approval_recommendation"] == "APPROVE"
    assert data["risk_score"] >= 70

def test_score_application_validation():
    """Test input validation"""
    application = {
        "applicant_income": -1000,  # Invalid: negative income
        "loan_amount": 150000,
        "loan_term_months": 360,
        "credit_history_months": 84,
        "employment_status": "employed",
        "property_area": "urban",
        "dependents": 2,
        "education": "graduate",
        "existing_debt": 15000
    }
    
    response = client.post("/api/v1/score", json=application)
    assert response.status_code == 422  # Validation error

def test_model_info():
    """Test model info endpoint"""
    response = client.get("/api/v1/model/info")
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "version" in data
    assert "accuracy" in data
    assert "features" in data

def test_required_features():
    """Test required features endpoint"""
    response = client.get("/api/v1/model/features")
    assert response.status_code == 200
    data = response.json()
    assert "required_features" in data
    assert "example" in data

def test_score_response_structure():
    """Test response structure"""
    application = {
        "applicant_income": 50000,
        "loan_amount": 150000,
        "loan_term_months": 360,
        "credit_history_months": 48,
        "employment_status": "employed",
        "property_area": "suburban",
        "dependents": 2,
        "education": "graduate",
        "existing_debt": 10000
    }
    
    response = client.post("/api/v1/score", json=application)
    assert response.status_code == 200
    data = response.json()
    
    # Check all required fields
    assert "application_id" in data
    assert "risk_score" in data
    assert "risk_category" in data
    assert "approval_recommendation" in data
    assert "confidence" in data
    assert "key_factors" in data
    assert "debt_to_income_ratio" in data
    assert "loan_to_income_ratio" in data
    assert "processed_at" in data
    
    # Check data types
    assert isinstance(data["risk_score"], int)
    assert 0 <= data["risk_score"] <= 100
    assert isinstance(data["confidence"], float)
    assert "positive" in data["key_factors"]
    assert "negative" in data["key_factors"]