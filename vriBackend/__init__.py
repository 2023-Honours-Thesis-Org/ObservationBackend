from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views.route import api as testingAPI
    app.register_blueprint(testingAPI)
    from .views.observation import api as observationAPI
    app.register_blueprint(observationAPI)

    return app