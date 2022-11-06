import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject, NameObject
from fpdf import FPDF

def replace_text(content, replacements = dict()):
    lines = content.splitlines()

    result = ""

    for line in lines:
        replaced_line = line
        for k, v in replacements.items():
            replaced_line = replaced_line.replace(k, v)
        result += replaced_line + "\n"

    return result


def process_data(object, replacements):
    data = object.getData()

    decoded_data = data.decode('iso-8859-1')
    replaced_data = replace_text(decoded_data, replacements)
    encoded_data = replaced_data.encode('iso-8859-1')

    object.decodedSelf.setData(encoded_data)

def process(file, replacements):

    pdf = PdfFileReader(file)
    writer = PdfFileWriter()

    page = pdf.getPage(0)
    contents = page.getContents()

    process_data(contents, replacements)

    page[PyPDF2.pdf.NameObject("/Contents")] = contents.decodedSelf
    writer.addPage(page)

    return writer

def create(fname, data):
    p = FPDF()
    p.add_page()
    p.set_font('Arial', 'B', 14)

    p.cell(0, 5, 'LES BAILLEURS :', ln=1)
    p.set_font('Arial', '', 12)
    p.cell(0, 5, 'M. MALLET Tristan', ln=1)
    p.cell(0, 5, 'Mme HOUDEBINE Lauriane', ln=1)
    p.cell(0, 5, '95 avenue de Choisy', ln=1)
    p.cell(0, 5, '75013, Paris', ln=1)
    p.cell(0, 5, '06 62 79 84 81', ln=1)
    p.cell(0, 5, '06 72 70 36 38', ln=1)


    p.set_font('Arial', 'B', 14)
    p.cell(0, 5, 'LES LOCATAIRES :', align="R", ln=1)

    p.set_font('Arial', '', 12)
    for name in data["names"]:
        p.cell(0, 5, name, align="R", ln=1)
    p.cell(0, 5, '16ter avenue Henri Barbusse', align="R", ln=1)
    p.cell(0, 5, '94400, Vitry-Sur-Seine', align="R", ln=1)

    p.ln(10)
    p.set_font('Arial', 'B', 14)
    p.cell(190, 20, 'QUITTANCE DE LOYER', border=True, align="C", ln=1)

    p.ln(3)

    p.set_font('Arial', '', 12)
    p.cell(0, 5, 'Loyer du ' + data["dates"][0] + ' au ' + data["dates"][1], align="C", ln=1)

    p.ln(3)

    p.set_font('Arial', '', 11)
    p.cell(0, 5, 'Reçu la somme de 1350 euros', ln=1)
    p.cell(0, 5, 'Le ' + data["dates"][0], ln=1)
    p.cell(0, 5, 'Pour loyer et accessoires des locaux sis :', ln=1)
    p.cell(0, 5, '16ter avenue Henri Barbusse à Vitry-sur-Seine (94400) avec emplacement de parking libre, gardien et cave.', ln=5)

    p.ln(10)

    p.cell(0, 10, 'Détail de la quittance de loyer', border="T", ln=1)
    p.cell(0, 5, '- Loyer hors charges : 1151 euros', ln=1)
    p.cell(0, 5, '- Charges : 199 euros', ln=1)

    p.ln(3)

    p.set_font('Arial', 'B', 12)
    p.cell(0, 10, 'TOTAL : 1350 euros', border="B", ln=1)

    p.ln(15)

    p.set_font('Arial', '', 11)
    p.cell(0, 5, 'Fait à Paris le ' + data["dates"][0], ln=1)
    p.cell(0, 5, 'Signatures :', ln=1)

    for i, file in enumerate(data["signatures"]):
        # TODO: Parametrize signature location according to jpeg size
        p.image('signature_' + str(i+1) + ".jpg", x = 20 + 30*i, y = 220 - 20*i, w = 30, h = 0)

    # Go to 4 cm from bottom
    p.set_y(-40)
    p.set_font('Arial', 'I', 8)
    p.cell(0, 3, "Le paiement de la présente n'emporte pas présomption de paiement des termes antérieurs.", ln=1, align="C")
    p.cell(0, 3, 'Cette quittance ou ce reçu annule tous les reçus qui auraient pu être donnés pour acompte versé sur le présent terme.', ln=1, align="C")
    p.cell(0, 3, "En cas de congé précédemment donné, cette quittance ou ce reçu représenterait l'indemnité d'occupation", ln=1, align="C")
    p.cell(0, 3, "et ne saurait être considéré comme un titre d'occupation. Sous réserve d'encaissement.", ln=1, align="C")

    p.output(fname, 'D')

if __name__ == "__main__":
    import os
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="path to PDF document")
    args = vars(ap.parse_args())

    file = args["input"]
    filename_base = file.replace(os.path.splitext(file)[1], "")

     # String to replace in PDF template
    replacements = {
        'old_val': new_val,
        }

    writer = process(file, replacements)

    # Create a new pdf file with changes
    with open(filename_base + "_result" + ".pdf", 'wb') as out_file:
        writer.write(out_file)
