import os
import csv
import random
from flask import Flask, render_template, request, redirect, url_for
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

FROM_EMAIL = os.getenv("FROM_EMAIL")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SUBMISSIONS_CSV = os.getenv("SUBMISSIONS_CSV", "submissions.csv")

def send_confirmation_email(to_email, name, company, role, application_id):
    if not SENDGRID_API_KEY or not FROM_EMAIL:
        raise RuntimeError("SENDGRID_API_KEY and FROM_EMAIL must be set in environment")

    subject = f"Application Received — {company}"
    html_content = f"""
    <p>Hi {name},</p>
    <p>Thanks for applying to <strong>{company}</strong> for the role of <strong>{role}</strong>.</p>
    <p>Your application ID is <strong>{application_id}</strong>.</p>
    <p>We will review your submission and contact you if you are shortlisted.</p>
    <p>Best regards,<br/>{company} Hiring Team</p>
    """
    message = Mail(from_email=FROM_EMAIL, to_emails=to_email, subject=subject, html_content=html_content)
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('apply'))

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    company = request.args.get('company', 'Our Company')
    tracking = request.args.get('track', '')
    role_q = request.args.get('role', '')

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', role_q).strip() or '—'
        application_id = random.randint(100000, 999999)

        # Persist submission locally to CSV (append)
        try:
            file_exists = os.path.exists(SUBMISSIONS_CSV)
            with open(SUBMISSIONS_CSV, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['application_id', 'company', 'tracking', 'name', 'email', 'role', 'ip'])
                writer.writerow([application_id, company, tracking, name, email, role, request.remote_addr])
        except Exception as e:
            print('Warning: could not write submission to CSV:', e)

        # Send confirmation email
        try:
            send_confirmation_email(email, name, company, role, application_id)
            email_sent = True
        except Exception as e:
            print('Error sending email:', e)
            email_sent = False

        return render_template('success.html', company=company, application_id=application_id, email_sent=email_sent, email=email)

    return render_template('form.html', company=company, tracking=tracking, role=role_q)

if __name__ == '__main__':
    # For local testing
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
