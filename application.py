import os
import re
import textract
from flask import Flask, request, abort, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS


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
    # print(request)
    filename = secure_filename(file.filename)
    if "/" in filename:
        abort(400, "no subdirectories allowed")

    pdfPath = os.path.join(UPLOAD_DIRECTORY, filename)
    file.save(pdfPath)
    text = textract.process(pdfPath)
    data = re.split('\s{8,}', text.decode("utf-8"))
    datt = '\n'.join(data)
    resp = jsonify({"pdfData": datt, "message": "SUCCESS"})
    resp.status_code = 200
    return resp
    # return jsonify(datt)

# app name


@application.errorhandler(404)
def not_found(e):
    return e.message


if __name__ == "__main__":
    # application.run()
    application.run(host="0.0.0.0", port=80)
