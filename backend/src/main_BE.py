# import the necessary packages
from creme.linear_model import LogisticRegression
from creme.multiclass import OneVsRestClassifier
from creme.preprocessing import StandardScaler
from creme.compose import Pipeline
from creme.metrics import Accuracy
from creme import stream
import numpy as np
import glob
import time
import utils as utils
import pickle
import uuid

def create_session_id() -> uuid:

    #generate unique session ID
    return uuid.uuid4()

def create_session_data(session_id: uuid, session_step: int, n: int) -> None:

    #generate and save n classifiers, iamge orders and result lists
    for subsession_id in range(n):
        model = Pipeline(
            StandardScaler(),
            OneVsRestClassifier(classifier=LogisticRegression())
        )
        filename = utils.create_filename(session_id, session_step, subsession_id, 'model')
        pickle.dump(model, open(filename, 'wb'))

        im_order = utils.shuffle_im_order()
        filename = utils.create_filename(session_id, session_step, subsession_id, 'im_order')
        pickle.dump(im_order, open(filename, 'wb'))

        im_index = 0
        filename = utils.create_filename(session_id, session_step, subsession_id, 'im_index')
        pickle.dump(im_index, open(filename, 'wb'))

        results = []
        filename = utils.create_filename(session_id, session_step, subsession_id, 'results')
        pickle.dump(results, open(filename, 'wb'))

def classify(session_id: uuid, session_step: int, subsession_id: int) -> tuple:
    #load correct model
    filename = utils.create_filename(session_id, session_step, subsession_id, 'model')
    model = pickle.load(open(filename, 'rb'))

    #load image data and get next image ID
    im_id = utils.next_im_id(session_id, session_step, subsession_id)
    data_sample, y_true = utils.load_data_sample(im_id)

    #classify the image
    pred = model.predict_one(data_sample)

    return im_id, y_true, pred

def save_and_update(
        session_id: uuid,
        session_step: int,
        subsession: int,
        im_id: int,
        y_true: bool,
        pred: int,
        user_input: int) -> None:
    #load correct model
    filename = utils.create_filename(session_id, session_step, subsession, 'model')
    model = pickle.load(open(filename, 'rb'))

    #update and save model
    data_sample, y_true = utils.load_data_sample(im_id)
    model = model.fit_one(data_sample, user_input)
    pickle.dump(model, open(filename, 'wb'))

    #update result data
    filename = utils.create_filename(session_id, session_step, subsession, 'results')
    results = pickle.load(open(filename, 'rb'))
    results.append([im_id, y_true, pred, user_input]) #add time????
    pickle.dump(results, open(filename, 'wb'))

    return


