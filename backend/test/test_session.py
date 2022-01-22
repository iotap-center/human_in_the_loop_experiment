from session import Session, Subsession, Strategy
import uuid

session = Session(uuid.uuid4(), 2)
print(session)
subsession = Subsession(session, 1, Strategy.MT, 2, 5)
print(subsession)
subsession.set_model(1, [])
print(subsession.get_model(1))
