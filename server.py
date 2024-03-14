from flask import Flask, request, jsonify
from waitress import serve
from main import process_docx
import base64

app = Flask(__name__)
PORT = "80"

@app.route('/', methods=['GET'])
def check():
   return {"OK" : 200}

@app.route('/process', methods=['POST'])
def process():
    """
    gets data from the automation and process the docx content to fill the fields
    """
    request_content: dict = request.data.decode()
    print(request_content)
    docx_content:bytes = base64.b64decode(request_content["file"])  # ["$content"]
    fields:dict = request_content["fields"]

    modified_docx_content:bytes = process_docx(fields, docx_content)
    return {"file" : modified_docx_content}

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=PORT)
    # serve(app, host = "0.0.0.0", port = PORT)