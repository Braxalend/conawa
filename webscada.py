from flask import Flask, render_template, request, session, g, redirect, url_for,abort, flash, json, jsonify


app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)

@app.route('/')
def show_entries():
    author = "Brax"
    return render_template('webscada.html', author=author)

if __name__ == "__main__":
    app.run(host='0.0.0.0')