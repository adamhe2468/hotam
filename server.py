from flask import Flask, request, jsonify
from waitress import serve
from main import process_docx,add_img_to_cc
import base64

from ast import literal_eval

app = Flask(__name__)
PORT = "80"

@app.route('/process', methods=['POST'])
def process():
    """
    gets data from the automation and process the docx content to fill the fields
    """
    request_content = request.get_json()
    docx_content = base64.b64decode(request_content["file"]["$content"])
    fields = request_content["fields"]
    import json

  

# Parse the JSON string into a list of dictionaries
    json_list = json.loads(fields)

# Construct the dictionary
    dictionary = {}
    for item in json_list:
     dictionary[item['key']] = item['value']
    
    print(dictionary)    
    modified_docx_content = process_docx(dictionary, docx_content)
        
        # Encode the modified DOCX content
    modified_docx_encoded = base64.b64encode(modified_docx_content).decode('utf-8')
        
    return jsonify({"file": modified_docx_encoded})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=PORT)
    # serve(app, host = "0.0.0.0", port = PORT)