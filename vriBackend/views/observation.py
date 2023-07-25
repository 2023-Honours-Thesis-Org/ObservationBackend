from flask import Blueprint, jsonify

api = Blueprint('observationAPI', __name__, url_prefix='/api/v1')

@api.route('/observe/health')
def health():
    return jsonify({'status': 'ok'}), 200

@api.route('/observe', methods=['POST'])
def start_observation():
    return jsonify({'status': 'starting observation'}), 201