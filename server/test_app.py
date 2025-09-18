from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/games', methods=['GET', 'POST'])
def games():
    if request.method == 'GET':
        return jsonify({"message": "GET request works"})
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({"message": "POST request works", "data": data})

if __name__ == '__main__':
    app.run(port=5001, debug=True)