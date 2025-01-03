import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

class NotificationManager:
    def __init__(self):
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': 'your-email@gmail.com',
            'password': 'your-app-password'
        }
        
    def send_email_alert(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.email_config['username']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(self.email_config['smtp_server'], 
                                self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], 
                        self.email_config['password'])
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def send_sms_alert(self, phone_number, message):
        # Mock SMS sending function
        print(f"SMS alert to {phone_number}: {message}")
        return True
    
    def send_high_risk_alert(self, user_data, risk_score):
        # Email to user
        email_body = f"""
        Dear {user_data['name']},
        
        Your recent voice analysis showed a high risk score of {risk_score}.
        We recommend immediate medical consultation.
        
        Best regards,
        VocalDiagnose Team
        """
        self.send_email_alert(user_data['email'], 
                            "High Risk Alert - VocalDiagnose",
                            email_body)
        
        # SMS to emergency contact
        sms_message = f"ALERT: {user_data['name']} has recorded a high risk voice analysis score. Please check immediately."
        self.send_sms_alert(user_data['emergency_contact'], sms_message)