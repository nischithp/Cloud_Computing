import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('Pong.html')


if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    app.run(debug=True, host='0.0.0.0', port=port)