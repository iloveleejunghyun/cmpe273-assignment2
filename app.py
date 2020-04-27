from flask import Flask, escape, request, render_template, Response
import sqlite3
import json
import db
app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template('index.html')

@app.route('/api/tests', methods=['POST'])
def CreateATest():
    db.init_db()
    subject = request.json['subject']
    answer_keys = request.json['answer_keys']
    print(type(subject))
    print(str(type(answer_keys)))
    id = db.create_test(subject, str(answer_keys))
    print(id, subject, answer_keys)
    return {
        "id": id,
        "subject": subject, 
        "answer_keys": answer_keys
    }, 201


@app.route('/api/tests/<test_id>/scantrons', methods=['POST'])
def	UploadAScantron(test_id):
    #get json from request
    format = 'json'
    
    try:
        name = request.json['name']
    except:
        name = "default"
    
    if format == 'pdf' or format == None:
        format = 'pdf'
        pass
    elif format == 'json':
        scantron = request.json['answers']
    
    subject, answer_keys = db.get_test(test_id)
    answer_keys = eval(answer_keys)
    score = 0
    result = {}
    for key in answer_keys:
        if scantron[key] == answer_keys[key]:
            score = score+2
        result[key] = {"actual": scantron[key], "expected": answer_keys[key]}

    result = json.dumps(result, sort_keys=False, indent=4, separators=(',', ':'))
    scantron = request.get_data()
    print(result, type(result))
    #todo compare result
    

    #todo generate url
    url = "http://localhost:5000/files/scantron-1.json"

    id = db.create_scantron(name, test_id, format, url, score, result, scantron)

    return {
        "scantron_id": id, 
        "scantron_url": url,
        "name": name,
        "subject": subject,
        "score": score,
        "result": result
    }, 201


@app.route('/api/tests/<id>', methods=['GET'])
def	checkAllScantronSubmissions(id):
    #get json from request
    subject, answer_keys = db.get_test(id)
    scantrons = db.get_scantrons(test_id=id)

    #todo convert scantrons to submission json.

    return {
        "test_id": id, 
        "subject": subject,
        "answer_keys": answer_keys,
        "submissions": scantrons
    }, 201


@app.route('/files/<file_name>', methods=['GET'])
def	files(file_name):
    scantron = db.get_scantron(file_name)
    mimetype = "text/json"
    return Response(scantron, mimetype=mimetype)