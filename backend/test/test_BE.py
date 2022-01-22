import sys
sys.path.append('../src/')

from session import Session, Subsession, Strategy
from datetime import datetime
import main_BE
import time

session = main_BE.create_session()

for step in range(0, session.nbr_of_steps()):
    for subsession in range(0, 1):
        for stream in range(0, len(session.get_subsession(step, subsession).get_streams())):
            print('predicting...')
            now = datetime.now()
            print(now.strftime("%H:%M:%S"))
            prediction = main_BE.classify(session.get_subsession(step, subsession), stream)
            print(prediction)
            now = datetime.now()
            print(now.strftime("%H:%M:%S"))
