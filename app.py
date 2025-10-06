from flask import Flask, render_template_string, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 回答を一時的に保存する変数（本格的にやるならDB）
answers = [None, None, None, None]

# 質問フォーム（簡易HTML）
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>質問フォーム</title></head>
<body>
  <h2>質問フォーム</h2>
  <form action="/submit" method="post">
    <p>質問1: <input type="number" name="q1" min="1" max="4" required></p>
    <p>質問2: <input type="number" name="q2" min="1" max="4" required></p>
    <p>質問3: <input type="number" name="q3" min="1" max="4" required></p>
    <p>質問4: <input type="number" name="q4" min="1" max="4" required></p>
    <button type="submit">送信</button>
  </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/submit', methods=['POST'])
def submit():
    global answers
    answers = [
        request.form.get('q1'),
        request.form.get('q2'),
        request.form.get('q3'),
        request.form.get('q4')
    ]
    return "回答を受け付けました！"

@app.route('/get-answers', methods=['GET'])
def get_answers():
    # Unity から読み取れる形式（例："2,1,3,4"）
    return ",".join(a or "0" for a in answers)

if __name__ == '__main__':
    app.run(debug=True)
