import os
import re
import textract
from flask import Flask, request, abort, jsonify, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_DIRECTORY = "/tmp"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


application = Flask(__name__)


@application.route("/", methods=["GET"])
def normal():
    return "Yippie"


@application.route("/pdf2txt/", methods=["POST"])
def post_file():
    """Upload a file."""

    # pdfPath = os.path.join(UPLOAD_DIRECTORY, filename)
    # with open(pdfPath, "wb") as fp:
    #     fp.write(request.data)
    file = request.files['file']
    filename = secure_filename(file.filename)
    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories allowed")

    pdfPath = os.path.join(UPLOAD_DIRECTORY, filename)
    file.save(pdfPath)
    text = textract.process(pdfPath)
    data = re.split('\s{8,}', text.decode("utf-8"))
    return jsonify(data)

# app name


@application.errorhandler(404)
def not_found(e):
    return "error yaar"


if __name__ == "__main__":
    # application.run()
    application.run(host="0.0.0.0", port=80)
