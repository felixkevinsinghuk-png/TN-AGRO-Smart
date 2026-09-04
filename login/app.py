from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login_page.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/ai-engine')
def ai_engine():
    return render_template('ai_engine.html')

if __name__ == '__main__':
    app.run(debug=True)
