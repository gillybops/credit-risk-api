import random
import csv
from datetime import datetime, timedelta
import json

def generate_application():
    """Generate one random loan application with realistic data"""
    
    # Random applicant profile
    income = random.randint(25000, 150000)
    loan_amount = random.randint(50000, 500000)
    loan_term = random.choice([60, 120, 180, 240, 360])
    credit_history = random.randint(0, 120)
    employment = random.choice(['employed', 'employed', 'employed', 'self_employed', 'unemployed'])
    property_area = random.choice(['urban', 'urban', 'suburban', 'rural'])
    dependents = random.choices([0, 1, 2, 3, 4], weights=[30, 25, 25, 15, 5])[0]
    education = random.choice(['graduate', 'graduate', 'not_graduate'])
    existing_debt = random.randint(0, int(income * 0.5))
    
    # Calculate ratios
    debt_to_income = (existing_debt / income) * 100
    loan_to_income = loan_amount / income
    monthly_payment = loan_amount / loan_term
    payment_to_income = (monthly_payment * 12 / income) * 100
    
    # Calculate risk score (same logic as API)
    score = 50
    
    # Income factors
    if income > 80000:
        score += 15
    elif income > 50000:
        score += 10
    elif income < 25000:
        score -= 15
    
    # Debt-to-income
    if debt_to_income < 20:
        score += 15
    elif debt_to_income < 35:
        score += 5
    elif debt_to_income > 50:
        score -= 15
    elif debt_to_income > 40:
        score -= 10
    
    # Loan-to-income
    if loan_to_income < 2:
        score += 15
    elif loan_to_income < 3:
        score += 8
    elif loan_to_income > 5:
        score -= 15
    elif loan_to_income > 4:
        score -= 10
    
    # Credit history
    if credit_history > 60:
        score += 10
    elif credit_history > 36:
        score += 5
    elif credit_history < 12:
        score -= 10
    
    # Employment
    if employment == 'employed':
        score += 10
    elif employment == 'unemployed':
        score -= 20
    
    # Education
    if education == 'graduate':
        score += 5
    
    # Property area
    if property_area == 'urban':
        score += 5
    elif property_area == 'rural':
        score -= 3
    
    # Dependents
    if dependents == 0:
        score += 5
    elif dependents > 3:
        score -= 5
    
    # Loan term
    if loan_term <= 180:
        score += 5
    elif loan_term > 360:
        score -= 3
    
    # Cap score
    score = max(0, min(100, score))
    
    # Determine category and decision
    if score >= 70:
        category = 'LOW'
        decision = 'APPROVED'
    elif score >= 50:
        category = 'MEDIUM'
        decision = 'REVIEW'
    else:
        category = 'HIGH'
        decision = 'DECLINED'
    
    return {
        'application_date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
        'applicant_income': income,
        'loan_amount': loan_amount,
        'loan_term_months': loan_term,
        'credit_history_months': credit_history,
        'employment_status': employment,
        'property_area': property_area,
        'dependents': dependents,
        'education': education,
        'existing_debt': existing_debt,
        'debt_to_income_ratio': round(debt_to_income, 2),
        'loan_to_income_ratio': round(loan_to_income, 2),
        'risk_score': score,
        'risk_category': category,
        'decision': decision
    }

def generate_dataset(num_applications=500):
    """Generate dataset of loan applications"""
    applications = []
    for _ in range(num_applications):
        applications.append(generate_application())
    
    # Sort by date
    applications.sort(key=lambda x: x['application_date'])
    
    return applications

def save_to_csv(applications, filename='loan_applications.csv'):
    """Save applications to CSV"""
    if not applications:
        return
    
    keys = applications[0].keys()
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(applications)
    
    print(f"Saved {len(applications)} applications to {filename}")

if __name__ == '__main__':
    # Generate 500 applications
    print("Generating loan applications...")
    apps = generate_dataset(500)
    save_to_csv(apps)
    print("Done!")