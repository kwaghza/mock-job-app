# Mock Job Application System (Ready-to-Deploy)

This small Flask app accepts job applications on a per-company basis using URL parameters and sends a confirmation email via SendGrid.

## What you get
- `/apply?company=Company%20Name&track=1234567890` shows a company-specific form.
- Submissions are saved to `submissions.csv` (default) and a confirmation email is sent to the applicant.
- `update_csv_links.py` helps you regenerate your CSV with the correct deployed URL and fresh tracking IDs.

## Quick local setup (entry-level-friendly)

1. Install Python 3.8+ and Git.
2. Create a project folder and move these files there, or extract `mock-job-app.zip`.
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # mac/linux
   venv\Scripts\activate    # windows (PowerShell)
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your SendGrid API key and FROM_EMAIL:
   ```text
   SENDGRID_API_KEY=SG.xxxxxx
   FROM_EMAIL=hr@yourdomain.com
   ```
   **Important:** Verify the FROM_EMAIL in SendGrid (single sender verification or domain authentication).
5. Run locally:
   ```bash
   python app.py
   ```
   Open in your browser: `http://127.0.0.1:5000/apply?company=NovaTech%20Solutions&track=12345`

## Deploy to Render (recommended free option)
1. Push the project to GitHub.
2. Create a new Web Service on https://render.com and connect your GitHub repo.
3. Set the build & start command (Render usually detects Python):
   - Start command: `gunicorn app:app`
4. Add Environment Variables in Render's dashboard:
   - `SENDGRID_API_KEY` = your SendGrid API key
   - `FROM_EMAIL` = verified sender email (e.g., hr@yourdomain.com)
   - `SUBMISSIONS_CSV` = (optional) e.g., `submissions.csv`
5. Deploy. Render will give you a live URL like `https://yourapp.onrender.com`.

## Update your CSV links to point to the live app
Use the provided script to regenerate links:
```bash
python update_csv_links.py input_companies.csv output_links.csv https://yourapp.onrender.com/apply
```
The script will produce fresh tracking IDs and URL-encode company names.

## Troubleshooting & tips
- If emails don't send, check Render logs and ensure `SENDGRID_API_KEY` and `FROM_EMAIL` are correct and that the sender is verified in SendGrid.
- Check `submissions.csv` in your project root for saved applications (download from Render's dashboard or via SSH/Files if supported).
- Don't send unsolicited emails; use this system only for legitimate applications.

## Alternatives
- Use Formspree or Make.com if you prefer not to host a backend. This repo is for a full backend solution with real email sending.

--
