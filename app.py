from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/command', methods=['GET', 'POST'])
def handle_command():
    if request.method == 'GET':
        try:
            with open('Command.txt', 'r') as file:
                command = file.read().strip()
            return jsonify({'command': command}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    elif request.method == 'POST':
        data = request.get_json()
        command = data['command']
        try:
            with open('Command.txt', 'a+') as file:
                file.write(command + '\n')
            return jsonify({'message': f'Command "{command}" sent successfully.'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/result', methods=['GET', 'POST'])
def handle_result():
    if request.method == 'GET':
        try:
            if not os.path.exists('Result.txt'):
                return jsonify({'result': ''}), 200
            with open('Result.txt', 'r') as file:
                result = file.read()
            return jsonify({'result': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    elif request.method == 'POST':
        data = request.get_json()
        result = data['result']
        try:
            with open('Result.txt', 'w') as file:
                file.write(result + '\n')
            return jsonify({'message': f'Result updated successfully.'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
