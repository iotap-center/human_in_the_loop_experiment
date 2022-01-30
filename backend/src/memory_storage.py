from session import Session
import uuid

class MemoryStorage:

    def __init__(self) -> None:
        self.__store: dict = dict()

    def add_session(self, session: Session) -> None:
        self.__store[session.get_id().int] = session

    def list_sessions(self) -> list:
        sessions = list()
        
        for key in self.__store:
            sessions.append(uuid.UUID(int=key))

        return sessions

    def get_sessions(self) -> dict:
        return self.__store.copy()

    def get_session(self, session: uuid) -> Session:
        if session.int in self.__store:
            return self.__store[session.int]
        else:
            return None

    def get_nbr_of_steps(self, session: uuid) -> int:
        steps: int = -1
        
        if session.int in self.__store:
            steps = self.__store[session.int].nbr_of_steps()

        return steps

    def get_steps(self, session: uuid) -> list:
        steps: list = None
        
        if session.int in self.__store:
            steps = self.__store[session.int].get_steps()

        return steps

    def get_step(self, session: uuid, step_id: int) -> dict:
        step: dict = None
        
        if session.int in self.__store:
            step = self.__store[session.int]['steps'][step_id]

        return step
