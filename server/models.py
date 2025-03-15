from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', back_populates='user', cascade='all, delete-orphan')

    serialize_rules = ('-recipes.user',)

    @hybrid_property
    def password_hash(self):
        raise AttributeError('password_hash is not readable.')

    @password_hash.setter
    def password_hash(self, password):
        if not password:
            raise ValueError('Password is required.')
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='recipes')

    serialize_rules = ('-user.recipes',)

    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions or len(instructions) < 50:
            raise ValueError('Instructions must be at least 50 characters.')
        return instructions

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title is required.')
        return title
