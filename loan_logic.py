"""
Loan Processing Logic
Same logic as before, but organized for web use
"""

import json
from datetime import datetime

class LoanProcessor:
    def __init__(self):
        self.loan_amount = 5000
        self.currency = "USDT"
    
    def process_application(self, data):
        """Main processing function"""
        try:
            # Step 1: Validate basic requirements
            errors = self.check_basic_requirements(data)
            if errors:
                return {
                    'status': 'ERROR',
                    'errors': errors,
                    'timestamp': datetime.now().isoformat()
                }
            
            # Step 2: Calculate approval score
            score = self.calculate_approval_score(data)
            
            # Step 3: Make decision
            decision = self.make_loan_decision(score)
            
            # Step 4: Create result
            result = {
                'status': 'SUCCESS',
                'applicant_name': data['name'],
                'loan_amount': self.loan_amount,
                'currency': self.currency,
                'application_score': score,
                'decision': decision,
                'timestamp': datetime.now().isoformat(),
                'application_id': f"LOAN{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            # Save result
            self.save_result(result)
            
            return result
            
        except Exception as e:
            return {
                'status': 'ERROR',
                'errors': [f"Processing error: {str(e)}"],
                'timestamp': datetime.now().isoformat()
            }
    
    def check_basic_requirements(self, data):
        """Check basic requirements"""
        errors = []
        
        if not data.get('name'):
            errors.append("Name is required")
        
        if data.get('age', 0) < 18:
            errors.append("Must be 18 or older")
        
        if data.get('monthly_income', 0) < 1000:
            errors.append("Monthly income must be at least $1000")
        
        if not data.get('email') or '@' not in data.get('email', ''):
            errors.append("Valid email is required")
        
        if not data.get('credit_score'):
            errors.append("Credit score information is required")
        
        return errors
    
    def calculate_approval_score(self, data):
        """Calculate approval score (0-100)"""
        score = 0
        
        # Credit Score (40 points max)
        credit_scores = {
            'excellent': 40,
            'good': 30,
            'fair': 20,
            'poor': 10,
            'unknown': 15
        }
        score += credit_scores.get(data.get('credit_score', 'unknown'), 0)
        
        # Monthly Income (30 points max)
        income = data.get('monthly_income', 0)
        if income >= 5000:
            score += 30
        elif income >= 3000:
            score += 25
        elif income >= 2000:
            score += 20
        elif income >= 1500:
            score += 15
        else:
            score += 10
        
        # Work Experience (20 points max)
        work_years = data.get('work_years', 0)
        if work_years >= 3:
            score += 20
        elif work_years >= 2:
            score += 15
        elif work_years >= 1:
            score += 10
        else:
            score += 5
        
        # Debt-to-Income Ratio (10 points max)
        if income > 0:
            debt_ratio = data.get('existing_debt', 0) / income
            if debt_ratio < 0.3:
                score += 10
            elif debt_ratio < 0.5:
                score += 7
            else:
                score += 3
        
        return min(score, 100)  # Cap at 100
    
    def make_loan_decision(self, score):
        """Make loan decision based on score"""
        if score >= 80:
            return {
                'status': 'APPROVED',
                'reason': 'Excellent application! All criteria met.',
                'interest_rate': 8.5,
                'monthly_payment': 439.12,
                'term_months': 12,
                'confidence': 'HIGH'
            }
        elif score >= 60:
            return {
                'status': 'APPROVED',
                'reason': 'Good application with standard terms.',
                'interest_rate': 12.5,
                'monthly_payment': 451.58,
                'term_months': 12,
                'confidence': 'MEDIUM'
            }
        elif score >= 40:
            return {
                'status': 'CONDITIONAL',
                'reason': 'Approved pending additional verification.',
                'interest_rate': 16.5,
                'monthly_payment': 465.84,
                'term_months': 12,
                'confidence': 'LOW',
                'required_documents': [
                    'Proof of income',
                    'Bank statements',
                    'Employment verification'
                ]
            }
        else:
            return {
                'status': 'DECLINED',
                'reason': 'Application does not meet minimum requirements.',
                'confidence': 'HIGH',
                'suggestions': [
                    'Increase monthly income',
                    'Reduce existing debt',
                    'Improve credit score',
                    'Apply again in 30 days'
                ]
            }
    
    def save_result(self, result):
        """Save result to file"""
        try:
            filename = f"loan_result_{result['application_id']}.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
        except:
            pass  # Don't fail if can't save