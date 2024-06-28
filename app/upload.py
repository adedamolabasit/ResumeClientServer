import os
import shutil
import subprocess
import re
import json
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pdfminer.high_level import extract_text
from docx import Document
from app.extensions import socketio

upload_blueprint = Blueprint('upload', __name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_pdf_to_txt(pdf_path, txt_path):
    text = extract_text(pdf_path)
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

def convert_docx_to_txt(docx_path, txt_path):
    doc = Document(docx_path)
    text = '\n'.join([p.text for p in doc.paragraphs])
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

@upload_blueprint.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'json_data' not in request.form:
        return jsonify({"error": "No file or json_data part in the request"}), 400

    file = request.files['file']
    json_data = request.form['json_data']

    try:
        data = json.loads(json_data)
        address = data.get('address')
        job_description = data.get('job_description')
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON data"}), 400

    if not address or not job_description:
        return jsonify({"error": "Missing address or job description"}), 400

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        folder_name = address[:6]
        folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = secure_filename(file.filename)
        file_path = os.path.join(folder_path, filename)
        file.save(file_path)

        # Save job description to a text file
        job_desc_path = os.path.join(folder_path, 'job_description.txt')
        with open(job_desc_path, 'w', encoding='utf-8') as f:
            f.write(job_description)

        file_ext = filename.rsplit('.', 1)[1].lower()
        txt_path = os.path.join(folder_path, filename.rsplit('.', 1)[0] + '.txt')
        if file_ext == 'pdf':
            convert_pdf_to_txt(file_path, txt_path)
        elif file_ext == 'docx':
            convert_docx_to_txt(file_path, txt_path)
        elif file_ext == 'txt':
            shutil.copy(file_path, txt_path)
        else:
            return jsonify({"error": "Unsupported file type for conversion"}), 400

        if os.path.exists(file_path):
            os.remove(file_path)

        script_path = 'app/rag_tools/add_knowledge_base.py'
        command = ['python', script_path, '--directory', folder_path, '--chunk-size', '8000', '--chunk-overlap', '100']

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            print("Script output:", result.stdout)

            cid_pattern = r'Qm[a-zA-Z0-9]{44}'
            match = re.search(cid_pattern, result.stdout)
            if match:
                cid = match.group(0).strip()
                print("Extracted CID:", cid)

                if result.returncode != 0:
                    print("Script error:", result.stderr)
                    return jsonify({"error": result.stderr}), 500

                return jsonify({"message": "File uploaded and processed successfully", "output": result.stdout, "cid": cid}), 200
            else:
                print("CID not found in script output")
                return jsonify({"error": "CID not found in script output"}), 500
        except subprocess.CalledProcessError as e:
            print("Subprocess error:", str(e))
            return jsonify({"error": "Subprocess error while running the script"}), 500
        except Exception as e:
            print("Exception occurred:", str(e))
            return jsonify({"error": "An error occurred while processing the file."}), 500
        finally:
            shutil.rmtree(folder_path)
    else:
        return jsonify({"error": "File type not allowed"}), 400