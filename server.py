#!/usr/bin/env python3
"""
Simple Web Server for Loan Dashboard
Uses only Python built-in libraries
"""

import http.server
import socketserver
import json
import urllib.parse
from loan_logic import LoanProcessor

class LoanDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.loan_processor = LoanProcessor()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/dashboard':
            self.path = '/dashboard.html'
        elif self.path == '/style.css':
            self.path = '/style.css'
        
        return super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/submit-loan':
            self.handle_loan_submission()
        else:
            self.send_error(404)
    
    def handle_loan_submission(self):
        """Process loan application submission"""
        try:
            # Get form data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse form data
            form_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            
            # Convert form data to our format
            user_data = self.parse_form_data(form_data)
            
            # Process loan application
            result = self.loan_processor.process_application(user_data)
            
            # Send JSON response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = json.dumps(result, indent=2)
            self.wfile.write(response.encode())
            
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
    
    def parse_form_data(self, form_data):
        """Convert form data to our data structure"""
        def get_value(key):
            return form_data.get(key, [''])[0]
        
        return {
            'name': get_value('name'),
            'age': int(get_value('age')) if get_value('age') else 0,
            'email': get_value('email'),
            'phone': get_value('phone'),
            'monthly_income': float(get_value('monthly_income')) if get_value('monthly_income') else 0,
            'existing_debt': float(get_value('existing_debt')) if get_value('existing_debt') else 0,
            'job': get_value('job'),
            'work_years': float(get_value('work_years')) if get_value('work_years') else 0,
            'credit_score': get_value('credit_score'),
            'loan_purpose': get_value('loan_purpose')
        }

def main():
    PORT = 8000
    
    print("="*50)
    print("    LOAN DASHBOARD WEB SERVER")
    print("="*50)
    print(f"Starting server on port {PORT}...")
    print(f"Open your browser and go to: http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    print("="*50)
    
    try:
        with socketserver.TCPServer(("", PORT), LoanDashboardHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()