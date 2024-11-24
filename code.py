#updated one
from flask import Flask, request, jsonify
from pyngrok import ngrok

app = Flask(__name__)

# In-memory database
items = []

@app.route('/')
def index():
    return "Welcome to the Flask CRUD API! Use endpoints like /items to interact with the API.", 200

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items), 200

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    for item in items:
        if item['id'] == item_id:
            return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = {"id": len(items) + 1, "name": data.get("name")}
    items.append(new_item)
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    for item in items:
        if item['id'] == item_id:
            item['name'] = data.get('name', item['name'])
            return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    # Setup ngrok
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")

    # Run Flask app
    app.run()
