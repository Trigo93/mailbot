from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject, NameObject

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
    if object.decodedSelf is not None:
        object.decodedSelf.setData(encoded_data)
    else:
        object.setData(encoded_data)

def process(file, replacements):

    pdf = PdfFileReader(file)
    writer = PdfFileWriter()

    for page_number in range(pdf.getNumPages()):

        page = pdf.getPage(page_number)
        contents = page.getContents()

        if isinstance(contents, DecodedStreamObject) or isinstance(contents, EncodedStreamObject):
            process_data(contents, replacements)
        elif len(contents) > 0:
            for obj in contents:
                if isinstance(obj, DecodedStreamObject) or isinstance(obj, EncodedStreamObject):
                    streamObj = obj.getObject()
                    process_data(streamObj, replacements)

        writer.addPage(page)

    return writer


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
