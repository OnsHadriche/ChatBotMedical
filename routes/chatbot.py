from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from rag_chatbot import rag_chat_medical

chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route("/")
@login_required
def index():
    return render_template('chat.html', user=current_user)


@chatbot_bp.route("/get_msg_chat_medical", methods=["GET", "POST"])
@login_required
def chat():
    msg = request.form.get('msg', '').strip()
    if not msg:
        return jsonify({'error': 'No message provided'}), 400
    return rag_chat_medical(msg)