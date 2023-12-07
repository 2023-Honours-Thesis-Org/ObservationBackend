from flask import Flask
from .tasks.Imports.vriCalc import observationManager

obsMan = observationManager(arrayDir='./vriBackend/tasks/arrays', 
                            verbose=True, debug=True)

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'data'

    from .views.observation import api as observationAPI
    app.register_blueprint(observationAPI)

    return app