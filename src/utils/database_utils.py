from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

import configs

Base = declarative_base()

class DatabaseUtils:
    def __init__(self, database_url=None):
        if database_url is None:
            database_url = configs.DATABASE_MARIADB_URL
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.Session

    def execute_query(self, query):
        with self.Session() as session:
            result = session.execute(query)
            return result.fetchall()

    def execute_statement(self, statement):
        with self.Session() as session:
            session.execute(statement)
            session.commit()

    def execute_data_model(self, data_model):
        if data_model is None:
            raise DataModelUndefinedError("Data model not defined!")
        with self.Session() as session:
            try:
                session.merge(data_model)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise e
        
    def query_model(self, DataModelClass, **filter_criteria):
        with self.Session() as session:
            return session.query(DataModelClass).filter_by(**filter_criteria).first()

class DataModelUndefinedError(Exception):
    def __init__(self, message):
        self.name = self.__name__
        self.message = self.message
        super().__init__(f"Exception in {self.__name__}: {message}")

if __name__ == "__main__":
    database = DatabaseUtils()