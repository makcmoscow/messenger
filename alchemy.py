import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def chk_DB():
    engine = sqlalchemy.create_engine('sqlite:///123.db', pool_recycle=7200, echo=False)
    try:
        result = engine.execute("select * from users")
    except sqlalchemy.exc.OperationalError:
        create_DB()

def create_DB():
    engine = sqlalchemy.create_engine('sqlite:///123.db', pool_recycle=7200, echo=False)
    #     создаем таблицу users
    metadata = sqlalchemy.MetaData()
    users_table = sqlalchemy.Table('users', metadata,
                                   sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                                   sqlalchemy.Column('name', sqlalchemy.String(25)),
                                   sqlalchemy.Column('password', sqlalchemy.String(25))
                                   )
    metadata.create_all(engine)


chk_DB()
def create_session_DB():
    engine = sqlalchemy.create_engine('sqlite:///123.db', pool_recycle=7200, echo=False)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()
    return Base, session

Base, session = create_session_DB()

class User_DB(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, name, password = None):
        self.name = name
        self.password = password

    def __repr__(self):
        return "<User {}".format(self.name)

class Friends_DB(Base):
    __tablename__ = 'friends'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    friend_id = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id

    def __repr__(self):
        return "<Пользователь {} будет являться другом {}".format(self.friend_id, self.user_id)

def chk_uexist_DB(login, password):
    user = User_DB(login, password)
    q_user = session.query(User_DB).filter_by(name=user.name).first()
    if q_user:
        print('this user already in database')
    elif user.password:
        session.add(user)
    else:
        print('you forget to enter your password')
    session.commit()


if __name__ == '__main__':
    user = User_DB(input('enter the name '), input('enter your password '))
    # session.add(user)
    q_user = session.query(User_DB).filter_by(name=user.name).first()
    if q_user:
        print('this user already in database')
    elif user.password:
        session.add(user)
        session.commit()
    else:
        print('you forget to enter your password')
    session.commit()

