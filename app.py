from flask import Flask, send_from_directory, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

JSON_FILE = 'answers.json'

# 初期化
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

def safe_load_json():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("⚠️ JSONファイルが壊れていたため初期化します")
        data = []
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/submit', methods=['POST'])
def submit():
    answers = safe_load_json()

    data = request.get_json()
    selections = data.get('selections', [0, 0, 0])  # [過去, 現在, 未来]
    qnum = len(answers) + 1  # 次の質問番号を自動で付ける

    record = {
        "question": qnum,
        "past": selections[0],
        "present": selections[1],
        "future": selections[2]
    }

    answers.append(record)

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)

    print("✅ 現在の蓄積状態:", answers)
    return "回答を受け付けました！"

@app.route('/get-answers', methods=['GET'])
def get_answers():
    return jsonify(safe_load_json())

@app.route('/ping', methods=['GET'])
def ping():
    return "pong"

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(debug=True)
