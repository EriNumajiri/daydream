from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Unity からのアクセスを許可

@app.route('/')
def hello():
    # Unity に送りたい文字列（自由に変更OK）
    return "jump"

if __name__ == '__main__':
    app.run(debug=True)
