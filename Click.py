import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import urlencode
from flask import Flask, request

app = Flask(__name__)

st.title('Email Sender')

@app.route('/')
def index():
    return 'Streamlit server is running.'

@app.route('/send_emails', methods=['POST'])
def send_emails():
    sender_email = request.form.get('sender_email')
    sender_password = request.form.get('sender_password')
    csv_file = request.files['csv_file']

    if not sender_email or not sender_password or not csv_file:
        return 'Please provide sender email, sender password, and upload a CSV file.', 400

    try:
        recipients_df = pd.read_csv(csv_file)
        send_emails(sender_email, sender_password, recipients_df)
        return 'Emails sent successfully!'
    except Exception as e:
        return f'Error: {str(e)}', 500

def send_emails(sender_email, sender_password, recipients_df):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    for index, row in recipients_df.iterrows():
        recipient_email = row['email']
        unique_link = row['unique_link']

        subject = 'Your Personalized Link'
        body = f'Hello,\n\nClick the following link to access your personalized content:\n{unique_link}\n\nBest regards,\nSender'

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, recipient_email, message.as_string())
        print(f"Email sent to {recipient_email}")

        server.quit()

@app.route('/click', methods=['GET'])
def track_click():
    recipient_email = request.args.get('recipient_email')
    unique_id = request.args.get('unique_id')
    
    
    with open('clicks.log', 'a') as logfile:
        logfile.write(f"{recipient_email},{unique_id}\n")
    
    return 'Link clicked successfully!'

if __name__ == '__main__':
    app.run(debug=True)
