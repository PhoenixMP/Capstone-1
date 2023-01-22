"""Favorited_Track and User_Favorited_Track models tests."""

# run these tests like:
#
#    python -m unittest test_favoriting_models.py


from app import app

from unittest import TestCase

from models import db, User, Favorited_Track, User_Favorited_Track


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///melodic-test"
app.config['SQLALCHEMY_ECHO'] = False


with app.app_context():
    db.create_all()


class FavoritesModelsTestCase(TestCase):
    """Test attributes of user."""

    def setUp(self):
        """Create test client"""
        with app.app_context():
            User.query.delete()
            Favorited_Track.query.delete()
            User_Favorited_Track.query.delete()

            self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_Favorited_Track_models(self):
        """Does basic model work?"""
        with app.app_context():
            db.session.rollback()
            u = User(
                username="testuser",
                password="HASHED_PASSWORD"
            )

            db.session.add(u)
            db.session.commit()

            track = Favorited_Track(track_name="trackName", artist_name="artistName",
                                    album_name="albumName", track_photo="photo.png", spotify_track_id='12345')

            db.session.add(track)
            db.session.commit()

            user_favorited = User_Favorited_Track(
                track_id=track.id, user_id=u.id)

            db.session.add(user_favorited)
            db.session.commit()

            # new favorited track should have saved data
            self.assertEqual(track.track_name, "trackName")
            self.assertEqual(track.spotify_track_id, "12345")

            # user favorited track should be associated with user u
            self.assertEqual(user_favorited.user_id, u.id)

    def test_favorited_track_requirements(self):
        """Are there requirements on adding a favorited track, do the defaults work?"""
        with app.app_context():
            # track1 has all requirements
            track1 = Favorited_Track(track_name="trackName", artist_name="artistName",
                                     album_name="albumName", track_photo="photo.png", spotify_track_id='1')

            # track2 has identical spotify_track_id as track1
            track2 = Favorited_Track(track_name="trackName", artist_name="artistName",
                                     album_name="albumName", track_photo="photo.png", spotify_track_id='1')

            # track3 has no track name
            track3 = Favorited_Track(artist_name="artistName", album_name="albumName",
                                     track_photo="photo.png", spotify_track_id='123')

            # track4 has no artist name
            track4 = Favorited_Track(track_name="trackName",  album_name="albumName",
                                     track_photo="photo.png", spotify_track_id='1234')

            # track5 has no album name
            track5 = Favorited_Track(track_name="trackName", artist_name="artistName",
                                     track_photo="photo.png", spotify_track_id='12345')

            # track6 has no track photo
            track6 = Favorited_Track(track_name="trackName", artist_name="artistName",
                                     album_name="albumName", spotify_track_id='123456')

            # track1 has no spotify track id
            track7 = Favorited_Track(track_name="trackName", artist_name="artistName",
                                     album_name="albumName", track_photo="photo.png")

            db.session.add(track1)
            db.session.commit()
            errors = 0

            try:
                db.session.add(track2)
                db.session.commit()
            except:
                errors += 1
                db.session.rollback()
            try:
                db.session.add(track3)
                db.session.commit()
            except:
                errors += 1
                db.session.rollback()
            try:
                db.session.add(track4)
                db.session.commit()
            except:
                errors += 1
                db.session.rollback()
            try:
                db.session.add(track5)
                db.session.commit()
            except:
                errors += 1
                db.session.rollback()
            try:
                db.session.add(track6)
                db.session.commit()
            except:
                errors += 1
                db.session.rollback()
            try:
                db.session.add(track7)
                db.session.commit()
            except:
                errors += 1
                db.session.rollback()

            # track2 and track7 should be the only tracks that could not be favorited
            self.assertEqual(errors, 2)
            self.assertEqual(track3.track_name, 'Not Available')
            self.assertEqual(track4.artist_name, 'Not Available')
            self.assertEqual(track5.album_name, 'Not Available')
            self.assertEqual(
                track6.track_photo, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcnVvH2T5J45c9Bp3zm4R7ZwLmBBwFCTbo3w&usqp=CAU')
            db.session.rollback()

    def test_cascade_on_delete(self):
        """Test if User_Favorited_Track model removes item if corresponding favorite track or user is deleted"""
        with app.app_context():
            db.session.rollback()
            u1 = User(
                username="testuser",
                password="HASHED_PASSWORD"
            )

            u2 = User(
                username="testuser2",
                password="HASHED_PASSWORD"
            )

            db.session.add_all([u1, u2])
            db.session.commit()

            track1 = Favorited_Track(track_name="trackName", artist_name="artistName",
                                     album_name="albumName", track_photo="photo.png", spotify_track_id='12345')
            track2 = Favorited_Track(track_name="trackName", artist_name="artistName",
                                     album_name="albumName", track_photo="photo.png", spotify_track_id='123456')

            db.session.add_all([track1, track2])
            db.session.commit()

            user_favorited1 = User_Favorited_Track(
                track_id=track1.id, user_id=u1.id)
            user_favorited2 = User_Favorited_Track(
                track_id=track2.id, user_id=u2.id)

            db.session.add_all([user_favorited1, user_favorited2])
            db.session.commit()

            self.assertEqual(len(User_Favorited_Track.query.all()), 2)

            # delete user 1
            db.session.delete(u1)
            db.session.commit()
            # the user favorited track associated with user 1 should also be deleted, leaving only 1 left
            self.assertEqual(len(User_Favorited_Track.query.all()), 1)

            # delete track2
            db.session.delete(track2)
            db.session.commit()
            # the user favorited track associated with track2 should also be deleted, leaving no favorited tracks left
            self.assertEqual(len(User_Favorited_Track.query.all()), 0)
