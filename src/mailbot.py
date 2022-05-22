# Imports
import os
import smtplib
from email.message import EmailMessage

# Variables containing your email address and password
EMAIL_SENDER = os.environ['EMAIL_SENDER']
EMAIL_RECEIVER = os.environ['EMAIL_RECEIVER']
EMAIL_PASSWORD = os.environ['EMAIL_SECRET']

def process(attachment, subject, content):
    # Create an instance of the EmailMessage class
    msg = EmailMessage()# Define the 'Subject' of the email
    msg['Subject'] = subject# Define 'From' (your email address)
    msg['From'] = EMAIL_SENDER # Define 'To' (to whom is it addressed)
    msg['To'] = EMAIL_RECEIVER # The email content (your message)
    msg.set_content(content)

    with open(attachment, 'rb') as attach:
        msg.add_attachment(attach.read(), maintype='application', subtype='octet-stream', filename=attach.name)

    # Establishing a secure connection (SSL), login to your email account and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD) 
        smtp.send_message(msg)

if __name__ == "__main__":
	process('photo.jpeg', "Coucou", "Test")
