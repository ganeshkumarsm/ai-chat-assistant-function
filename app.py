from flask import Flask, render_template, request, jsonify
from rag import ask

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    question = request.json["message"]

    answer = ask(question)

    return jsonify({"response": answer})


if __name__ == "__main__":
    app.run()