import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Movie
a persistent movie entity, extends the base SQLAlchemy Model
Movies with attributes title and release date
'''


class Movie(db.Model):
	__tablename__ = "movies"
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # Movie Title
    title = Column(String(80), nullable=False)
    # Release date of movie
    release_date = Column(DateTime(), nullable=False)
    # Actors
    actors = db.relationship("Actor", backref="movies")


    '''
    get_movie_info()
        json form representation of the Movie model
    '''

    def get_movie_info(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.get_movie_info())

'''
Actor
a persistent movie entity, extends the base SQLAlchemy Model
Actors with attributes name, age and gender
'''


class Actor(db.Model):
	__tablename__ = "actors"
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # Actor Name
    name = Column(String(80), nullable=False)
    # Age of actor
    age= Column(Integer(), nullable=False)
    # Actor gender
    gender = Column(String(80), nullable=False)
    # Movies
    movie_id = Column(Integer(),ForeignKey("parent.id"),nullable=False)


    '''
    get_actor_info()
        json form representation of the Movie model
    '''

    def get_actor_info(self):
        return {
            'id': self.id,
            'title': self.name,
            'release_date': self.age,
            'gender': self.gender
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.get_actor_info())