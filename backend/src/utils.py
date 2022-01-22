from session import Strategy
import pickle
import random
import uuid

# Path to folder were the static data is stored, file with feature data, etc.
data_path = 'data/'
data_features_name = 'features.pickle'
im_indices_name = 'im_indices.pickle'

# Path to folder were all data used during the session is used, ML models, etc.
session_path = 'session_data/'

# Path to folder were all results are stored
results_path = 'results/'

# Features file
data_features: list = None

def init() -> None:
    global data_features
    filename = data_path + data_features_name #update to load file
    data_features = pickle.load(open(filename, 'rb')) #UPDATE!!!!!!!!!!

def create_filename(
        session_id: uuid,
        session_step: int,
        strategy: Strategy,
        object_type: str
    ) -> str:

    path = results_path if object_type == 'results' else session_path
    filename = '{0}{1}_{2}_{3}_{4}.pickle'.format(path, session_id, session_step, str(strategy), object_type)

    return filename

def shuffle_im_order(max_images: int):

    filename = data_path + im_indices_name #update to load file
    image_list = pickle.load(open(filename, 'rb'))

    random.shuffle(image_list)

    return image_list[0:(max_images)]

#def next_im_id(
#        session_id: uuid,
#        session_step: int,
#        strategy: Strategy,
#        subsession_id: int) -> str:
#    filename = create_filename(session_id, session_step, strategy, subsession_id, 'im_order')
#    im_order = pickle.load(open(filename, 'rb'))
#
#    filename = create_filename(session_id, session_step, strategy, subsession_id, 'im_index')
#    im_index = pickle.load(open(filename, 'rb'))
#
#    im_id = im_order[im_index]
#
#    return im_id

def load_data_sample(image_id: str) -> tuple:
    data_sample = data_features[image_id]['features']
    y_true = data_features[image_id]['class']

    return data_sample, y_true

def AL_uncertainty(
        model,
        AL_param,
        data_sample: list,
        prediction: int) -> tuple:
    probs = model.predict_proba_one(data_sample)
    if len(probs.keys()) < 2:
        query = True
    else:
        prob = probs[prediction]
        if prob < AL_param[0]:
            query = True
            AL_param[0] = AL_param[0] - AL_param[1]
        else:
            query = False
            AL_param[0] = AL_param[0] + AL_param[1]
    
    return query, AL_param

init()
