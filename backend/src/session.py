from enum import Enum
import uuid

# This is an ugly hack used to  satisfy some dependencies
Session = type('Session', (object,), {})
Subsession = type('Session', (object,), {})

class Strategy(Enum):
    """
    """
    
    MT: str = 'MT'
    ALMT: str = 'ALMT'

class Stream:
    """
    """
    
    def __init__(self, size: int) -> None:
        """
        """
        self.__model = None
        self.__images: list = [None] * size
        self.__predictions: dict = dict()
        self.__results: dict = dict()

    def set_model(self, model) -> None:
        self.__model = model

    def get_model(self):
        return self.__model

    def set_images(self, images: list) -> None:
        self.__images = images

    def get_images(self) -> list:
        return self.__images

    def get_image(self, index: int) -> str:
        try:
            return self.__images[index]
        except:
            return None

    def set_prediction(self, image_id: str, prediction: int) -> None:
        self.__predictions[image_id] = prediction

    def get_prediction(self, image_id: str) -> int:
        try:
            return self.__predictions[image_id]
        except:
            return -1
        
    def set_result(self, result: list) -> None:
        self.__results[list[0]] = result

    def set_results(self, results: list) -> None:
        self.__results = results

    def get_results(self) -> dict:
        return self.__results

    def get_result(self, index: int) -> list:
        try:
            return self.__results[index]
        except:
            return None

    def size(self) -> int:
        return len(self.__images)

class Subsession:
    """
    """
    
    def __init__(self,
            session_step: int,
            session: Session,
            strategy: Strategy,
            nbr_of_streams: int,
            nbr_of_slots: int) -> None:
        """
        """
        self.__session_step: int = session_step
        self.__session: Session = session
        self.__strategy: Strategy = strategy
        self.__parameters: list = list()
        self.__streams: list = list()
        for i in range(nbr_of_streams):
            self.__streams.append(Stream(nbr_of_slots))

    def get_session_step(self) -> int:
        return self.__session_step

    def get_strategy(self) -> Strategy:
        return self.__strategy

    def set_session(self, session: Session) -> None:
        self.__session = session

    def get_session(self) -> Session:
        return self.__session

    def set_stream(self, stream_id: int, stream: Stream) -> None:
        try:
            self.__streams[stream_id] = stream
        except:
            return

    def get_stream(self, stream_id: int) -> Stream:
        try:
            return self.__streams[stream_id]
        except:
            return None

    def get_streams(self) -> Stream:
        return self.__streams

    def set_model(self, stream_id: int, model) -> None:
        try:
            self.__streams[stream_id].set_model(model)
        except:
            return None

    def get_model(self, stream_id: int):
        try:
            return self.__streams[stream_id].get_model()
        except:
            return None

    def set_parameters(self, parameters: list) -> None:
        self.__parameters = parameters

    def get_parameters(self) -> list:
        return self.__parameters

    def nbr_of_images(self) -> int:
        return self.__streams[0].size()

    def nbr_of_streams(self) -> int:
        return len(self.__streams)

    def serialize(self) -> dict:
        """
        """
        subsession_data: dict = dict()
        try:
            for stream_id in range(len(self.__streams)):
                subsession_data[stream_id] = dict()
                subsession_data[stream_id]['model'] = self.__streams[stream_id].get_model()
                subsession_data[stream_id]['im_order'] = self.__streams[stream_id].get_images()
                subsession_data[stream_id]['im_index'] = len(self.__streams)
                subsession_data[stream_id]['results'] = list(self.__streams[stream_id].get_results().values())
                subsession_data[stream_id]['session_id'] = str(self.__session.get_id())
                subsession_data[stream_id]['session_step'] = self.__step
                subsession_data[stream_id]['maxImages'] = self.__streams[stream_id].size()
                subsession_data[stream_id]['strategy'] = str(self.__strategy)
                if self.__steams[stream_id].get_strategy() == Strategy.ALMT:
                    subsession_data[stream_id]['param'] = self.__parameters
                else:
                    subsession_data[stream_id]['param'] = list()
            return subsession_data
        except:
            return None

    @classmethod
    def deserialize(cls, data: dict) -> Subsession:
        """
        """
        try:
            subsession: Subsession = Subsession(
                    subsession[0]['session_step'],
                    None,
                    Strategy[subsession[0]['strategy']],
                    len(subsession_data),
                    subsession_data[0]['maxImages'])
            subsession.set_current_index(subsession_data[0]['im_index'])
            subsession.set_parameters(subsession_data[stream_id]['param'])
            for stream_id in range(len(data)):
                stream: Stream = Stream(data[stream_id]['maxImages'])
                stream.set_images(data[stream_id]['im_order'])
                stream.set_results(data[stream_id]['results'])
                subsession.set_stream(stream_id, stream)
        except:
            return None

class Session:
    """
    """
    
    def __init__(self,
            session_id: uuid,
            steps: int) -> None:
        """
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
        """
        """
        self.__steps[step_id].insert(subsession.get_session_step(), subsession)

    def get_step(self, step_id: int) -> list:
        try:
            return self.__steps[step_id]
        except:
            return None
    
    def get_steps(self) -> list:
        return self.__steps

    def nbr_of_steps(self) -> int:
        return len(self.__steps)

    def nbr_of_subsessions_in_step(self, step_id: int) -> int:
        try:
            return len(self.__steps[step_id])
        except:
            return 0

    def get_subsession(self, step_id: int, subsession_id: int) -> Subsession:
        try:
            return self.__steps[step_id][subsession_id]
        except:
            return None
    
    def serialize(self) -> dict:
        """
        """
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
        """
        """
        try:
            session: Session = Session(uuid.UUID(int=data['session_id']), len(data['steps']))
            for step in range(session.nbr_of_steps()):
                for subsession_idex in range(len(data['steps'])):
                    subsession: Subsession = Subsession.deserialize(data['steps']['subsession_index'])
                    subsession.set_session(session)
                    session.add_subsession(step, subsession)
            return session
        except:
            return None
