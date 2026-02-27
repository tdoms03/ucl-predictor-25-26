from flask import Flask, render_template

app = Flask(__name__)

# Route for the Homepage
@app.route('/')
def index():
    return render_template('index.html')

# --- NEW ROUTE ---
@app.route('/knockout')
def knockout():
    return render_template('knockout.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)