from flask import Flask, render_template, request, jsonify
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

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    # 既存の回答を読み込み
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        answers = json.load(f)

    data = request.get_json()
    selections = data.get('selections', [0, 0, 0])  # 今回分だけ

    # 過去・現在・未来ごとに追加
    for i in range(3):
        answers[i].append(selections[i])

    # JSON に保存
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
