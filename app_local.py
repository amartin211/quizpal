from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from pipeline.generate_full_response import get_response_from_raw_image
from flask import send_from_directory

from flask import Flask, request, render_template_string
import os
from werkzeug.utils import secure_filename
import time 
import re
import boto3

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

from flask import send_from_directory

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_latex_format(latex_str):
    converted_str = re.sub(r'\$(.*?)\$', r'\\(\1\\)', latex_str)
    return converted_str


#def simulated_lambda_function(file_path):
#    original_image_path = file_path.replace("/static/", "")
#    processed_image_path = file_path.replace("/static/", "")
#    ocr_text = convert_latex_format(r"""If $\left(\frac{1}{5}\right)^{m}\left(\frac{1}{4}\right)^{18}=\frac{1}{2(10)^{35}}$, then $m=$""")

#    response_text = "Simulated Lambda Response"
#    return original_image_path, processed_image_path, ocr_text, response_text


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not allowed_file(file.filename):
            return "Invalid file. Please upload a valid image."

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        original_image, processed_image, ocr_text, response_text, answer_choice = get_response_from_raw_image(file_path)

        ocr_text = convert_latex_format(ocr_text)
        response_text = convert_latex_format(response_text)
        
        return render_template('results.html', 
                               original_image=original_image, 
                               processed_image=processed_image, 
                               ocr_text=ocr_text, 
                               response_text=response_text)
    
    return render_template('upload.html')


@app.route('/intermediary_files', methods=['GET'])
def handle_intermediary_files():
    # Logic to handle the request for intermediary files.
    # For this example, let's assume you want to list and return all filenames in the UPLOAD_FOLDER.
    
    file_list = os.listdir(UPLOAD_FOLDER)
    
    return render_template('intermediary_files.html', files=file_list)

   
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
