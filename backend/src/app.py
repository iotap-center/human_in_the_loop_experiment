from waitress import serve
from flask import Flask, jsonify, request, send_from_directory, abort
from session import Session, Subsession
from storage.storage import Storage
import configparser
import utils
import uuid
import main_BE

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config/app.ini')
mode=config['app']['mode']
host=config['app']['host']
port=config['app']['port']

base_url: str = config['api']['base_url']
frontend_base: str = config['frontend']['frontend_base']
image_base: str = config['frontend']['image_base']
image_directory: str = config['frontend']['image_directory']
storage: Storage = Storage.create_storage(config['backend']['storage_backend'])
backend = main_BE

step_duration: int = int(config['frontend']['step_duration'])
subsession_pause_duration: int = int(config['frontend']['subsession_pause_duration'])
labels: list = config['backend']['labels'].split(',')

@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory(frontend_base, 'index.html')

@app.route('/script/<string:script>', methods=['GET'])
def serve_scripts(script: str):
    return send_from_directory(frontend_base + '/scripts', script)

@app.route('/style/<string:style>', methods=['GET'])
def serve_styles(style: str):
    return send_from_directory(frontend_base + '/styles', style)

@app.route('/images/<string:image>', methods=['GET'])
def serve_images(image: str):
    return send_from_directory(image_directory, image)

@app.route(base_url + '/sessions', methods=['GET'])
def list_sessions():
    sessions: list = storage.list_sessions()

    data = {
        'sessions': list(),
        'links': {
            'self': {
                'href': base_url + '/sessions',
                'method': 'GET'
            },
            'create': {
                'href': base_url + '/sessions',
                'method': 'POST'
            }
        }
    }
    
    if len(sessions) > 0:
        data['links']['first'] = dict()
        data['links']['first']['href'] = base_url + '/sessions/' + str(sessions[0])
        data['links']['first']['method'] = 'GET'
        data['links']['last'] = dict()
        data['links']['last']['href'] = base_url + '/sessions/' + str(sessions[-1])
        data['links']['last']['method'] = 'GET'
        for session in sessions:
            item: dict = dict()
            item['session'] = str(session)
            item['href'] = base_url + '/sessions/' + str(session)
            item['method'] = 'GET'
            data['sessions'].append(item)
    
    return jsonify(data)

@app.route(base_url + '/sessions', methods=['POST'])
def create_session():
    session: Session = backend.create_session()
    storage.add_session(session)
    data = {
        'session': str(session.get_id()),
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session.get_id()),
                'method': 'GET'
            },
            'steps': {
                'href': base_url + '/sessions/' + str(session.get_id()) + '/steps',
                'method': 'GET'
            }
        }
    }
    return jsonify(data)

@app.route(base_url + '/sessions/<uuid:session_id>', methods=['GET'])
@app.route(base_url + '/sessions/<uuid:session_id>/steps', methods=['GET'])
def list_steps(session_id: uuid):
    steps: int = storage.get_nbr_of_steps(session_id)

    if steps < 1:
        abort(404)
    
    data = {
        'session': str(session_id),
        'steps': [],
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session_id),
                'method': 'GET'
            },
            'first': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/1',
                'method': 'GET'
            },
            'last': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(steps),
                'method': 'GET'
            }
        }
    }
    
    for step in range(steps):
        element = {
            'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step + 1),
            'method': 'GET'
        }
        data['steps'].append(element)
        element = None
    
    return jsonify(data)

@app.route(base_url + '/sessions/<uuid:session_id>/steps/<int:step>', methods=['GET'])
@app.route(base_url + '/sessions/<uuid:session_id>/steps/<int:step>/subsessions', methods=['GET'])
def get_step(session_id: uuid, step: int):
    session: Session = storage.get_session(session_id)
    be_step: int = step - 1 # Normalize from web friendly to backend friendly

    if not session:
        abort(404)

    data = {
        'session': str(session_id),
        'step': step,
        'subsessions': list(),
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step),
                'method': 'GET'
            },
            'first': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/1',
                'method': 'GET'
            },
            'last': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(session.nbr_of_steps()),
                'method': 'GET'
            },
            'parent': {
                'href': base_url + '/sessions/' + str(session_id),
                'method': 'GET'
            }
        }
    }
    
    if (step < session.nbr_of_steps()):
        data['links']['next'] = {
            'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step + 1),
            'method': 'GET'
        }
    
    for index in range(session.nbr_of_subsessions_in_step(be_step)):
        element = {
            'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(index + 1),
            'method': 'GET'
        }
        data['subsessions'].append(element)
        element = None

    return jsonify(data)

@app.route(base_url + '/sessions/<uuid:session_id>/steps/<int:step>/subsessions/<int:subsession_id>', methods=['GET'])
@app.route(base_url + '/sessions/<uuid:session_id>/steps/<int:step>/subsessions/<int:subsession_id>/steps', methods=['GET'])
def list_subsession_steps(session_id: uuid, step: int, subsession_id: int):
    session: Session = storage.get_session(session_id)
    subsession: Subsession = None
    be_step: int = step - 1 # Normalize from web friendly to backend friendly
    be_subsession_id: int = subsession_id - 1 # Normalize from web friendly to backend friendly
    
    if not session or not session.get_subsession(be_step, be_subsession_id):
        abort(404)

    subsession = session.get_subsession(be_step, be_subsession_id)
    data = {
        'session': str(session_id),
        'step': step,
        'subsession': subsession_id,
        'subsession_steps': list(),
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id),
                'method': 'GET'
            },
            'first': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/1',
                'method': 'GET'
            },
            'last': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(session.nbr_of_subsessions_in_step(be_step)),
                'method': 'GET'
            },
            'parent': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step),
                'method': 'GET'
            }
        }
    }
    
    if (subsession_id < session.nbr_of_subsessions_in_step(step)):
        data['links']['next'] = {
            'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id + 1),
            'method': 'GET'
        }
    elif step < session.nbr_of_steps():
        data['links']['next_step'] = {
            'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step + 1),
            'method': 'GET'
        }
    
    for index in range(subsession.nbr_of_images()):
        element = {
            'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id) + '/steps/' + str(index + 1),
            'method': 'GET'
        }
        data['subsession_steps'].append(element)
        element = None

    return jsonify(data)

@app.route(base_url + '/sessions/<uuid:session_id>/steps/<int:step>/subsessions/<int:subsession_id>/steps/<int:sub_step>', methods=['GET'])
def get_subsession_step(session_id: uuid, step: int, subsession_id: int, sub_step: int):
    session: Session = storage.get_session(session_id)
    subsession: Subsession = None
    be_step: int = step - 1 # Normalize from web friendly to backend friendly
    be_subsession_id: int = subsession_id - 1 # Normalize from web friendly to backend friendly
    be_sub_step: int = sub_step - 1 # Normalize from web friendly to backend friendly
    
    if not session or not session.get_subsession(be_step, be_subsession_id).get_stream(0).get_image(be_sub_step):
        abort(404)
        
    subsession = session.get_subsession(be_step, be_subsession_id)
    data = {
        'session': str(session_id),
        'step': step,
        'subsession': subsession_id,
        'subsession_step': sub_step,
        'timeout': 0,
        'images': [],
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id) + '/steps/' + str(sub_step),
                'method': 'GET'
            },
            'last': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id) + '/steps/' + str(subsession.nbr_of_images()),
                'method': 'GET'
            },
            'parent': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id),
                'method': 'GET'
            },
            'update': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id) + '/steps/' + str(sub_step),
                'method': 'PUT'
            }
        }
    }
    
    for index in range(subsession.nbr_of_streams()):
        image = subsession.get_stream(index).get_image(be_sub_step)
        classification: tuple = backend.classify(subsession, index, be_sub_step)
        item = {
            'stream': index + 1,
            'image': image,
            'classification': classification[2],
            'labels': labels,
            'image_url': image_base + image,
            'query': classification[3]
        }
        data['images'].append(item)
        item = None
    
    if sub_step < subsession.get_stream(0).size():
        data['timeout'] = step_duration
        data['links']['next'] = {
            'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id) + '/steps/' + str(sub_step + 1),
            'method': 'GET'
        }
    else:
        data['timeout'] = subsession_pause_duration
        data['end_message'] = subsession.get_end_message()
        if subsession_id < session.nbr_of_subsessions_in_step(be_step):
            data['links']['next_subsession'] = {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id + 1),
                'method': 'GET'
            }
        elif step < session.nbr_of_steps():
            data['links']['next_subsession'] = {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step + 1) + '/subsessions/' + str(1),
                'method': 'GET'
            }
        
    return jsonify(data)

@app.route(base_url + '/sessions/<uuid:session_id>/steps/<int:step>/subsessions/<int:subsession_id>/steps/<int:sub_step>', methods=['PUT'])
def update_subsession_step(session_id: uuid, step: int, subsession_id: str, sub_step: int):
    session: Session = storage.get_session(session_id)
    subsession: Subsession = None
    image_data: list = request.get_json()['images']
    images: dict = dict()
    be_step: int = step - 1 # Normalize from web friendly to backend friendly
    be_subsession_id: int = subsession_id - 1 # Normalize from web friendly to backend friendly
    be_sub_step: int = sub_step - 1 # Normalize from web friendly to backend friendly
    
    subsession = session.get_subsession(be_step, be_subsession_id)
    
    for image in image_data:
        images[image['image']] = image
    
    data = {
        'session': str(session_id),
        'step': step,
        'subsession': subsession_id,
        'subsession_step': sub_step,
        'timeout': 0,
        'images': [],
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id) + '/steps/' + str(sub_step),
                'method': 'GET'
            },
            'last': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id) + '/steps/' + str(subsession.nbr_of_images()),
                'method': 'GET'
            },
            'parent': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id),
                'method': 'GET'
            },
            'update': {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id) + '/steps/' + str(sub_step),
                'method': 'PUT'
            }
        }
    }
    
    for index in range(subsession.nbr_of_streams()):
        image = subsession.get_stream(index).get_image(be_sub_step)
        sample = utils.load_data_sample(image)
        subsession = backend.update(subsession,
            index,
            image,
            sample[1],
            subsession.get_stream(index).get_prediction(image),
            images[image]['classification'],
            bool(images[image]['query']))
        item = {
            'stream': index + 1,
            'image': image,
            'classification': images[image]['classification'],
            'labels': labels,
            'image_url': image_base + image,
            'query': bool(images[image]['query'])
        }
        data['images'].append(item)
        item = None
    
    if sub_step < subsession.get_stream(0).size():
        data['timeout'] = step_duration
        data['end_message'] = subsession.get_end_message()
        data['links']['next'] = {
            'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id) + '/steps/' + str(sub_step + 1),
            'method': 'GET'
        }
    else:
        storage.save_results(subsession)
        #storage.update_session(session)
        data['timeout'] = subsession_pause_duration
        data['end_message'] = subsession.get_end_message()
        if (subsession_id < session.nbr_of_subsessions_in_step(be_step)):
            data['links']['next_subsession'] = {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step) + '/subsessions/' + str(subsession_id + 1),
                'method': 'GET'
            }
        elif step < session.nbr_of_steps():
            data['links']['next_subsession'] = {
                'href': base_url + '/sessions/' + str(session_id) + '/steps/' + str(step + 1) + '/subsessions/' + str(1),
                'method': 'GET'
            }
        
        
    return jsonify(data)


if __name__ == '__main__':
    if mode == 'development':
        app.run(host=host, port=port)
    elif mode == 'production':
        serve(app, host=host, port=port)