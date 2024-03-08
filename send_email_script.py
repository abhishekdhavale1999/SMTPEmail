# send_email_script.py

import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, unique_link):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  
    
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
    st.success(f"Email sent to {recipient_email}")
    server.quit()

def main():
    st.title('Email Sending')

    sender_email = st.text_input('Sender Email')
    sender_password = st.text_input('Sender Password', type='password')
    recipient_email = st.text_input('Recipient Email')
    unique_link = st.text_input('Unique Link')

    if st.button('Send Email'):
        send_email(sender_email, sender_password, recipient_email, unique_link)

if __name__ == "__main__":
    main()
