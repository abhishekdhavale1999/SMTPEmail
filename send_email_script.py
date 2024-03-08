# combined_app.py

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

def track_click(recipient_email, unique_link):
    with open('clicks.log', 'a+') as logfile:
        existing_data = logfile.readlines()
        exists = any(f"{recipient_email},{unique_link}" in line for line in existing_data)
        if not exists:
            logfile.write(f"{recipient_email},{unique_link}\n")

def main():
    st.title('Email Sending and Click Tracking')

    sender_email = st.text_input('Sender Email')
    sender_password = st.text_input('Sender Password', type='password')
    recipient_email = st.text_input('Recipient Email')
    unique_link = st.text_input('Unique Link')

    if st.button('Send Email'):
        send_email(sender_email, sender_password, recipient_email, unique_link)

    st.write('---')

    recipient_email_click = st.text_input('Recipient Email for Click Tracking')
    unique_link_click = st.text_input('Unique Link for Click Tracking')

    if st.button('Track Click'):
        track_click(recipient_email_click, unique_link_click)
        st.success('Click tracked successfully!')

if __name__ == "__main__":
    main()
