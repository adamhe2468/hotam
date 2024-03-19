from docx import Document
from io import BytesIO
from docx.shared import Inches
from docx.shared import Pt
from io import BytesIO
from PIL import Image
import base64
from xml.etree import ElementTree as ET
from docx.oxml.ns import qn

def add_img_to_cc(docx_content, img_dict):

 doc = Document(BytesIO(docx_content))
 real_pics = doc._element.xpath("//pic:cNvPr")
 pics_names = []
 
 for real_pic in real_pics:
    pics_names.append(real_pic.name)   
 for cc_name, img_data in img_dict.items():
        # Decode base64 image data
    img_data_decoded = base64.b64decode(img_data.split(',')[1])
    
        # Add image to the document
    img_stream = BytesIO(img_data_decoded)
    # adding the image and removing it to create a rel between the document and the image
    doc.add_picture(img_stream)
    p = doc.paragraphs[-1]._element
    p.getparent().remove(p)
    
    # finding the id of the image
 
 keys = list(doc.part.rels.keys())

    # the rid of the picture we wanna add its also the last key in the list
    # rid = keys[-1]    # search for the image content control
    
 pic_ccs = doc._element.xpath("//a:blip")
 index = -2
    # iterating over the list of all the picture content controls
 for pic in pic_ccs:
      for name in pics_names:
        if(name == cc_name):    
          pic.set(qn("r:embed"), keys[index])
          try:
            temp = doc._element.xpath("//w:sdtPr")[0]
            temp.getparent().remove(temp)
          except:
            print("already gone") 
      index = index+1
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

