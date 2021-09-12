from flask import Flask,request
from service.ipCalculatorService import getModelOneAnswer,getModelOneAnswerWithId
app = Flask(__name__)


@app.route('/')
def getAnswer():
    return getModelOneAnswer(request.args.get('ip'))

@app.route('/<string:studentId>')
def getAnswerStudentId(studentId):
    return getModelOneAnswerWithId(studentId)

if __name__ == '__main__':
    app.run()