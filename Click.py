import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save('recipients.csv')
    send_emails()
    return 'Emails sent successfully!'

def send_emails():
    sender_email = 'abhishekdhavale121@gmail.com'
    sender_password = 'vssj pgrs xums trgx'
    
    with open('recipients.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipient_email = row['email']
            unique_link = row['unique_link']
            send_email(sender_email, sender_password, recipient_email, unique_link)

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
    print(f"Email sent to {recipient_email}")
    
    server.quit()

@app.route('/<path:path>')
def catch_all(path):
    parsed_url = parse_qs(path.split('?')[-1])
    if 'email' in parsed_url and 'unique_link' in parsed_url:
        recipient_email = parsed_url['email'][0]
        unique_link = parsed_url['unique_link'][0]
        track_click(recipient_email, unique_link)
        return 'Link clicked successfully!'
    else:
        return 'Bad request'

def track_click(recipient_email, unique_link):
    with open('clicks.log', 'a') as logfile:
        logfile.write(f"{recipient_email},{unique_link}\n")

if __name__ == '__main__':
    app.run(debug=True)
