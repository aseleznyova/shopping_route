from flask import Flask, session
import json
app = Flask(__name__)

app.config.update(SECRET_KEY="sdasda")

@app.route('/api')
def server():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return {"msg":"Hellow world {}".format(session.get('visits'))}

if __name__ == "__main__":
    app.run('0.0.0.0', 5001)
