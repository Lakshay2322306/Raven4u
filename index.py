fromfrom flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    # Extract and handle commands here
    command = data.get('command')
    user_id = data.get('user_id')
    params = data.get('params', [])
    response = handle_command(command, user_id, params)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
