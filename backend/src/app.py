from flask import Flask, jsonify, request, send_from_directory
import uuid
import mock_backend

app = Flask(__name__)
base_url: str = '/api/v1'
frontend_dir: str = '../../frontend'

@app.route('/', methods=['GET'])
def serve_frontend():
    return mock_backend.send_from_directory(frontend_dir, 'index.html')

@app.route('/script/<string:script>', methods=['GET'])
def serve_scripts(script: str):
    return mock_backend.send_from_directory(frontend_dir + '/scripts', script)

@app.route('/style/<string:style>', methods=['GET'])
def serve_styles(style: str):
    return mock_backend.send_from_directory(frontend_dir + '/styles', style)

# TODO: Byt ut mot CDN
@app.route('/images/<string:image>', methods=['GET'])
def serve_images(image: str):
    return mock_backend.send_from_directory(frontend_dir + '/images', image)

@app.route(base_url + '/sessions', methods=['GET'])
def list_sessions():
    return mock_backend.list_sessions()

@app.route(base_url + '/sessions', methods=['POST'])
def create_session():
    return mock_backend.create_session()

@app.route(base_url + '/sessions/<uuid:session>/steps', methods=['GET'])
def get_steps(session: uuid):
    return mock_backend.get_steps(session)

@app.route(base_url + '/sessions/<uuid:session>/steps/<int:step>', methods=['GET'])
def get_step(session: uuid, step: int):
    return mock_backend.get_step(session, step)

@app.route(base_url + '/sessions/<uuid:session>/steps/<int:step>', methods=['PUT'])
def update_step(session: uuid, step: int):
    return mock_backend.update_step(session, step)
