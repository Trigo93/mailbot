# Imports
import smtplib
from email.message import EmailMessage

# Variables containing your email address and password
EMAIL_ADDRESS = os.environ['EMAIL']
EMAIL_PASSWORD = os.environ['EMAIL_SECRET']

# Create an instance of the EmailMessage class
msg = EmailMessage()# Define the 'Subject' of the email
msg['Subject'] = 'Coucou Moumine'# Define 'From' (your email address)
msg['From'] = EMAIL_ADDRESS# Define 'To' (to whom is it addressed)
msg['To'] = "lauriane.houdebine@hotmail.fr"# The email content (your message)
msg.set_content('Test des boubins!')

with open('./photo.jpeg', 'rb') as attach:
    msg.add_attachment(attach.read(), maintype='application', subtype='octet-stream', filename=attach.name)

# Establishing a secure connection (SSL), login to your email account and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
    smtp.send_message(msg)
