from docx import Document

def process_docx(fields, docx_content):
    doc = Document(docx_content)

    # Iterate through each content control in the document
    for paragraph in doc.paragraphs:
        for cc in paragraph._element.xpath("w:sdt/w:sdtContent/w:r/w:t"):
            # Check each field for a match
            for field in fields:
                key = field["key"]
                value = field["value"]
                # Replace the content control text if it matches the key
                if cc.text == f"[{key}]":
                    cc.text = value
                    # Break the loop to avoid unnecessary checks
                    break
    
    return doc


# replace_content_control("ויתור סודיות copy.docx")
