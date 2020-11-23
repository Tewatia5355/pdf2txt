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


# def vectorize(Text): return
# def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])


def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])


plagiarism_results = set()


def check_plagiarism():
    global s_vectors
    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            score = sim_score*100
            plagiarism_results.add(score)
    return plagiarism_results


application = Flask(__name__)
cors = CORS(application)


@application.route("/", methods=["GET"])
def normal():
    return "Yippie"


@application.route("/plag/", methods=["POST"])
def plag_check():
    """Upload a file."""
    global s_vectors
    file = request.form['myarray']
    tf1, tf2 = open("./tmp/t1.txt", "w"), open("./tmp/t2.txt", "w")
    file = ["./tmp/t1.txt", "./tmp/t2.txt"]
    tf1.write(file[0])
    tf2.write(file[1])
    tf1.close()
    tf2.close()
    student_notes = [open(File).read() for File in file]
    vectors = vectorize(student_notes)
    s_vectors = list(zip(file, vectors))
    ans = list(check_plagiarism())
    return jsonify(ans)


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
