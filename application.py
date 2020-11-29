import os
import re
import textract
from flask import Flask, request, abort, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from py2 import extract_module, plag_check
UPLOAD_DIRECTORY = "/tmp"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

application = Flask(__name__)
cors = CORS(application)


@application.route("/", methods=["GET"])
def normal():
    return "Yippie"


@application.route("/pdf2txt/", methods=["POST"])
def post_file():
    """Upload a file."""

    file = request.files['file']
    linkedin_comp = [request.form['skill'].encode('utf8'),
                     request.form['work'].encode('utf8'), request.form['edu'].encode('utf8')]
    print(linkedin_comp)
    filename = secure_filename(file.filename)
    if "/" in filename:
        abort(400, "no subdirectories allowed")

    pdfPath = os.path.join(UPLOAD_DIRECTORY, filename)
    file.save(pdfPath)
    text = textract.process(pdfPath)
    data = re.split('\s{8,}', text.decode("utf-8"))
    datt = '\n'.join(data)
    resp = extract_module(datt)
    for x in resp:
        x = x.encode('utf8')
    print(resp)
    return jsonify(plag_check(linkedin_comp, resp))

# app name


@application.errorhandler(404)
def not_found(e):
    return e.message


if __name__ == "__main__":
    application.run()
    # application.run(host="0.0.0.0", port=80)
