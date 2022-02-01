from session import Strategy
import configparser
import pickle
import random
import uuid

config = configparser.ConfigParser()
config.read('config/app.ini')

# Path to folder were the static data is stored, file with feature data, etc.
data_path = config['backend']['data_path']
data_features_name = config['backend']['data_features_name']
im_indices_name = config['backend']['im_indices_name']

# Features file
data_features: list = None

def init() -> None:
    """Initializes the backend by loading the data featues file."""
    global data_features
    filename = data_path + data_features_name #update to load file
    data_features = pickle.load(open(filename, 'rb')) #UPDATE!!!!!!!!!!

def shuffle_im_order(max_images: int) -> list:
    """Generates a randomized list of images of a specified size.
    
    Keyword arguments:
    max_images -- The size of the image list
    """
    filename = data_path + im_indices_name #update to load file
    image_list = pickle.load(open(filename, 'rb'))

    random.shuffle(image_list)

    return image_list[0:(max_images)]

def load_data_sample(image_id: str) -> tuple:
    """Loads a data sample for the data set.
    
    Keyword arguments:
    image_id -- The name of an image
    """
    data_sample = data_features[image_id]['features']
    y_true = data_features[image_id]['class']

    return data_sample, y_true

def AL_uncertainty(
        model,
        AL_param,
        data_sample: list,
        prediction: int) -> tuple:
    """Calculates the uncertainity level of a prediction.
    
    Keyword arguments:
    model -- The model used for a prediction
    AL_param -- The parameters used for an active learning session
    data_sample -- The sample on which the prediction is performed
    prediction -- The prediction made for a sample
    """
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
