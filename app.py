from flask import Flask, send_from_directory, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

JSON_FILE = 'answers.json'

# JSON ファイルがなければ初期化
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump([[], [], []], f, ensure_ascii=False, indent=2)

def safe_load_json():
    """壊れてるJSONを安全に読み込む"""
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("⚠️ JSONファイルが壊れていたため初期化します")
        data = [[], [], []]
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
    selections = data.get('selections', [0, 0, 0])  # 今回分だけ

    for i in range(3):
        answers[i].append(selections[i])

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)

    print("現在の蓄積状態:", answers)
    return "回答を受け付けました！"

@app.route('/get-answers', methods=['GET'])
def get_answers():
    answers = safe_load_json()
    return jsonify(answers)

@app.route('/ping', methods=['GET'])
def ping():
    return "pong"

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(debug=True)
