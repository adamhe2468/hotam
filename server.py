from flask import Flask, request, jsonify
import main

app = Flask(__name__)



@app.route('/process', methods=['POST'])
def process():
    json_data = request.json
    request_content: dict = request.data.decode()
    print(request_content)
    docx_content = request_content["file"]
    modified_docx_content = main.process_docx(json_data, docx_content)
    return modified_docx_content

if __name__ == '__main__':
    app.run(debug=True)
