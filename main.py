from flask import Flask, render_template, request
from src.answer.default_answer import answering


app = Flask(__name__)

@app.route("/")
def show():
	return render_template("template.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    ans, data = answering(userText)
    print(data)
    return ans