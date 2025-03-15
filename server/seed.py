#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Recipe, User

fake = Faker()

with app.app_context():

    Recipe.query.delete()
    User.query.delete()

    users = []
    usernames = set()

    for _ in range(20):
        username = fake.unique.first_name()
        user = User(
            username=username,
            bio=fake.paragraph(nb_sentences=3),
            image_url=fake.url(),
        )
        user.password_hash = f'{username}password'
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    recipes = []
    for i in range(100):
        recipe = Recipe(
            title=fake.sentence(),
            instructions=fake.paragraph(nb_sentences=10),
            minutes_to_complete=randint(15, 90),
            user_id=rc(users).id
        )
        recipes.append(recipe)

    db.session.add_all(recipes)
    db.session.commit()
