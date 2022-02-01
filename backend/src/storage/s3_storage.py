from session import Session
from memory_storage import MemoryStorage
import boto3
import json
import uuid

class S3Storage:

    def __init__(self) -> None:
        self.__cache: MemoryStorage = MemoryStorage()
        self.__resource = boto3.resource('s3')
        self.__client = boto3.client('s3')
        self.__bucket: str = ""
        self.__path: str = ""

    def set_bucket(self, bucket: str) -> None:
        self.__bucket = bucket
    
    def set_path(self, path: str) -> None:
        if path.endswith("/"):
            path += "/"
        self.__path = path

    def add_session(self, session: Session) -> None:
        self.__cache.add_session(session)
        obj = self.__resource.Object(self.__bucket, self.__path + str(session.get_id))
        obj.put(Body=json.dumps(session.serialize()))

    def list_sessions(self) -> list:
        # TODO: list sessions in S3
        sessions = list()
        
        response = self.__client.list_objects_v2(
            Bucket = self.__bucket,
            Prefix = self.__path
        )

        for key in self.__store:
            sessions.append(uuid.UUID(int=key))

        return sessions

    def get_session(self, session_id: uuid) -> Session:
        session: Session = self.__cache.get_session(session_id)
        if not Session:
            try:
                obj = self.__resource.Object(self.__bucket, self.__path + str(session_id))
                session = Session.deserialize(obj.get()['Body'].read())
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
