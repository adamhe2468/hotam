from docx import Document
from io import BytesIO
from docx.shared import Inches
import base64


def add_img_to_cc(docx_content, img_dict):
    # Load the DOCX content
    doc = Document(BytesIO(docx_content))

    # Iterate over the content controls and replace them with images
    for cc_name, img_data in img_dict.items():
        # Decode base64 image data
        img_data_decoded = base64.b64decode(img_data.split(',')[1])

        # Add image to the document
        img_stream = BytesIO(img_data_decoded)
        doc.add_picture(img_stream, width=Inches(1))  # You can adjust the width as needed

        # Find and replace the content control with the image
        for p in doc.paragraphs:
            if cc_name in p.text:
                # Clear the content control text
                p.clear()

                # Add the image to the paragraph
                run = p.add_run()
                run.add_picture(img_stream, width=Inches(1))  # You can adjust the width as needed
 # You can adjust the width as needed

    # Save the modified document content to a buffer
    modified_docx_buffer = BytesIO()
    doc.save(modified_docx_buffer)
    modified_docx_content = modified_docx_buffer.getvalue()                 
    return modified_docx_content

def process_docx(fields:dict, docx_content:bytes) -> bytes:
    doc = Document(BytesIO(docx_content))

    # Iterate through each content control in the document
    for paragraph in doc.paragraphs:
        for cc in paragraph._element.xpath("w:sdt/w:sdtContent/w:r/w:t"):
            # Check each field for a match
            for key,value in fields.items():
                if cc.text == f"[{key}]":
                    cc.text = value

    modified_docx_buffer = BytesIO()
    doc.save(modified_docx_buffer)
    modified_docx_content = modified_docx_buffer.getvalue()                 
    return modified_docx_content

