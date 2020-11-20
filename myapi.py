import os
import re
import textract
from flask import Flask, request, abort, jsonify, send_from_directory


UPLOAD_DIRECTORY = "/api_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


api = Flask(__name__)


@api.route("/", methods=["GET"])
def normal():
    return "Yippie"


@api.route("/pdf2txt/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""
    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories allowed")
    pdfPath = os.path.join(UPLOAD_DIRECTORY, filename)
    with open(pdfPath, "wb") as fp:
        fp.write(request.data)
    text = textract.process(pdfPath)
    data = re.split('\s{8,}', text.decode("utf-8"))
    return jsonify(data)

# app name


@api.errorhandler(404)
def not_found(e):
    return "error yaar"


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8080)
