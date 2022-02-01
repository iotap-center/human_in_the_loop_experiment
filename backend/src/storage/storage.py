from session import Session, Subsession
from storage.disk_storage import DiskStorage
from storage.memory_storage import MemoryStorage
import uuid

# This is an ugly hack used to  satisfy some internal dependencies
Storage = type('Storage', (object,), {})

class Storage:

    def __init__(self, backend) -> None:
        self.__backend = backend

    def add_session(self, session: Session) -> None:
        self.__backend.add_session(session)

    def list_sessions(self) -> list:
        return self.__backend.list_sessions()

    def get_session(self, session_id: uuid) -> Session:
        return self.__backend.get_session(session_id)

    def get_nbr_of_steps(self, session_id: uuid) -> int:
        return self.__backend.get_nbr_of_steps(session_id)

    def get_steps(self, session_id: uuid) -> list:
        return self.__backend.get_steps(session_id)

    def get_step(self, session_id: uuid, step_id: int) -> dict:
        return self.__backend.get_step(session_id, step_id)

    def save_subsession(self, subsession: Subsession) -> None:
        self.__backend.save_subsession(subsession)

    @classmethod
    def create_storage(cls, backend: str) -> Storage:
        if backend == 'disk':
            return Storage(DiskStorage())
        else:
            return Storage(MemoryStorage())
