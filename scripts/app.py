from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/upload_levels', methods=['POST'])
def upload_levels():
    data = request.json
    if 'input1' not in data or 'input2' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    input1 = data['input1']
    input2 = data['input2']

    print(f"Received audio levels: Input 1: {input1}, Input 2: {input2}")
    # Further processing or storage of audio levels can be done here
    return jsonify({'status': 'success'})

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5001)
