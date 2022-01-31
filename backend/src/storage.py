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

    def get_nbr_of_steps(self, session_id: uuid) -> int:
        return self.__backend.get_nbr_of_steps(session_id)

    def get_steps(self, session_id: uuid) -> list:
        return self.__backend.get_steps(session_id)

    def get_step(self, session_id: uuid, step_id: int) -> dict:
        return self.__backend.get_step(session_id, step_id)
