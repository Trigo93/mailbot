import os
import gdrive_helper as gd
import pdf_helper as pdf
import mailbot as mail

from datetime import date
from dateutil.relativedelta import relativedelta

DRIVE_FILE_ID = os.environ['DRIVE_FILE_ID']

# Download template from google drive
gd.download_file_from_google_drive(DRIVE_FILE_ID, "template.pdf")

# Get first month day
first_day = date.today().replace(day=1)
d1 = first_day.strftime("%d/%m/%Y")

# Get last month day
next_month = first_day + relativedelta(months=1)
d2 = (next_month - relativedelta(days=1)).strftime("%d/%m/%Y")

# String to replace in PDF template
replacements = {
    'startDate': d1,
    'endDate': d2,
    }

print("Replacing startDate and endDate in template with", d1, "and", d2)

# Process pdf
writer = pdf.process("template.pdf", replacements)

# Create a new pdf file with changes
fname = "quittance_" + first_day.strftime("%m_%Y") + ".pdf"
with open(fname, 'wb') as out_file:
    writer.write(out_file)

# Send email
subject = "Quittance " + first_day.strftime("%m/%Y")
content = \
    "Bonjour Romain, Bonjour Simon,\n" \
    "Nous espérons que tout se passe bien pour vous à Vitry.\n" \
    "Nous avons bien reçu votre virement. Vous trouverez donc en pièce jointe la quittance pour votre paiement.\n\n" \
    "Bien cordialement,\n" \
    "Lauriane Houdebine"

# Send email
mail.process(sender, receiver, fname, subject, content)
