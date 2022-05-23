import smtplib
from email.message import EmailMessage

def process(sender, receiver, attachment, subject, content, password):
    # Create an instance of the EmailMessage class
    msg = EmailMessage()# Define the 'Subject' of the email
    msg['Subject'] = subject# Define 'From' (your email address)
    msg['From'] = sender # Define 'To' (to whom is it addressed)
    msg['To'] = receiver # The email content (your message)
    msg.set_content(content)

    with open(attachment, 'rb') as attach:
        msg.add_attachment(attach.read(), maintype='application', subtype='octet-stream', filename=attach.name)

    # Establishing a secure connection (SSL), login to your email account and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password) 
        smtp.send_message(msg)

if __name__ == "__main__":
	import os
	process(os.environ['EMAIL_SENDER'], os.environ['EMAIL_RECEIVER'], 'photo.jpeg', "Coucou", "Test", os.environ['EMAIL_SECRET'])
