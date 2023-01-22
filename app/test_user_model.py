"""User model tests."""

# run these tests like:
#
#    python3 -m unittest test_user_model.py


from app import app
from unittest import TestCase

from models import db, User, User_Favorited_Track


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///melodic-test"
app.config['SQLALCHEMY_ECHO'] = False


with app.app_context():
    db.create_all()


class UserModelTestCase(TestCase):
    """Test attributes of melody."""

    def setUp(self):
        """Create test client."""
        with app.app_context():
            User.query.delete()
            User_Favorited_Track.query.delete()

            self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            username="testuser",
            password="HASHED_PASSWORD"
        )

        with app.app_context():
            db.session.add(u)
            db.session.commit()

            # username of the new user should be testuser
            self.assertEqual(u.username, "testuser")
            # There should be no favorited songs associated with any user
            self.assertEqual(User_Favorited_Track.query.all(), [])

    def test_user_requirements(self):
        """Are there requirements on creating a new user?"""
        # user1 has no username
        user1 = User(
            password="HASHED_PASSWORD"
        )

        # user2 has no password
        user2 = User(
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        # user3 should be fine
        user3 = User(
            username="testuser3",
            password="HASHED_PASSWORD"
        )

        # user4 has same username as user3
        user4 = User(
            username="testuser3",
            password="HASHED_PASSWORD"
        )
        with app.app_context():
            db.session.add(user3)
            db.session.commit()
            errors = 0

            try:
                db.session.add(user1)
                db.session.commit()
            except:
                errors += 1
            try:
                db.session.add(user2)
                db.session.commit()
            except:
                errors += 1
            try:
                db.session.add(user4)
                db.session.commit()
            except:
                errors += 1

            # user3 should be the only user that was made, the other 3 should create erros
            self.assertEqual(errors, 3)

    def test_authenticate(self):
        """Does User.authenticate on return a user with valid login?"""

        user1 = User(
            username="testuser1",
            password="HASHED_PASSWORD",
        )
        with app.app_context():
            user = User.signup(
                user1.username, user1.password)

            # User should not be able to login with wrong/blank username or password
            self.assertEqual(User.authenticate(
                "testuser1", "HASHED_PASSWORD"), user)
            self.assertEqual(User.authenticate(
                "WRONG_USER", user.password), False)
            self.assertEqual(User.authenticate(
                "testuser1", "WRONG_PASSWORD"), False)
            self.assertEqual(User.authenticate("", "WRONG_PASSWORD"), False)
            self.assertEqual(User.authenticate("testuser1", ""), False)
