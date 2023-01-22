"""melodies model tests."""

# run these tests like:
#
#    python -m unittest test_melody_model.py


from app import app
from unittest import TestCase

from models import db, User, Melody


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///melodic-test"
app.config['SQLALCHEMY_ECHO'] = False


with app.app_context():
    db.drop_all()
    db.create_all()


class MelodyModelTestCase(TestCase):
    """Test attributes of melody model."""

    def setUp(self):
        """Create test client."""
        with app.app_context():
            User.query.delete()
            Melody.query.delete()

            self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_melody_model(self):
        """Does basic model work?"""

        with app.app_context():
            u = User(
                username="testuser",
                password="HASHED_PASSWORD")
            db.session.add(u)
            db.session.commit()

            mel = Melody(
                user_id=u.id,
                name="test",
                timestamp="1/18/22 10:40",
                music_notes="sample notes",
                visibility=True
            )

            db.session.add(mel)
            db.session.commit()

        # melody should have user of testuser
            self.assertEqual(mel.users.username, 'testuser')
            # melody instrument should default to piano
            self.assertEqual(mel.instrument, "piano")
            db.session.rollback()

    def test_melody_requirements(self):
        """Are there requirements on creating a new melody? Do the defaults work?"""
        with app.app_context():
            db.session.rollback()
            u = User(
                username="testuser",
                password="HASHED_PASSWORD"
            )

            db.session.add(u)
            db.session.commit()

# no timestamp
            mel1 = Melody(
                user_id=u.id,
                name="test",
                music_notes="sample notes",
                visibility=True
            )
    # no name
            mel2 = Melody(
                user_id=u.id,
                timestamp="1/18/22 10:40",
                music_notes="sample notes",
                visibility=True
            )

# no user_id

            mel3 = Melody(
                name="test",
                timestamp="1/18/22 10:40",
                music_notes="sample notes",
                visibility=True
            )

# no music notes

            mel4 = Melody(
                user_id=u.id,
                name="test",
                timestamp="1/18/22 10:40",
                visibility=True
            )

# no visibility
            mel5 = Melody(
                user_id=u.id,
                name="test",
                timestamp="1/18/22 10:40",
                music_notes="sample notes",
            )

            db.session.add_all([mel2, mel5])
            db.session.commit()

            errors = []
            try:
                db.session.add(mel1)
                db.session.commit()
            except:
                errors += ["mel1"]
                db.session.rollback()

            # except:
            #     errors += ["msg2"]
            try:
                db.session.add(mel3)
                db.session.commit()

            except:
                errors += ["mel3"]
                db.session.rollback()
            try:
                db.session.add(mel4)
                db.session.commit()
            except:
                errors += ["mel4"]
                db.session.rollback()
            try:
                db.session.add(mel5)
                db.session.commit()
            except:
                errors += ["mel5"]
                db.session.rollback()

            # Only melodies 2 and 5 should have been accepted
            self.assertEqual(errors, ["mel1", "mel3", "mel4"])
            # Mel2 should have default name
            self.assertEqual(mel2.name, "Unnamed")
            # mel5 should have default visibility
            self.assertEqual(mel5.visibility, False)

    def test_cascade_on_delete(self):
        """test if melody is removed if associated user is deleted"""
        with app.app_context():
            u = User(
                username="testuser",
                password="HASHED_PASSWORD"
            )

            db.session.add(u)
            db.session.commit()

            mel = Melody(
                user_id=u.id,
                name="test",
                timestamp="1/18/22 10:40",
                music_notes="sample notes",
                visibility=True
            )

            db.session.add(mel)
            db.session.commit()

            db.session.delete(u)
            db.session.commit()

            # No melodies should be in table after user is deleted
            self.assertEqual(len(Melody.query.all()), 0)
