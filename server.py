from flask import Flask, request, jsonify
import os

app = Flask(_name_)

@app.route("/start-jarvis", methods=["POST"])
def start_jarvis():
    os.system("jarvis.py")   # your main file name
    return jsonify({"status": "Jarvis started"})

if _name_ == "_main_":
    app.run(port=5000)