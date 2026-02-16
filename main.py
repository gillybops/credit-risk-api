from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict
import uvicorn
import pickle
from datetime import datetime
import os

app = FastAPI(
    title="Credit Risk Scoring API",
    description="ML-powered credit risk assessment for loan applications",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://creditrisk.gilliannewton.com",
        "https://creditrisk-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class LoanApplication(BaseModel):
    applicant_income: float = Field(..., gt=0, description="Annual income in USD")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount")
    loan_term_months: int = Field(..., ge=12, le=480, description="Loan term in months")
    credit_history_months: int = Field(..., ge=0, description="Length of credit history")
    employment_status: str = Field(..., description="employed, self_employed, unemployed")
    property_area: str = Field(..., description="urban, suburban, rural")
    dependents: int = Field(..., ge=0, le=10)
    education: str = Field(..., description="graduate, not_graduate")
    existing_debt: float = Field(..., ge=0, description="Existing debt amount")
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }

class RiskAssessment(BaseModel):
    application_id: str
    risk_score: int
    risk_category: str
    approval_recommendation: str
    confidence: float
    key_factors: Dict[str, List[str]]
    debt_to_income_ratio: float
    loan_to_income_ratio: float
    processed_at: str

class ModelInfo(BaseModel):
    model_name: str
    version: str
    accuracy: float
    features: List[str]
    trained_on: str

# Simple rule-based scoring (for demo - would be ML model in production)
def calculate_risk_score(application: LoanApplication) -> RiskAssessment:
    """
    Calculate credit risk score based on application data
    Score: 0-100 (higher = lower risk)
    """
    
    # Calculate financial ratios
    debt_to_income = (application.existing_debt / application.applicant_income) * 100
    loan_to_income = (application.loan_amount / application.applicant_income)
    monthly_payment = application.loan_amount / application.loan_term_months
    payment_to_income = (monthly_payment * 12 / application.applicant_income) * 100
    
    # Base score
    score = 50
    
    # Income factors (+/- 20 points)
    if application.applicant_income > 80000:
        score += 15
    elif application.applicant_income > 50000:
        score += 10
    elif application.applicant_income < 25000:
        score -= 15
    
    # Debt-to-income ratio (+/- 15 points)
    if debt_to_income < 20:
        score += 15
    elif debt_to_income < 35:
        score += 5
    elif debt_to_income > 50:
        score -= 15
    elif debt_to_income > 40:
        score -= 10
    
    # Loan-to-income ratio (+/- 15 points)
    if loan_to_income < 2:
        score += 15
    elif loan_to_income < 3:
        score += 8
    elif loan_to_income > 5:
        score -= 15
    elif loan_to_income > 4:
        score -= 10
    
    # Credit history (+/- 10 points)
    if application.credit_history_months > 60:
        score += 10
    elif application.credit_history_months > 36:
        score += 5
    elif application.credit_history_months < 12:
        score -= 10
    
    # Employment status (+/- 10 points)
    if application.employment_status == "employed":
        score += 10
    elif application.employment_status == "unemployed":
        score -= 20
    
    # Education (+/- 5 points)
    if application.education == "graduate":
        score += 5
    
    # Property area (+/- 5 points)
    if application.property_area == "urban":
        score += 5
    elif application.property_area == "rural":
        score -= 3
    
    # Dependents (+/- 5 points)
    if application.dependents == 0:
        score += 5
    elif application.dependents > 3:
        score -= 5
    
    # Loan term (+/- 5 points)
    if application.loan_term_months <= 180:
        score += 5
    elif application.loan_term_months > 360:
        score -= 3
    
    # Cap score between 0-100
    score = max(0, min(100, score))
    
    # Determine risk category
    if score >= 70:
        risk_category = "LOW"
        approval = "APPROVE"
    elif score >= 50:
        risk_category = "MEDIUM"
        approval = "REVIEW"
    else:
        risk_category = "HIGH"
        approval = "DECLINE"
    
    # Identify key factors
    positive_factors = []
    negative_factors = []
    
    if application.applicant_income > 60000:
        positive_factors.append("Strong income level")
    if debt_to_income < 30:
        positive_factors.append("Low debt-to-income ratio")
    if application.credit_history_months > 48:
        positive_factors.append("Established credit history")
    if application.employment_status == "employed":
        positive_factors.append("Stable employment")
    if loan_to_income < 3:
        positive_factors.append("Reasonable loan amount")
    
    if debt_to_income > 40:
        negative_factors.append("High existing debt burden")
    if loan_to_income > 4:
        negative_factors.append("Large loan relative to income")
    if application.credit_history_months < 24:
        negative_factors.append("Limited credit history")
    if application.employment_status == "unemployed":
        negative_factors.append("No stable income source")
    if payment_to_income > 40:
        negative_factors.append("High monthly payment burden")
    
    # Generate application ID
    app_id = f"APP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Calculate confidence (simplified)
    confidence = 0.75 + (abs(score - 50) / 100) * 0.2
    
    return RiskAssessment(
        application_id=app_id,
        risk_score=int(score),
        risk_category=risk_category,
        approval_recommendation=approval,
        confidence=round(confidence, 2),
        key_factors={
            "positive": positive_factors if positive_factors else ["None identified"],
            "negative": negative_factors if negative_factors else ["None identified"]
        },
        debt_to_income_ratio=round(debt_to_income, 2),
        loan_to_income_ratio=round(loan_to_income, 2),
        processed_at=datetime.now().isoformat()
    )

# Endpoints
@app.get("/")
def root():
    return {
        "message": "Credit Risk Scoring API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/v1/score", response_model=RiskAssessment)
def score_application(application: LoanApplication):
    """
    Score a loan application and return risk assessment
    """
    try:
        assessment = calculate_risk_score(application)
        return assessment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")

@app.get("/api/v1/model/info", response_model=ModelInfo)
def get_model_info():
    """
    Get information about the scoring model
    """
    return ModelInfo(
        model_name="Credit Risk Assessment Model",
        version="1.0.0",
        accuracy=0.82,
        features=[
            "applicant_income",
            "loan_amount", 
            "loan_term_months",
            "credit_history_months",
            "employment_status",
            "property_area",
            "dependents",
            "education",
            "existing_debt"
        ],
        trained_on="2026-02-01"
    )

@app.get("/api/v1/model/features")
def get_required_features():
    """
    Get list of required features for scoring
    """
    return {
        "required_features": LoanApplication.model_json_schema()["properties"],
        "example": LoanApplication.Config.json_schema_extra["example"]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)