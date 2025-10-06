from flask import Flask, render_template_string, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Unityからのアクセスを許可

# 回答を保存する変数（初期値は未回答状態）
answers = [None, None, None, None]

# シンプルなフォームページ
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>質問フォーム</title></head>
<body>
  <h2>質問フォーム</h2>
  <form action="/submit" method="post">
    <p>質問1の回答番号（1〜4）: <input type="number" name="q1" min="1" max="4" required></p>
    <p>質問2の回答番号（1〜4）: <input type="number" name="q2" min="1" max="4" required></p>
    <p>質問3の回答番号（1〜4）: <input type="number" name="q3" min="1" max="4" required></p>
    <p>質問4の回答番号（1〜4）: <input type="number" name="q4" min="1" max="4" required></p>
    <button type="submit">送信</button>
  </form>
  <p><a href="/get-answers" target="_blank">現在の回答を確認</a></p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/submit', methods=['POST'])
def submit():
    global answers
    # フォームから回答を取得
    answers = [
        request.form.get('q1'),
        request.form.get('q2'),
        request.form.get('q3'),
        request.form.get('q4')
    ]
    print("新しい回答を受信:", answers)
    return "回答を受け付けました！"

@app.route('/get-answers', methods=['GET'])
def get_answers():
    # Unityに返す用（例："2,1,3,4"）
    return ",".join(a or "0" for a in answers)

if __name__ == '__main__':
    app.run(debug=True)
