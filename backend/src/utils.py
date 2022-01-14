from nanoid import generate
import pickle
import random

# Path to folder were the static data is stored, file with feature data, etc.
data_path = 'data/'
data_features_name = 'features.pickle'
im_indices_name = 'im_indices.pickle'

# Path to folder were all data used during the session is used, ML models, etc.
session_path = 'session_data/'

# Path to folder were all results are stored
results_path = 'results/'

#generate unique ID for session
def generate_session_id():
    session_id = generate()
    return session_id

def create_filename(session_id, session_step, i, object_type):

    path = results_path if object_type == 'results' else session_path
    filename = '{0}{1}_{2}_{3}_{4}.pickle'.format(path, session_id, session_step, i, object_type)

    return filename

def shuffle_im_order():

    filename = data_path + im_indices_name #update to load file
    im_list = pickle.load(open(filename, 'rb'))

    random.shuffle(im_list)

    return im_list

def next_im_id(session_id, session_step, subsession_id):
    filename = create_filename(session_id, session_step, subsession_id, 'im_order')
    im_order = pickle.load(open(filename, 'rb'))

    filename = create_filename(session_id, session_step, subsession_id, 'im_index')
    im_index = pickle.load(open(filename, 'rb'))

    im_id = im_order[im_index]

    return im_id

def load_data_sample(im_id):
    filename = data_path + data_features_name #update to load file
    data_features = pickle.load(open(filename, 'rb'))
    data_sample = data_features[im_id]['features']
    y_true = data_features[im_id]['class']

    return data_sample, y_true