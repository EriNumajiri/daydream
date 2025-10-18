from flask import Flask, request, jsonify, send_from_directory
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, 'answers.json')

# JSON ファイル初期化
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump([[], [], []], f, ensure_ascii=False, indent=2)

# ルートで一番上の階層の index.html を返す
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/submit', methods=['POST'])
def submit():
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        answers = json.load(f)

    data = request.get_json()
    selections = data.get('selections', [0, 0, 0])

    for i in range(3):
        answers[i].append(selections[i])

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)

    print("現在の蓄積状態:", answers)
    return "回答を受け付けました！"

@app.route('/get-answers', methods=['GET'])
def get_answers():
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        answers = json.load(f)
    return jsonify(answers)

if __name__ == '__main__':
    app.run(debug=True)
