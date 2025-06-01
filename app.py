from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"

memory_data = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global memory_data
    uploaded_file = request.files['memory_file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            memory_data = f.read()
    return "File uploaded successfully"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']

    prompt = f"""
You are now simulating a person based on the following memories:
{memory_data}

Respond to the user as if you are that person, using their tone and knowledge.

User: {user_message}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    bot_reply = response.choices[0].message.content.strip()
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
