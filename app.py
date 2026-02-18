from flask import Flask, render_template, jsonify, request

from dotenv import load_dotenv
import rag_chatbot
from src.prompt import *

import os


#Initialize flask app
app = Flask(__name__)
load_dotenv()



@app.route("/")
def index():
    return render_template('chatbot.html')

@app.route("/get_mesg_chat_medical", methods =["GET","POST"])
def chatbot():
    msg = request.form['msg']
    input = msg
    return rag_chatbot(input, 1)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)