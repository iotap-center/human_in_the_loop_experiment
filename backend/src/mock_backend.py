from flask import jsonify, request, send_from_directory
import uuid

base_url: str = '/api/v1'
frontend_dir: str = '../../frontend'

def list_sessions():
    data = {
        'sessions': [
            {
                'session': '16fd2706-8baf-433b-82eb-8c7fada847da',
                'uri': base_url + '/sessions/16fd2706-8baf-433b-82eb-8c7fada847da'
            }
        ],
        'links': {
            'self': {
                'href': base_url + '/sessions/',
                'method': 'GET'
            },
            'first': {
                'href': base_url + '/sessions/16fd2706-8baf-433b-82eb-8c7fada847da',
                'method': 'GET'
            },
            'create': {
                'href': base_url + '/sessions/',
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
            'first': {
                'href': base_url + '/sessions/' + str(session) + '/steps/1',
                'method': 'GET'
            }
        }
    }
    return jsonify(data)

def get_steps(session: uuid):
    data = {
        'session': str(session),
        'steps': [
            base_url + '/sessions/' + str(session) + '/steps/1',
            base_url + '/sessions/' + str(session) + '/steps/2',
            base_url + '/sessions/' + str(session) + '/steps/3',
            base_url + '/sessions/' + str(session) + '/steps/4',
            base_url + '/sessions/' + str(session) + '/steps/5'
        ],
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session) + '/steps',
                'method': 'GET'
            },
            'first': {
                'href': base_url + '/sessions/' + str(session) + 'steps/1',
                'method': 'GET'
            },
            'last': {
                'href': base_url + '/sessions/' + str(session) + 'steps/5',
                'method': 'GET'
            }
        }
    }
    return jsonify(data)

def get_step(session: uuid, step: int):
    data = {
        'session': str(session),
        'step': 1,
        'images': [
            {
                'subsession': 1,
                'image': 'dummy.cat.jpg',
                'labels': ['katt', 'hund'],
                'prediction': 0,
                'classification': -1,
                'image_url': '/images/dummy.cat.jpg'
            },
            {
                'subsession': 2,
                'image': 'dummy.ball.jpg',
                'labels': ['puck', 'boll'],
                'prediction': 1,
                'classification': -1,
                'image_url': '/images/dummy.ball.png'
            },
            {
                'subsession': 3,
                'image': 'dummy.apple.jpg',
                'labels': ['äpple', 'banan'],
                'prediction': 0,
                'classification': -1,
                'image_url': '/images/dummy.apple.jpg'
            },
            {
                'subsession': 4,
                'image': 'dummy.bat.jpg',
                'labels': ['fladdermus', 'tjuv'],
                'prediction': 1,
                'classification': -1,
                'image_url': '/images/dummy.bat.jpg'
            }
        ],
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session) + '/steps/1',
                'method': 'GET'
            },
            'next': {
                'href': base_url + '/sessions/' + str(session) + '/steps/2',
                'method': 'GET'
            },
            'update': {
                'href': base_url + '/sessions/' + str(session) + '/steps/1',
                'method': 'PUT'
            }
        }
    }
    return jsonify(data)

def update_step(session: uuid, step: int):
    images = request.get_json()['images']

    data = {
        'session': str(session),
        'step': 1,
        'images': [
            {
                'subsession': 1,
                'image': 'dummy.cat.jpg',
                'labels': ['katt', 'hund'],
                'prediction': 0,
                'classification': 0,
                'image_url': '/images/dummy.cat.jpg'
            },
            {
                'subsession': 2,
                'image': 'dummy.ball.jpg',
                'labels': ['puck', 'boll'],
                'prediction': 1,
                'classification': 1,
                'image_url': '/images/dummy.ball.png'
            },
            {
                'subsession': 3,
                'image': 'dummy.apple.jpg',
                'labels': ['äpple', 'banan'],
                'prediction': 0,
                'classification': 0,
                'image_url': '/images/dummy.apple.jpg'
            },
            {
                'subsession': 4,
                'image': 'dummy.bat.jpg',
                'labels': ['fladdermus', 'tjuv'],
                'prediction': 1,
                'classification': 0,
                'image_url': '/images/dummy.bat.jpg'
            }
        ],
        'links': {
            'self': {
                'href': base_url + '/sessions/' + str(session) + '/steps/1',
                'method': 'GET'
            },
            'next': {
                'href': base_url + '/sessions/' + str(session) + '/steps/2',
                'method': 'GET'
            },
            'update': {
                'href': base_url + '/sessions/' + str(session) + '/steps/1',
                'method': 'PUT'
            }
        }
    }
    return jsonify(data)
