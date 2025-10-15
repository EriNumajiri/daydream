from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

answers = [None, None, None, None]

@app.route('/')
def index():
    return render_template("index.html")  # ← これでtemplates/index.htmlを表示

@app.route('/submit', methods=['POST'])
def submit():
    global answers
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
    return ",".join(a or "0" for a in answers)

if __name__ == '__main__':
    app.run(debug=True)
