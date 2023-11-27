from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS
import requests, json

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'
app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json.get('message', '')
    print("User message: ", user_message)

    try:
        rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
        rasa_response.raise_for_status()
        rasa_response_json = rasa_response.json()

        print("Rasa response: ", rasa_response_json)

        if isinstance(rasa_response_json, list) and rasa_response_json:
            bot_response = rasa_response_json[0].get('text', 'Sorry, I didn\'t understand that.')
        else:
            bot_response = 'Invalid or empty response from Rasa server'
    except (requests.exceptions.RequestException, json.JSONDecodeError) as err:
        print(f"Error: {err}")
        bot_response = 'Error communicating with Rasa server'

    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True, port=3000)
