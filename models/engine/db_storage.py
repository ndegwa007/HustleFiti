#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from models.base_model import Base, BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import pymysql

from models.user import User
from models.service import ServiceCategory, Service, PricePackage
from models.contract import Contract
from models.payment import Payment
from models.reviews import ServiceReview, ClientReview

classes = {"User": User, "ServiceCategory": ServiceCategory,
    "Service": Service, "PricePackage": PricePackage,
    "Contract": Contract, "Payment": Payment,
    "ServiceReview": ServiceReview, "ClientReview": ClientReview}


class DBStorage:
    """Represents a database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+pymysql://{}:{}@{}/{}".
                                      format('admin', 'admin123',
                                             'localhost', 'hustle_db'),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the curret database session all objects of the given class.

        If cls is None, queries all types of objects.

        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            objs = self.__session.query(User).all()
            objs.extend(self.__session.query(ServiceCategory).all())
            objs.extend(self.__session.query(Service).all())
            objs.extend(self.__session.query(PricePackage).all())
            objs.extend(self.__session.query(Contract).all())
            objs.extend(self.__session.query(Payment).all())
            objs.extend(self.__session.query(ServiceReview).all())
            objs.extend(self.__session.query(ClientReview).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
      
    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count