from docx import Document

# function to change the values of the content control in the word file


def replace_content_control(document_path):
    # opening the file to edit and read
    doc = Document(document_path)

    # iterating through every paragraph in the file
    for paragraph in doc.paragraphs:
        # looking for all the content control parts in the file
        for cc in paragraph._element.xpath("w:sdt/w:sdtContent/w:r/w:t"):
            # checking the existing text and changing it accordingly
            if cc.text == "[ClientName]":
                # change to whatever the user inputs
                cc.text = "[ClientName]"
    # saving the updated text
    doc.save(document_path)


# replace_content_control("ויתור סודיות copy.docx")
