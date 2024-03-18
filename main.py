from docx import Document
from io import BytesIO
from docx.shared import Inches
from PIL import Image
import base64
from lxml import etree

def add_img_to_cc(docx_content, signatures: dict):
    """
    Add images to content controls in a Word document.

    Args:
        docx_content (bytes): Content of the Word document.
        signatures (dict): Dictionary mapping content control names to signature images.

    Returns:
        bytes: Modified Word document content.
    """
    doc = Document(BytesIO(docx_content))

    for cc_name, signature in signatures.items():
        # Extract base64 data from the signature
        base64_data = signature.split(",")[1]
        image_data = base64.b64decode(base64_data)
        
        # Open the image using PIL
        image = Image.open(BytesIO(image_data))
        
        # Add the image to the document
        width, height = image.size
        doc.add_picture(BytesIO(image_data), width=Inches(width / 96))
        
        # Remove the paragraph containing the image
        p = doc.paragraphs[-1]._element
        p.getparent().remove(p)

        # Finding the ID of the image
        keys = list(doc.part.rels.keys())
        rid = keys[-1]

        # Register namespaces
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
              "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
              "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}

        # Find the content control with the specified name or skip if not found
        for sdt in doc.element.xpath("w:sdt"):
            alias = sdt.xpath(".//w:alias[@w:val='%s']" % cc_name)
            if alias:
                # Set the relationship ID for the image
                blip = sdt.xpath(".//a:blipFill/a:blip")[0]
                blip.set("{%s}embed" % ns["r"], rid)
                break

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

