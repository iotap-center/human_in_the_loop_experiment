from fileinput import filename
from session import Session, Subsession, Strategy
from storage.memory_storage import MemoryStorage
import configparser
import pickle
import os
import uuid

class DiskStorage:

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config/app.ini')
        self.__cache: MemoryStorage = MemoryStorage()
        self.__results_path: str = config['backend']['results_path']
        self.__sessions_path: str = config['backend']['sessions_path']

    def add_session(self, session: Session) -> None:
        self.__cache.add_session(session)
        self.__save_session(session)

    def list_sessions(self) -> list:
        # TODO: list sessions on disk
        sessions = list()
        
        for file in os.listdir(self.__sessions_path):
            if file.endswith(".full.pickle"):
                sessions.append(uuid.UUID(file[0:file.find(".")]))

        return sessions

    def get_session(self, session_id: uuid) -> Session:
        session: Session = self.__cache.get_session(session_id)
        if not Session:
            try:
                filename = self.__create_filename(session_id=session_id, object_type="full")
                session = Session.deserialize(pickle.load(open(filename, 'rb')))
                self.__cache.add_session(session)
            except:
                return None
        return session

    def get_nbr_of_steps(self, session_id: uuid) -> int:
        session: Session = self.get_session(session_id)
        steps: int = -1
        
        if session:
            steps = session.nbr_of_steps()

        return steps

    def get_steps(self, session_id: uuid) -> list:
        session: Session = self.get_session(session_id)
        steps: list = None
        
        if session:
            steps = session.get_steps()

        return steps

    def get_step(self, session_id: uuid, step_id: int) -> dict:
        session: Session = self.get_session(session_id)
        step: dict = None
        
        if session:
            step = session['steps'][step_id]

        return step

    def save_subsession(self, subsession: Subsession) -> None:
        filename = self.__create_filename(str(subsession.get_session().get_id()), subsession.get_session_step(), subsession.get_strategy(), 'results')
        pickle.dump(subsession.serialize(), open(filename, 'wb'))
    
    def __save_session(self, session: Session) -> None:
        filename = self.__create_filename(session_id = str(session.get_id()), object_type = 'full')
        pickle.dump(session.serialize(), open(filename, 'wb'))

    def __create_filename(self,
            session_id: uuid = None,
            session_step: int = 0,
            strategy: Strategy = None,
            object_type: str = "") -> str:
        """Creates a filename based on a subsession.
        
        Keyword arguments:
        session_id -- The UUID of a session
        session_step -- The step wherein we'll find the subsession
        strategy -- The strategy used to predict in this subsession
        object_type -- A suffix used to tell what the dump actually contains
        """
        if object_type == 'results':
            return '{0}{1}_{2}_{3}.{4}.pickle'.format(self.__results_path, str(session_id), session_step, str(strategy), object_type)
        elif object_type == 'full':
            return '{0}{1}.{2}.pickle'.format(self.__sessions_path, str(session_id), object_type)

        return None
