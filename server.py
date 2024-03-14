from flask import Flask, request, jsonify
from waitress import serve
from main import process_docx

app = Flask(__name__)
PORT = "80"

@app.route('/process', methods=['POST'])
def process():
    """
    gets data from the automation and process the docx content to fill the fields
    """
    request_content: dict = request.data.decode()
    print(request_content)
    docx_content = request_content["file"]
    fields = request_content["fields"]
    modified_docx_content = process_docx(fields, docx_content)
    return modified_docx_content

if __name__ == '__main__':
   # app.run(debug=True)
     serve(app, host = "0.0.0.0", port = PORT)