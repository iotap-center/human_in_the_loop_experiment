from flask import jsonify, request, send_from_directory
import uuid

base_url: str = '/api/v1'
frontend_dir: str = '../../frontend'

def list_sessions():
    data = {
        'sessions': [
            {
                'session': '16fd2706-8baf-433b-82eb-8c7fada847da',
                'href': base_url + '/sessions/16fd2706-8baf-433b-82eb-8c7fada847da',
                'method': 'GET'
            }
        ],
        'links': {
            'self': {
                'href': base_url + '/sessions',
                'method': 'GET'
            },
            'first': {
                'href': base_url + '/sessions/16fd2706-8baf-433b-82eb-8c7fada847da',
                'method': 'GET'
            },
            'last': {
                'href': base_url + '/sessions/16fd2706-8baf-433b-82eb-8c7fada847da',
                'method': 'GET'
            },
            'create': {
                'href': base_url + '/sessions',
                'method': 'POST'
            }
        }
    }
    return jsonify(data)

def create_session():
    session: UUID = uuid.uuid4()
    print("Ny session: " + str(session))
    data = {
        'session': str(session),
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session),
                'method': 'GET'
            },
            'steps': {
                'href': base_url + '/sessions/' + str(session) + '/steps',
                'method': 'GET'
            }
        }
    }
    return jsonify(data)

def list_steps(session: uuid):
    data = {
        'session': str(session),
        'steps': [
            base_url + '/sessions/' + str(session) + '/steps/1',
            base_url + '/sessions/' + str(session) + '/steps/2',
            base_url + '/sessions/' + str(session) + '/steps/3',
            base_url + '/sessions/' + str(session) + '/steps/4'
        ],
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session) + '/steps',
                'method': 'GET'
            },
            'first': {
                'href': base_url + '/sessions/' + str(session) + '/steps/1',
                'method': 'GET'
            },
            'last': {
                'href': base_url + '/sessions/' + str(session) + '/steps/4',
                'method': 'GET'
            }
        }
    }
    return jsonify(data)

def get_step(session: uuid, step: int):
    data = {
        'session': str(session),
        'step': 1,
        'subsessions': [
            {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/1',
                'method': 'GET'
            },
            {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/2',
                'method': 'GET'
            }
        ],
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step),
                'method': 'GET'
            },
            'first': {
                'href': base_url + '/sessions/' + str(session) + '/steps/1',
                'method': 'GET'
            },
            'next': {
                'href': base_url + '/sessions/' + str(session) + '/steps/2',
                'method': 'GET'
            },
            'last': {
                'href': base_url + '/sessions/' + str(session) + '/steps/4',
                'method': 'GET'
            },
            'parent': {
                'href': base_url + '/sessions/' + str(session),
                'method': 'GET'
            }
        }
    }
    return jsonify(data)

def list_subsession_steps(session: uuid, step: int, subsession: int):
    data = {
        'session': str(session),
        'step': 1,
        'subsession': subsession,
        'subsession_steps': [
            {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/1',
                'method': 'GET'
            },
            {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/2',
                'method': 'GET'
            },
            {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/3',
                'method': 'GET'
            },
            {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/4',
                'method': 'GET'
            },
            {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/5',
                'method': 'GET'
            }
        ],
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession),
                'method': 'GET'
            },
            'first': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/1',
                'method': 'GET'
            },
            'next': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/2',
                'method': 'GET'
            },
            'last': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/2',
                'method': 'GET'
            },
            'parent': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step),
                'method': 'GET'
            }
        }
    }
    return jsonify(data)

def get_subsession_step(session: uuid, step: int, subsession: int, substep: int):
    data = {
        'session': str(session),
        'step': 1,
        'subsession': subsession,
        'subsession_step': substep,
        'images': [
            {
                'stream': 1,
                'image': 'dummy.cat.jpg',
                'labels': ['katt', 'hund'],
                'classification': -1,
                'image_url': '/images/dummy.cat.jpg'
            },
            {
                'stream': 2,
                'image': 'dummy.ball.jpg',
                'labels': ['puck', 'boll'],
                'classification': -1,
                'image_url': '/images/dummy.ball.png'
            },
            {
                'stream': 3,
                'image': 'dummy.apple.jpg',
                'labels': ['äpple', 'banan'],
                'classification': -1,
                'image_url': '/images/dummy.apple.jpg'
            },
            {
                'stream': 4,
                'image': 'dummy.bat.jpg',
                'labels': ['fladdermus', 'tjuv'],
                'classification': -1,
                'image_url': '/images/dummy.bat.jpg'
            }
        ],
        'timeout': 5,
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/1',
                'method': 'GET'
            },
            'next': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/2',
                'method': 'GET'
            },
            'last': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/5',
                'method': 'GET'
            },
            'parent': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession),
                'method': 'GET'
            },
            'update': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/1',
                'method': 'PUT'
            }
        }
    }
    return jsonify(data)

def update_subsession_step(session: uuid, step: int):
    images = request.get_json()['images']

    data = {
        'session': str(session),
        'step': 1,
        'subsession': '1.1',
        'images': [
            {
                'stream': 1,
                'image': 'dummy.cat.jpg',
                'labels': ['katt', 'hund'],
                'classification': 0,
                'image_url': '/images/dummy.cat.jpg'
            },
            {
                'stream': 2,
                'image': 'dummy.ball.jpg',
                'labels': ['puck', 'boll'],
                'classification': 1,
                'image_url': '/images/dummy.ball.png'
            },
            {
                'stream': 3,
                'image': 'dummy.apple.jpg',
                'labels': ['äpple', 'banan'],
                'classification': 0,
                'image_url': '/images/dummy.apple.jpg'
            },
            {
                'stream': 4,
                'image': 'dummy.bat.jpg',
                'labels': ['fladdermus', 'tjuv'],
                'classification': 0,
                'image_url': '/images/dummy.bat.jpg'
            }
        ],
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/1',
                'method': 'GET'
            },
            'next': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/2',
                'method': 'GET'
            },
            'next': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/5',
                'method': 'GET'
            },
            'parent': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession),
                'method': 'GET'
            },
            'update': {
                'href': base_url + '/sessions/' + str(session) + '/steps/' + str(step) + '/subsessions/' + str(subsession) + '/steps/1',
                'method': 'PUT'
            }
        }
    }
    return jsonify(data)
