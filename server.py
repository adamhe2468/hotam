from flask import Flask, request, jsonify
from waitress import serve
from main import process_docx,add_img_to_cc
import base64
import json
from io import BytesIO
app = Flask(__name__)
PORT = "80"

@app.route('/process', methods=['POST'])
def process():
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
     dictionary[item['key']] = item['value']
     # first fill the text fields
    signatures= {"Picture 1":law_sig,
                 "Picture 2": costumer_sig}
    modified_docx_content = process_docx(dictionary, docx_content)
    # insert the signatures
    modified_docx_content =  add_img_to_cc(modified_docx_content,signatures)  
        # Encode the modified DOCX content
    modified_docx_encoded = base64.b64encode(modified_docx_content).decode('utf-8')
        
    return jsonify({"file": {    "$content-type": docx_type,"$content": modified_docx_encoded}})
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=PORT)
    # serve(app, host = "0.0.0.0", port = PORT)