
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

from sqlalchemy_utils.types.password import PasswordType

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.orm import sessionmaker

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_password_updated = Column(DateTime)

    password = Column(PasswordType(schemes=[
            'pbkdf2_sha512'
        ],
        deprecated=[]))


def on_user_password_updated(target, value, old_value, initiator):
    target.last_password_updated = datetime.utcnow()


listen(User.password, 'set', on_user_password_updated)


engine = create_engine('sqlite:///sample.db')


Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)

session = Session()

user = User()

user.password = "This is a test"
session.add(user)
session.commit()
