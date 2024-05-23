from flask import Flask, request, jsonify
from waitress import serve
from main import process_docx,add_img_to_cc
import base64
import json
from io import BytesIO
app = Flask(__name__)
PORT = "80"

@app.route('/process', methods=['POST'])
def process() -> dict:
    """
    gets data from the automation and process the docx content to fill the fields
    """
    request_content = request.get_json()
    docx_content = base64.b64decode(request_content["file"]["$content"])
    docx_type =request_content["file"]["$content-type"]
    fields = request_content["fields"]
    law_sig = request_content["lawyer"]
    costumer_sig = request_content["costumer"]


# Parse the JSON string into a list of dictionaries
    json_list = json.loads(fields)

# Construct the dictionary
    dictionary = {}
    for item in json_list:
        # security check to prevent file injections
        if "<" not in item['value'] and ">" not in item["value"] and len(item["value"])< 50:
             dictionary[item['key']] = item['value']
        else:
            return jsonify({"Message":f"{item['value']} contains < or > or has more than 50 characters"}), 400
            
     # first fill the text fields
    no_sig== False
    if(law_sig=="" and costumer_sig==""):
      no_sig = True 
    elif(costumer_sig==""):   
     signatures= {"Picture 1":law_sig}
    elif(law_sig==""):
      signatures={
                 "Picture 2": costumer_sig}  
    else:
      signatures= {"Picture 1":law_sig,
                 "Picture 2": costumer_sig}  
        
    modified_docx_content = process_docx(dictionary, docx_content)
    # insert the signatures
    if(no_sig== False ):
     modified_docx_content =  add_img_to_cc(modified_docx_content,signatures)  
        # Encode the modified DOCX content
    modified_docx_encoded = base64.b64encode(modified_docx_content).decode('utf-8')
        
    return jsonify({"file": {    "$content-type": docx_type,"$content": modified_docx_encoded}})
    
if __name__ == '__main__':
    serve(app, host = "0.0.0.0", port = PORT)
