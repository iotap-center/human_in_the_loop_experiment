from session import Session, Subsession
import uuid

class MemoryStorage:

    def __init__(self) -> None:
        self.__store: dict = dict()

    def add_session(self, session: Session) -> None:
        self.__store[session.get_id().int] = session

    def remove_session(self, session_id) -> None:
        self.__store.pop(session_id.int)

    def list_sessions(self) -> list:
        sessions = list()
        
        for key in self.__store:
            sessions.append(uuid.UUID(int=key))

        return sessions

    def get_session(self, session_id: uuid) -> Session:
        if session_id.int in self.__store:
            return self.__store[session_id.int]
        else:
            return None

    def get_nbr_of_steps(self, session_id: uuid) -> int:
        steps: int = -1
        
        if session_id.int in self.__store:
            steps = self.__store[session_id.int].nbr_of_steps()

        return steps

    def get_steps(self, session_id: uuid) -> list:
        steps: list = None
        
        if session_id.int in self.__store:
            steps = self.__store[session_id.int].get_steps()

        return steps

    def get_step(self, session_id: uuid, step_id: int) -> dict:
        step: dict = None
        
        if session_id.int in self.__store:
            step = self.__store[session_id.int]['steps'][step_id]

        return step

    def save_subsession(self, subsession: Subsession) -> None:
        # Memory-based storage is instantly "saved", hence this is empty
        pass
