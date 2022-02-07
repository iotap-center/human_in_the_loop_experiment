# import the necessary packages
from creme.linear_model import LogisticRegression
from creme.multiclass import OneVsRestClassifier
from creme.preprocessing import StandardScaler
from creme.compose import Pipeline
from creme.metrics import Accuracy
from creme import stream
from session import Session, Subsession, Strategy, Stream
import numpy as np
import glob
import time
import utils as utils
import uuid
import configparser

config = configparser.ConfigParser()
config.read('config/app.ini')

def create_session(nbr_of_steps: int = 0, nbr_of_images: int = 0) -> Session:
    """Creates and populates a Session object. If the arguments aren't set,
    they will be read from the config file
    
    Keyword arguments:
    nbr_of_steps -- The number of steps used in this session
    nbr_of_images -- The number of images used in each subsession stream
    """

    # Checking arguments
    if nbr_of_steps < 1:
        nbr_of_steps = int(config['backend']['default_nbr_of_steps'])
    if nbr_of_images < 1:
        nbr_of_images = int(config['backend']['default_nbr_of_images'])

    # Setting up the data structure
    session: Session = Session(create_session_id(), nbr_of_steps)
    
    # Step 1
    session.add_subsession(0, create_subsession(session, 0, Strategy.MT, 1, nbr_of_images, "In the next part you will see 1 image at a time again, but this image will not be displayed all the time (when it is not displayed you cannot provide feedback)."));
    session.add_subsession(0, create_subsession(session, 0, Strategy.ALMT, 1, nbr_of_images, "In the next part you will see 3 images at a time."));
    
    # Step 2
    session.add_subsession(1, create_subsession(session, 1, Strategy.MT, 3, nbr_of_images, "In the next part you will see 3 images at a time again, but the images will not be displayed all the time (when it is not displayed you cannot provide feedback)."));
    session.add_subsession(1, create_subsession(session, 1, Strategy.ALMT, 3, nbr_of_images, "In the next part you will see 6 images at a time."));
    
    # Step 3
    session.add_subsession(2, create_subsession(session, 2, Strategy.MT, 6, nbr_of_images, "In the next part you will see 6 images at a time again, but the images will not be displayed all the time (when it is not displayed you cannot provide feedback)."));
    session.add_subsession(2, create_subsession(session, 2, Strategy.ALMT, 6, nbr_of_images, "In the next part you will see 9 images at a time."));
    
    # Step 4
    session.add_subsession(3, create_subsession(session, 3, Strategy.MT, 9, nbr_of_images, "In the next part you will see 9 images at a time again, but the images will not be displayed all the time (when it is not displayed you cannot provide feedback)."));
    session.add_subsession(3, create_subsession(session, 3, Strategy.ALMT, 9, nbr_of_images, "<p>That was the last part, thank you for your participation in the experiments!</p><p>Agnes Tegen, Paul Davidsson and Jan Persson</p>"));
    
    return session

def create_session_id() -> uuid:
    """Generates a unique session ID"""
    return uuid.uuid4()

def create_subsession(
        session: Session,
        session_step: int,
        strategy: Strategy,
        nbr_of_streams: int,
        nbr_of_images: int,
        end_message: str) -> Subsession:
    """Creates and populates a Subsession object.
    
    Keyword arguments:
    session -- The session that this subsession belongs to
    session_step -- The step session step that this subsession belongs to
    strategy -- The strategy used to predict the image contents in this subsession
    nbr_of_streams -- The number of streams used in this subsession
    nbr_of_images -- The number of images in each subsession stream
    """
    subsession: Subsession = Subsession(session_step, session, strategy, nbr_of_streams, nbr_of_images)
    subsession.set_end_message(end_message)
    
    #generate and save nbr_of_streams classifiers, image orders and result lists
    for stream_id in range(nbr_of_streams):
        model = Pipeline(
            StandardScaler(),
            OneVsRestClassifier(classifier=LogisticRegression()))
        stream = Stream(nbr_of_images)
        stream.set_images(utils.shuffle_im_order(nbr_of_images))
        stream.set_model(model)
        subsession.set_stream(stream_id, stream)

        if strategy == Strategy.ALMT:
            subsession.set_parameters([1, 0.05])
        model = None

    return subsession

def classify(
        subsession: Subsession,
        stream_id: int,
        subsession_step: int) -> tuple:
    """Classifies the contents of an image.
    
    Keyword arguments:
    subsession -- The subsession in which the image is located
    stream_id -- The stream in which the image is located
    subsession_step -- The position within the stream where we'll find our image
    """
    #load correct model
    model = subsession.get_stream(stream_id).get_model()

    #load image data and get next image ID
    images = subsession.get_stream(stream_id).get_images()
    image_id = images[subsession_step]
    data_sample, y_true = utils.load_data_sample(image_id)

    #classify the image
    prediction = model.predict_one(data_sample)
    subsession.get_stream(stream_id).set_prediction(image_id, prediction)

    #check if image should be shown to user
    if subsession.get_strategy() == Strategy.ALMT:
        query, parameters = utils.AL_uncertainty(
            subsession.get_stream(stream_id).get_model(),
            subsession.get_parameters(),
            data_sample,
            prediction)
        subsession.set_parameters(parameters)
    elif subsession.get_strategy() == Strategy.MT:
        query = True

    return image_id, y_true, prediction, query

def update(
        subsession: Subsession,
        stream_id: int,
        image_id: str,
        y_true: int,
        prediction: int,
        user_input: int,
        query: bool) -> Subsession:
    """Updates the model used to predict a stream's images.
    
    Keyword arguments:
    subsession -- The subsession wherein we'll find our model and images
    stream_id -- The stream that we're interested in
    image_id -- The image used for this training sample
    y_true -- The classification of this image
    prediction -- The prediction of this image based on the model
    user_input -- The user's classification of this image
    query -- Tells whether the model should be updated or not. If false, the
    result will just be recorded.
    """
    if query:
        # load correct model
        model = subsession.get_stream(stream_id).get_model()

        # update and save model
        data_sample, y_true = utils.load_data_sample(image_id)
        model = model.fit_one(data_sample, user_input)
        subsession.get_stream(stream_id).set_model(model)

    # update result data
    # add time????
    subsession.get_stream(stream_id).add_result([image_id, y_true, prediction, user_input])

    return subsession
