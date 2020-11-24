import os
import re
import textract
from flask import Flask, request, abort, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
UPLOAD_DIRECTORY = "/tmp"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

application = Flask(__name__)
cors = CORS(application)


@application.route("/", methods=["GET"])
def normal():
    return "Yippie"


@application.route("/plag/", methods=["POST"])
def plag_check():
    """Upload a file."""

    global vectors
    file = request.form['myarray']
    tf1, tf2 = open("./tmp/t1.txt", "w"), open("./tmp/t2.txt", "w")
    tf1.write(file[0])
    tf2.write(file[1])
    file = ["./tmp/t1.txt", "./tmp/t2.txt"]
    tf1.close()
    tf2.close()
    student_notes = [open(File).read() for File in file]
    vectors = TfidfVectorizer().fit_transform(student_notes).toarray()
    sim_score = cosine_similarity([vectors[0], vectors[1]])[0][1]
    score = sim_score*100
    return jsonify(score)


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
    application.run()
    # application.run(host="0.0.0.0", port=80)
