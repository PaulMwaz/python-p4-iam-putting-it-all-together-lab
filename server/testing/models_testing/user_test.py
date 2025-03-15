from sqlalchemy.exc import IntegrityError
import pytest

from app import app
from models import db, User, Recipe

class TestUser:

    def test_has_attributes(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(
                username="Liz",
                image_url="https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg",
                bio="""Dame Elizabeth Rosemond Taylor DBE (February 27, 1932 - March 23, 2011) was a British-American actress. She began her career as a child actress in the early 1940s and was one of the most popular stars of classical Hollywood cinema in the 1950s. She then became the world's highest paid movie star in the 1960s, remaining a well-known public figure for the rest of her life. In 1999, the American Film Institute named her the seventh-greatest female screen legend of Classic Hollywood cinema."""
            )

            user.password_hash = "whosafraidofvirginiawoolf"
            db.session.add(user)
            db.session.commit()

            created_user = User.query.filter(User.username == "Liz").first()

            assert created_user.username == "Liz"
            assert created_user.image_url == "https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg"
            assert created_user.bio.startswith("Dame Elizabeth Rosemond Taylor DBE")

            with pytest.raises(AttributeError):
                _ = created_user.password_hash

    def test_requires_username_and_password(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(username=None)
            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()
            db.session.rollback()

            user2 = User(username="TestUser")
            with pytest.raises(IntegrityError):
                db.session.add(user2)
                db.session.commit()
            db.session.rollback()

    def test_requires_unique_username(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user_1 = User(username="Ben")
            user_1.password_hash = "password1"

            user_2 = User(username="Ben")
            user_2.password_hash = "password2"

            with pytest.raises(IntegrityError):
                db.session.add_all([user_1, user_2])
                db.session.commit()
            db.session.rollback()

    def test_has_list_of_recipes(self):
        with app.app_context():
            User.query.delete()
            Recipe.query.delete()
            db.session.commit()

            user = User(username="Prabhdip")
            user.password_hash = "securepassword"

            recipe_1 = Recipe(
                title="Delicious Shed Ham",
                instructions="Or kind rest bred with am shed then. In raptures building an bringing be. Elderly is detract tedious assured private so to visited. Do travelling companions contrasted it. Mistress strongly remember up to. Ham him compass you proceed calling detract. Better of always missed we person mr. September smallness northward situation few her certainty something.",
                minutes_to_complete=60,
            )
            recipe_2 = Recipe(
                title="Hasty Party Ham",
                instructions="As am hastily invited settled at limited civilly fortune me. Really spring in extent an by. Judge but built gay party world. Of so am he remember although required. Bachelor unpacked be advanced at. Confined in declared marianne is vicinity. Some additional instructions to meet validation length.",
                minutes_to_complete=30,
            )

            user.recipes.extend([recipe_1, recipe_2])
            db.session.add(user)
            db.session.commit()

            assert user.id
            assert recipe_1.id
            assert recipe_2.id

            assert recipe_1 in user.recipes
            assert recipe_2 in user.recipes
