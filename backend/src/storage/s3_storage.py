from re import sub
from session import Session, Subsession, Strategy
from storage.memory_storage import MemoryStorage
import configparser
import io
import pickle
import boto3
import json
import uuid

S3Resource = type('S3Resource', (object,), {})

class S3Storage:

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config/app.ini')
        self.__cache: MemoryStorage = MemoryStorage()
        self.__bucket: str = config['aws']['bucket']
        self.__resource = self.__connect(config['aws']['region'], config['aws']['access_key'], config['aws']['secret_access_key'])
        self.__client = boto3.client('s3')
        self.__sessions_path: str = config['backend']['sessions_path']
        self.__results_path: str = config['backend']['results_path']

    def add_session(self, session: Session) -> None:
        self.__cache.add_session(session)
        obj = self.__resource.Object(self.__bucket, self.__sessions_path + str(session.get_id()) + '.pickle')
        obj.put(Body=pickle.dumps(session))

    def list_sessions(self) -> list:
        sessions: list = list()
        prefix_length: int = len(self.__sessions_path)
        
        response = self.__client.list_objects_v2(
            Bucket = self.__bucket,
            Prefix = self.__sessions_path
        )

        result = response.get("Contents")

        for session in result:
            sessions.append(uuid.UUID(session['Key'][0:prefix_length]))

        return sessions

    def get_session(self, session_id: uuid) -> Session:
        session: Session = self.__cache.get_session(session_id)
        if not Session:
            try:
                obj = self.__resource.Object(self.__bucket, self.__sessions_path + str(session_id))
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

    def save_subsession(self, subsession: Subsession) -> None:
        filename = self.__create_filename(subsession, 'results')
        obj = self.__resource.Object(self.__bucket, filename)
        obj.put(Body=pickle.dumps(subsession))

    def save_results(self, subsession: Subsession) -> None:
        pickle_filename = self.__create_filename(subsession, 'results')
        pickle_file = self.__resource.Object(self.__bucket, pickle_filename)
        pickle_file.put(Body=pickle.dumps(subsession.serialize_results()))
        json_filename = self.__create_filename(subsession, 'results', 'json')
        json_file = self.__resource.Object(self.__bucket, json_filename)
        json_file.put(Body=json.dumps(subsession.serialize_results()))

    def __create_filename(self,
            subsession: Subsession = None,
            object_type: str = "",
            format: str = "pickle") -> str:
        """Creates a filename based on a subsession.
        
        Keyword arguments:
        session_id -- A session
        object_type -- A suffix used to tell what the dump actually contains
        format -- The kind of format that we want to save in
        """
        session_id = str(subsession.get_session().get_id())
        session_step = subsession.get_session_step() + 1
        strategy = str(subsession.get_strategy())
        if object_type == 'results':
            path = self.__results_path + format + "/"
            return '{0}{1}_{2}_{3}.{4}.{5}'.format(path, session_id, session_step, strategy, object_type, format)
        elif object_type == 'full':
            return '{0}{1}.{2}.{3}'.format(self.__sessions_path, session_id, object_type, format)

        return None

    def __connect(self, region: str, access_key: str, secret: str) -> S3Resource:
        return boto3.resource(
            service_name = 's3',
            region_name = region,
            aws_access_key_id = access_key,
            aws_secret_access_key = secret
        )