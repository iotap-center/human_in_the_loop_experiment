from enum import Enum
from creme.compose import Pipeline
import uuid

# This is an ugly hack used to  satisfy some internal dependencies
Session = type('Session', (object,), {})
Subsession = type('Session', (object,), {})

class Strategy(Enum):
    """This enum class represents the available strategies used in the
    experiment. We use enums to mitigate errors stemming from hard coded
    string values.
    """
    
    MT: str = 'MT'
    ALMT: str = 'ALMT'

class Stream:
    """A stream represents a sequence of images, coupled with their predictions
    (when calculated), and the results from a user interaction. Each stream
    adheres to a single model.
    """
    
    def __init__(self, size: int) -> None:
        """Initializes a stream of size elements.
        
        Keyword arguments:
        size -- The number of images that this stream will contain
        """
        self.__model = None
        self.__images: list = [None] * size
        self.__predictions: dict = dict()
        self.__results: dict = dict()

    def set_model(self, model: Pipeline) -> None:
        """Sets the model used by this stream.
        
        Keyword arguments:
        model -- The model is a Creme pipeline.
        """
        self.__model = model

    def get_model(self) -> Pipeline:
        return self.__model

    def set_images(self, images: list) -> None:
        """Sets a sorted list of images. Useful for e.g. batches from util's
        image randomizer.
        
        Keyword arguments:
        images -- A list of strings, each being the name of an image file.
        """
        self.__images = images

    def get_images(self) -> list:
        return self.__images

    def get_image(self, index: int) -> str:
        """Returns a single image from the stream.
        
        Keyword arguments:
        index -- The position of the image we want to know. The index starts at 0.
        """
        try:
            return self.__images[index]
        except:
            return None

    def set_prediction(self, image_id: str, prediction: int) -> None:
        """Sets the prediction made for an image.
        
        Keyword arguments:
        image_id -- The name of the image.
        prediction -- The prediction made by a classifier.
        """
        self.__predictions[image_id] = prediction

    def get_prediction(self, image_id: str) -> int:
        """Returns the prediction for an image.
        
        Keyword arguments:
        image_id -- The name of the image we're interested in.
        """
        try:
            return self.__predictions[image_id]
        except:
            return -1
        
    def add_result(self, result: list) -> None:
        """Adds the results from a user interaction.
        
        Keyword arguments:
        result -- a list on the form
                [image_id: str,
                 y_true: int,
                 prediction: int,
                 user_input: int]
        """
        self.__results[result[0]] = result

    def set_results(self, results: dict) -> None:
        """Sets a complete list of results. Useful for e.g. deserialization.
        
        Keyword arguments:
        results -- a dictionary of values as described in add_value(list).
        """
        self.__results = results

    def get_results(self) -> dict:
        """Returns the complete results dictionary."""
        return self.__results

    def get_result(self, image_id: str) -> list:
        """Returns a single result.
        
        Keyword arguments:
        image_id - The name of an image
        """
        try:
            return self.__results[image_id]
        except:
            return None
    
    def serialize_results(self) -> list:
        return list(self.__results.values())

    def size(self) -> int:
        return len(self.__images)

class Subsession:
    """Represents a subsession, i.e., a set of image streams sharing a common
    strategy. A subsession belongs to a session step.
    """
    
    def __init__(self,
            session_step: int,
            session: Session,
            strategy: Strategy,
            nbr_of_streams: int,
            nbr_of_slots: int) -> None:
        """Initializes a new subsession.
        
        Keyword arguments:
        session_step -- The session step that this subsession belongs to
        session -- The session that this subsession belongs to
        strategy -- The strategy used to predict the image contents in this subsession
        nbr_of_streams -- The number of streams that will be used in in this subsession
        nbr_of_slots -- The number of images used in the streams
        """
        self.__session_step: int = session_step
        self.__session: Session = session
        self.__strategy: Strategy = strategy
        self.__end_message: str = ""
        self.__parameters: list = list()
        self.__streams: list = list()
        for i in range(nbr_of_streams):
            self.__streams.append(Stream(nbr_of_slots))

    def get_session_step(self) -> int:
        return self.__session_step

    def get_strategy(self) -> Strategy:
        return self.__strategy

    def set_session(self, session: Session) -> None:
        """Sets the session that this subsession belongs to. Useful for e.g. deserialization.
        
        Keyword arguments:
        session -- The session that this subsession belongs to
        """
        self.__session = session

    def get_session(self) -> Session:
        """ Returns the session that this subsession belongs to."""
        return self.__session

    def set_end_message(self, end_message: str) -> None:
        """Sets the end message that follows upon the completion of this sub session.

        Keyword arguments:
        end_message -- The message to display
        """
        self.__end_message = end_message
    
    def get_end_message(self) -> str:
        """Returns the end message"""
        return self.__end_message

    def set_stream(self, stream_id: int, stream: Stream) -> None:
        """Sets a complete stream. Useful for e.g. deserialization.
        
        Keyword arguments:
        stream_id -- The id of the stream
        stream -- The stream that we want to set
        """
        try:
            self.__streams[stream_id] = stream
        except:
            return

    def get_stream(self, stream_id: int) -> Stream:
        """Returns a full stream.
        
        Keyword arguments:
        stream_id -- The id of the stream that we want
        """
        try:
            return self.__streams[stream_id]
        except:
            return None

    def get_streams(self) -> Stream:
        return self.__streams

    def set_model(self, stream_id: int, model: Pipeline) -> None:
        """Sets the model used to predict the images a stream.
        If not found, None is returned.
        
        Keyword arguments:
        stream_id -- The stream that we'll predict in
        model -- A Creme pipeline
        """
        try:
            self.__streams[stream_id].set_model(model)
        except:
            return None

    def get_model(self, stream_id: int) -> Pipeline:
        """Returns the model used to predict in a stream.
        If not found, None is returned.
        
        Keyword arguments:
        stream_id -- The stream that we're interested in
        """
        try:
            return self.__streams[stream_id].get_model()
        except:
            return None

    def set_parameters(self, parameters: list) -> None:
        """Sets the parameters used when predicting according to the AL+MT model.
        
        Keyword arguments:
        parameters -- A list of an integer and a float value, e.g., [1, 1.07]
        """
        self.__parameters = parameters

    def get_parameters(self) -> list:
        return self.__parameters

    def nbr_of_images(self) -> int:
        """Returns the number of images in this subsession's streams."""
        return self.__streams[0].size()

    def nbr_of_streams(self) -> int:
        """Returns the number of streams in this subsession."""
        return len(self.__streams)
    
    def serialize_results(self) -> list:
        results = list()
        for stream in self.__streams:
            results = results + stream.serialize_results()
        return results

    def serialize(self) -> dict:
        """Converts this subsession object to a dictionary. Returns None if unsuccessful."""
        subsession_data: dict = dict()
        subsession_data['end_message'] = self.__end_message
        try:
            for stream_id in range(len(self.__streams)):
                subsession_data[stream_id] = dict()
                subsession_data[stream_id]['model'] = self.__streams[stream_id].get_model()
                subsession_data[stream_id]['im_order'] = self.__streams[stream_id].get_images()
                subsession_data[stream_id]['im_index'] = len(self.__streams)
                subsession_data[stream_id]['results'] = list(self.__streams[stream_id].get_results().values())
                subsession_data[stream_id]['session_id'] = str(self.__session.get_id())
                subsession_data[stream_id]['session_step'] = self.__session_step
                subsession_data[stream_id]['maxImages'] = self.__streams[stream_id].size()
                subsession_data[stream_id]['strategy'] = str(self.__strategy)
                if self.__strategy == Strategy.ALMT:
                    subsession_data[stream_id]['param'] = self.__parameters
                else:
                    subsession_data[stream_id]['param'] = list()
            return subsession_data
        except:
            return None

    @classmethod
    def deserialize(cls, subsession_data: dict) -> Subsession:
        """Creates a Subsession object from a serialization dictionary.
        Returns None if unsuccessful.
        
        Keyword arguments:
        subsession_data -- A dictionary generated by serialize()
        """
        try:
            subsession: Subsession = Subsession(
                    subsession_data[0]['session_step'],
                    None,
                    Strategy[subsession_data[0]['strategy']],
                    len(subsession_data),
                    subsession_data[0]['maxImages'])
            subsession.set_end_message(subsession_data['end_message'])
            subsession.set_current_index(subsession_data[0]['im_index'])
            subsession.set_parameters(subsession_data[0]['param'])
            for stream_id in range(len(subsession_data)):
                stream: Stream = Stream(subsession_data[stream_id]['maxImages'])
                stream.set_images(subsession_data[stream_id]['im_order'])
                stream.set_results(subsession_data[stream_id]['results'])
                subsession.set_stream(stream_id, stream)
        except:
            return None

class Session:
    """Represents a session, consising of a number of steps. Each step consists
    of a number of subsessions, each containing a number of image streams.
    """
    
    def __init__(self,
            session_id: uuid,
            steps: int) -> None:
        """Initializes a session object.
        
        Keyword arguments:
        session_id -- A universally unique id identifying this session
        steps -- The number of steps used in this session.
        """
        self.__id: uuid = session_id
        self.__steps: list = [None] * steps
        for step in range(steps):
            self.__steps[step] = list()

    def get_id(self) -> uuid:
        return self.__id

    def add_subsession(self,
            step_id: int,
            subsession: Subsession) -> None:
        """Adds a subsession to a step.
        
        Keyword arguments:
        step_id -- The step where we want to put the subsession
        subsession -- The subsession we want to add
        """
        self.__steps[step_id].insert(subsession.get_session_step(), subsession)

    def get_step(self, step_id: int) -> list:
        """Returns a list of subsession objects. If not found, None is returned.
        
        Keyword arguments:
        step_id -- The step that we're interested in
        """
        try:
            return self.__steps[step_id]
        except:
            return None
    
    def get_steps(self) -> list:
        return self.__steps

    def nbr_of_steps(self) -> int:
        return len(self.__steps)

    def nbr_of_subsessions_in_step(self, step_id: int) -> int:
        """Returns the number of subsessions in a specified step.
        If not found, 0 is returned.
        
        Keyword arguments:
        step_id -- The step that we're interested in
        """
        try:
            return len(self.__steps[step_id])
        except:
            return 0

    def get_subsession(self, step_id: int, subsession_id: int) -> Subsession:
        """Returns a specified subsession. If not found, None is returned.
        
        Keyword arguments:
        step_id -- The step that our subsession is located in
        subsession_id -- The id of the subsession that we're interested in
        """
        try:
            return self.__steps[step_id][subsession_id]
        except:
            return None
    
    def serialize(self) -> dict:
        """Converts this session object to a dictionary. Returns None if unsuccessful."""
        session_data: dict = dict()
        try:
            session_data['session_id'] = str(self.__id)
            session_data['steps'] = list()
            for step in range(len(session_data['steps'])):
                session_data.append(dict())
                for subsession in self.__steps[step]:
                    session_data['steps'][step] = self.__steps[step][subsession].serialize()
            return session_data
        except:
            return None
    
    @classmethod
    def deserialize(cls, data: dict) -> Session:
        """Creates a Session object from a serialization dictionary.
        Returns None if unsuccessful.
        
        Keyword arguments:
        data -- A dictionary generated by serialize()
        """
        try:
            session: Session = Session(uuid.UUID(int=data['session_id']), len(data['steps']))
            for step in range(session.nbr_of_steps()):
                for subsession_index in range(len(data['steps'])):
                    subsession: Subsession = Subsession.deserialize(data['steps'][subsession_index])
                    subsession.set_session(session)
                    session.add_subsession(step, subsession)
            return session
        except:
            return None
