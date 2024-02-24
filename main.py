from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def send_command():
    data = request.get_json()
    command = data['command']
    try:
        with open('Command.txt', 'a+') as file:
            file.write(command + '\n')
        return jsonify({'message': f'Command "{command}" sent successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/result', methods=['GET'])
def get_result():
    try:
        if not os.path.exists('Result.txt'):
            with open('Result.txt', 'w'):
                pass
        with open('Result.txt', 'r') as file:
            result = file.read()
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
