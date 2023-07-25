from flask import Blueprint, jsonify

api = Blueprint('testingAPI', __name__, url_prefix='/api/v1')

@api.route('/health')

def health():
    return jsonify({"status":"ok"}), 200