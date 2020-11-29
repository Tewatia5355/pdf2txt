import os
import re
import textract
from flask import Flask, request, abort, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_module(ResumeText):
    ResumeTextLis = ResumeText.split()

    sections = [
        'SKILLS',
        'WORK',
        'EDUCATION',
        'ACHIEVEMENTS'
    ]

    newText = []
    Sections = []
    flag = False
    for i in range(len(sections)-1):
        for word in ResumeTextLis:
            if flag:
                newText.append(word)
            if word == sections[i]:
                flag = True
            elif word == sections[i+1]:
                flag = False
        flag = False
        Sections.append(newText)
        newText = []

    sectionString = []

    for subList in Sections:
        string = " "
        STRING = string.join(subList)
        STRING = STRING.encode('utf8')
        sectionString.append(STRING)

    return sectionString


def plag_check(linkedin, respp):
    ans = 0
    for i in range(3):
        tf1, tf2 = open("./tmp/t1.txt", "w"), open("./tmp/t2.txt", "w")
        tf1.write(linkedin[i])
        tf2.write(respp[i])
        file = ["./tmp/t1.txt", "./tmp/t2.txt"]
        tf1.close()
        tf2.close()
        student_notes = [open(File).read() for File in file]
        vectors = TfidfVectorizer().fit_transform(student_notes).toarray()
        sim_score = cosine_similarity([vectors[0], vectors[1]])[0][1]
        ans = ans + sim_score*100
    return ans/3
