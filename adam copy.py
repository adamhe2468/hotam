from docx import Document
from docx.oxml.ns import qn

doc = Document("delete.docx")

img_ids = []
for rid in doc.part.rels.keys():
    if "image" in doc.part.rels[rid].target_ref:
        print(rid)
        img_ids.append(rid)

print(img_ids)

pic = doc._element.xpath("//a:blip")[0]
for img in img_ids:
  pic.set(qn("r:embed"),img)
try:
  pokemon = doc._element.xpath("//w:sdtPr")[0].getparent()
  pokemon.remove(doc._element.xpath("//w:sdtPr")[0])
except:
   print("already gone")

doc.save("delete.docx")