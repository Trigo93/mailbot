import os
import argparse
import gdrive_helper as gd
import pdf_helper as pdf
import mail_helper as mail

from datetime import date
from dateutil.relativedelta import relativedelta

# Secret environment variables
DRIVE_FILE_IDS = [os.environ['SIGNATURE1'], os.environ['SIGNATURE2']]
EMAIL_SENDER = os.environ['EMAIL_SENDER']
EMAIL_RECEIVER = os.environ['EMAIL_RECEIVER']
EMAIL_PASSWORD = os.environ['EMAIL_SECRET']

ap = argparse.ArgumentParser()
ap.add_argument('-n','--names', nargs='+', help='noms des locataires', required=True)
args = vars(ap.parse_args())

# Download signatures from google drive
for i, file in enumerate(DRIVE_FILE_IDS):
    print(file)
    gd.download_file_from_google_drive(file, "signature_" + str(i+1) + ".jpg")

# Get first month day
first_day = date.today().replace(day=1)
d1 = first_day.strftime("%d-%m-%Y")

# Get last month day
next_month = first_day + relativedelta(months=1)
d2 = (next_month - relativedelta(days=1)).strftime("%d-%m-%Y")

data = {
    "signatures": ["signature_" + str(i+1) + ".jpg" for i in range(len(DRIVE_FILE_IDS))],
    "names": args["names"],
    "dates": [d1, d2]
}

# Create pdf
fname = "quittance_" + first_day.strftime("%m_%Y") + ".pdf"

pdf.create(fname, data)

# Send email
subject = "Quittance " + first_day.strftime("%m/%Y")
content = \
    "Bonjour Agnès, Bonjour Sylvain,\n" \
    "Nous espérons que tout se passe bien pour vous à Vitry.\n" \
    "Nous avons bien reçu votre virement. Vous trouverez donc en pièce jointe la quittance pour votre paiement.\n\n" \
    "Bien cordialement,\n" \
    "Lauriane Houdebine"

# Send email
mail.process(EMAIL_SENDER, EMAIL_RECEIVER, "src/"+fname, subject, content, EMAIL_PASSWORD)
