from flask import Flask, send_from_directory, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

JSON_FILE = 'answers.json'
STATE_FILE = 'state.json'  # ← end状態を保存する小さなファイル

# JSONファイルがなければ初期化
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

# 状態ファイルがなければ初期化
if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"state": "none"}, f, ensure_ascii=False, indent=2)


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


def load_state():
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get("state", "none")
    except Exception:
        return "none"


def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"state": state}, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')


@app.route('/submit', methods=['POST'])
def submit():
    answers = safe_load_json()

    data = request.get_json()
    selections = data.get('selections', [0, 0, 0])
    question_number = data.get('question_number')

    if question_number is None:
        question_number = len(answers) + 1  # fallback

    record = {
        "question": question_number,
        "past": selections[0],
        "present": selections[1],
        "future": selections[2]
    }

    updated = False
    for i, ans in enumerate(answers):
        if ans["question"] == question_number:
            answers[i] = record
            updated = True
            break

    if not updated:
        answers.append(record)

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)

    print(f"✅ 質問{question_number}を更新:", record)
    return "回答を受け付けました！"


@app.route('/get-answers', methods=['GET'])
def get_answers():
    """回答データ＋end状態を返す"""
    data = {
        "answers": safe_load_json(),
        "state": load_state()
    }
    return jsonify(data)


@app.route('/end-reached')
def end_reached():
    """end.html が開かれたときに呼ばれる"""
    save_state("end")
    print("🟥 end.html にアクセスされました！（state = end）")
    return "OK"


@app.route('/reset-state')
def reset_state():
    """Unity側で処理完了後に呼べば再実行可能"""
    save_state("none")
    print("🔄 stateをリセットしました")
    return "reset OK"


@app.route('/ping', methods=['GET'])
def ping():
    return "pong"


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)


if __name__ == '__main__':
    app.run(debug=True)
