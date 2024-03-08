import streamlit as st
import pandas as pd
import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title('Email Sender')

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

sender_email = st.text_input('Sender Email')
sender_password = st.text_input('Sender Password', type='password')
csv_file = st.file_uploader('Upload CSV File', type=['csv'])

if sender_email and sender_password and csv_file:
    recipients_df = pd.read_csv(csv_file)
    send_emails(sender_email, sender_password, recipients_df)
    st.success('Emails sent successfully!')
