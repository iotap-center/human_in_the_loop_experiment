from re import S
from session import Session
from memory_storage import MemoryStorage
import uuid

class Storage:

    def __init__(self) -> None:
        self.__backend: MemoryStorage = MemoryStorage()

    def add_session(self, session: Session) -> None:
        self.__backend.add_session(session)

    def list_sessions(self) -> list:
        return self.__backend.list_sessions()

    def get_sessions(self) -> dict:
        return self.__backend.get_sessions()

    def get_session(self, session: uuid) -> Session:
        return self.__backend.get_session(session)

    def get_nbr_of_steps(self, session: uuid) -> int:
        return self.__backend.get_nbr_of_steps(session)

    def get_steps(self, session: uuid) -> list:
        return self.__backend.get_steps(session)

    def get_step(self, session: uuid, step_id: int) -> dict:
        return self.__backend.get_step(session, step_id)
