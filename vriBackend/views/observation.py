from typing import Tuple, Dict
from flask import Blueprint, jsonify, request, Response, send_file
from vriBackend.models.observation import Observation
from vriBackend import obsMan
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os

import traceback
import vriBackend.tasks.observationTask as observationTask
import base64

api = Blueprint('observationAPI', __name__, url_prefix='/api/v1')
observations:Dict[str, Observation] = {}

@api.route('/observe/health')
def health() -> Tuple[Response, int]:
    return jsonify({'status': 'ok'}), 200

@api.route('/observe/init', methods=['POST'])
def init_observation() -> Tuple[Response, int]:
    try:
        observation = Observation()
        observation.init()
        observations[observation.getID()] = observation
        observationTask.init_obs_man(obsId=observation.getID())
        return jsonify({'status': 'Initialised Observation Session',
                        'observation_id': f'{observation.getID()}'}), 201
                        
    except Exception as e:
        return jsonify({'error': 'Unknown error occurred',
                        'details': f'{e}'}), 501

@api.route('/observe/select/<obs_id>/array', methods=['POST'])
def select_arrays(obs_id: str) -> Tuple[Response, int]:
    try:
        observation = observations[obs_id]
        observation.setArrayConfig(request.json)
        
        response = observationTask.select_array(
            array_config=request.json['array_config'],
            haStart=request.json['hour_angle_start'],
            haEnd=request.json['hour_angle_end'],
            sampleRate=request.json['sample_rate'],
            id=obs_id
        )
        
        return jsonify(response), 201
    except KeyError as kE:
        return jsonify({'error': 'observation not found'}), 504
    except Exception as e:
        return jsonify({'error': 'Unknown error occurred',
                        'details': f'{e}'}), 501

@api.route('/observe/select/<obs_id>/options', methods=['POST'])
def select_observation_options(obs_id: str) -> Tuple[Response, int]:
    try:
        observation = observations[obs_id]

        observation.setObservationFreq(request.json.get('freq'))
        observation.setSrcDeclination(request.json.get('src_declination'))

        response = observationTask.select_observation_options(
            freq=request.json['freq'],
            src_declination=request.json['src_declination'],
            id=obs_id
        )

        return jsonify(response), 201
    except KeyError as kE:
        return jsonify({'error': 'observation not found'}), 504
    except Exception as e:
        return jsonify({'error': 'Unknown error occurred',
                        'details': f'{e}'}), 501

@api.route('/observe/<obs_id>/start/uv_cov', methods=['GET'])
def start_observation_uv_cov(obs_id: str) -> Tuple[Response, int]:
    try:
        observation = observations[obs_id]

        response = observationTask.observation_setup(obs_id)
        return send_file(response['figure'], mimetype="image/png"), 200
    except KeyError as kE:
        return jsonify({'error': 'observation not found'}), 504
    except Exception as e:
        return jsonify({'error': 'Unknown error occurred',
                        'details': f'{e}'}), 501

@api.route('/observe/<id>/start/loadimage', methods=['POST', 'PUT'])
def load_image(id: str) -> Tuple[Response, int]:
    imageFile = FileStorage(request.stream)
    try:
        imageFile.save(f'./vriBackend/data/toObserve_{id}.png')
        with open(f'./vriBackend/data/toObserve_{id}.png', 'rb') as f:  
            return jsonify({
                'filename': f'uploadedFile', 
                'status': 'uploaded',
                'content-type': request.content_type,
                'image': base64.b64encode(f.read()).decode('utf-8')
            }), 201
    except Exception as e:
        return jsonify({'error': 'Unknown error occured', 'details': f'{e}'}), 501 

@api.route('/observe/<obs_id>/start/image', methods=['POST', 'PUT'])
def send_image(obs_id: str) -> Tuple[Response, int]:
    try:
        observation = observations[obs_id]

        filePath = f'./vriBackend/data/img_{obs_id}.png'
        FileStorage(request.stream).save(filePath)
        response = observationTask.observation_image_calc(obs_id, filePath)
        return jsonify(response), 201
    except KeyError as kE:
        return jsonify({'error': 'observation not found'}), 504
    except Exception as e:
        return jsonify({'error': 'Unknown error occurred',
                        'details': f'{e}'}), 501

@api.route('/observe/<obs_id>/results', methods=['GET'])
def get_results(obs_id: str) -> Tuple[Response, int]:
    try:
        return jsonify(""), 201
    except Exception as e:
        return jsonify({'error': 'Unknown error occurred',
                        'details': f'{e}'}), 501
    
@api.route('/observe/<obs_id>/clear', methods=['POST'])
def clear_observation_manager(obs_id: str) -> Tuple[Response, int]:
    try: 
        return jsonify(observationTask.clear_obs(id=obs_id)), 201
    except Exception as e:
        return jsonify({'error': 'Unknown error occurred',
                        'details': f'{e}'}), 501