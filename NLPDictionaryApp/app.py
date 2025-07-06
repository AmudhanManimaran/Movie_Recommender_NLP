from flask import Flask, render_template, request
from dictionary_engine import get_word_details

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        word = request.form.get("word")
        result = get_word_details(word)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
