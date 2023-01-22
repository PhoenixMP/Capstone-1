"""All View tests."""

# run these tests like:
#
# FLASK_ENV=production
# python3 -m unittest test_views.py


from app import app, CURR_USER_KEY, do_login
from unittest import TestCase
from models import db, connect_db, Melody, User, Favorited_Track, User_Favorited_Track


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///melodic-test"
app.config['SQLALCHEMY_ECHO'] = False


with app.app_context():
    db.drop_all()
    db.create_all()


app.config['WTF_CSRF_ENABLED'] = False


class AllViewsTestCase(TestCase):
    """Test views."""

    def setUp(self):
        """Create test client, add sample data."""
        with app.app_context():
            User.query.delete()
            Melody.query.delete()
            Favorited_Track.query.delete()
            User_Favorited_Track.query.delete()

            # Building database of users
            self.mainuser = User(username="mainuser",
                                 password="testing")
            self.user1 = User(username="testuser1",
                              password="testing")

            db.session.add_all(
                [self.mainuser, self.user1])
            db.session.commit()

            self.mainuser_id = 100
            self.mainuser.id = self.mainuser_id
            self.user1_id = 101
            self.user1.id = self.user1_id

            self.track1 = Favorited_Track(track_name="trackName1", artist_name="artistName1",
                                          album_name="albumName1", track_photo="photo1.png", spotify_track_id='12345')
            self.track2 = Favorited_Track(track_name="trackName2", artist_name="artistName2",
                                          album_name="albumName2", track_photo="photo2.png", spotify_track_id='123456')

            db.session.add_all([self.track1, self.track2])
            db.session.commit()

            self.track1_id = 100
            self.track1.id = self.track1_id
            self.track2_id = 101
            self.track2.id = self.track2_id

            self.user_favorited1 = User_Favorited_Track(
                track_id=self.track1.id, user_id=self.mainuser.id)
            self.user_favorited2 = User_Favorited_Track(
                track_id=self.track2.id, user_id=self.user1.id)

            db.session.add_all([self.user_favorited1, self.user_favorited2])
            db.session.commit()

            self.mel1 = Melody(
                user_id=self.mainuser_id,
                name="test1",
                timestamp="1/18/22 10:40",
                music_notes="sample notes",
                visibility=True
            )

            self.mel2 = Melody(
                user_id=self.mainuser_id,
                name="test2",
                timestamp="1/18/22 10:40",
                music_notes="sample notes",
                visibility=False
            )
            self.mel3 = Melody(
                user_id=self.user1_id,
                name="test3",
                timestamp="1/18/22 10:40",
                music_notes="sample notes",
                visibility=True
            )

            self.mel4 = Melody(
                user_id=self.user1_id,
                name="test4",
                timestamp="1/18/22 10:40",
                music_notes="sample notes",
                visibility=False
            )

            self.mel1_id = 100
            self.mel1.id = self.mel1_id
            self.mel2_id = 101
            self.mel2.id = self.mel2_id
            self.mel3_id = 102
            self.mel3.id = self.mel3_id
            self.mel4_id = 103
            self.mel4.id = self.mel4_id

            db.session.add_all([self.mel1, self.mel2, self.mel3, self.mel4])
            db.session.commit()

            self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_home(self):
        """Do the 2 "shared" melodies show up on home-page"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.mainuser_id
            resp = c.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            # Test that the two melodies with visibility set to True are shown, but not the two with visibility set to False
            self.assertIn("test1", html)
            self.assertNotIn("test2", html)
            self.assertIn("test3", html)
            self.assertNotIn("test4", html)

    def test_search_form(self):
        """Can you see fa fa-hearts on /search-tracks page when logged in? """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.mainuser_id

            resp = c.get("/search-tracks")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("fa fa-heart", html)

    def test_spotify_player(self):
        """Can you see fa fa-hearts on /jam page when logged in? """

        with app.app_context():
            with self.client as c:
                with c.session_transaction() as session:
                    session[CURR_USER_KEY] = self.mainuser_id
                    session['recommended_tracks'] = []

                    favorite_track = [Favorited_Track.query.get(
                        track.track_id) for track in User_Favorited_Track.query.filter(User_Favorited_Track.user_id == self.mainuser_id)]

                    if favorite_track != None:
                        session['favorite_track_ids'] = [
                            track.spotify_track_id for track in favorite_track]
                    else:
                        session['favorite_track_ids'] = []

                resp = c.get("/jam/6tHtqQ2VYGqgcjh5TAMunF")
                resp = c.get("/jam/6tHtqQ2VYGqgcjh5TAMunF")
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn("fa fa-heart", html)

    def test_delete_melody(self):
        """Can a user delete their melody"""
        with app.app_context():
            with self.client as c:
                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = self.mainuser_id
                    sess['last_url'] = '/'

                resp = c.post(
                    f'/delete-melody/{self.mel2_id}', follow_redirects=True)

                # Make sure it redirects back to home page
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn("Welcome to Melodic", html)

                melodies = Melody.query.filter(
                    Melody.user_id == self.mainuser_id).all()

                # only 1 of the initial 2 melodies by this user should be left
                self.assertEqual(len(melodies), 1)

    def test_save_melody(self):
        """Can a user save a new melody"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.mainuser_id
                sess['last_url'] = '/'

            resp = c.post("/save-melody", data={"name": "third"})

            self.assertEqual(resp.status_code, 302)
            melodies = Melody.query.filter(
                Melody.user_id == self.mainuser_id).all()

            # there should be 3 melodies after adding one
            self.assertEqual(len(melodies), 3)
            self.assertEqual(melodies[2].name, 'third')

    def test_edit_melody(self):
        """Can a user edit their existing melody (toggle visibility)"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.mainuser_id
                sess['last_url'] = '/'

            resp = c.post(
                f'/edit-melody/{self.mel1_id}', follow_redirects=True)

            # Make sure it redirects back to home page
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Welcome to Melodic", html)
            self.assertNotIn("test1", html)

            melody = Melody.query.get(self.mel1_id)
            self.assertEqual(melody.visibility, False)

    def test_user_profile(self):
        """Does the user profile page show their favorited tracks and recorded melodies?"""
        with app.app_context():
            with self.client as c:
                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = self.mainuser_id

                resp = c.get(
                    f"/profile/{self.mainuser_id}")
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)

                self.assertIn("test1", html)

                self.assertIn("test2", html)
                self.assertNotIn("test3", html)
                self.assertNotIn("test4", html)

                self.assertIn("fa fa-heart", html)

                self.assertIn("trackName1", html)
                self.assertNotIn("trackName2", html)


############################################################################
# Testing when user is logged out

    def test_home_logged_out(self):
        """Is a user unable to edit visibility of melodies on home page when logged out?"""

        with self.client as c:

            resp = c.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            self.assertNotIn("Melody Visible", html)

    def test_search_form_logged_out(self):
        """Can you see no fa fa-hearts on /search-tracks page when logged out? """
        with self.client as c:
            resp = c.get("/search-tracks")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("fa fa-heart", html)

    def test_spotify_player_logged_out(self):
        """Can you see no fa fa-hearts on /jam page when logged out? """

        with self.client as c:
            with c.session_transaction() as session:
                session['favorite_track_ids'] = []
            resp = c.get("/jam/6tHtqQ2VYGqgcjh5TAMunF")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("fa fa-heart", html)

    def test_delete_melody_logged_out(self):
        """Can a user delete melody when logged out?"""
        with self.client as c:
            resp = c.post(
                f'delete-melody/{self.mel2_id}', follow_redirects=True)
            # Make sure it redirects back to home page
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Access unauthorized", html)

    def test_save_melody_logged_out(self):
        """Can a user save a new melody when logged out"""
        with self.client as c:

            resp = c.post("/save-melody",
                          data={"name": "third"}, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Log-in to save melodies", html)

    def test_edit_melody_logged_out(self):
        """Can a user edit their existing melody (toggle visibility) if logged out"""
        with self.client as c:

            resp = c.post(
                f'/edit-melody/{self.mel1_id}', follow_redirects=True)

            # Make sure it redirects back to home page
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Access unauthorized", html)

    def test_edit_profile_logged_out(self):
        """Can a user edit their username if logged out?"""
        with self.client as c:

            resp = c.post('/edit-profile',
                          data={"username": "newMain", "password": "testing"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Access unauthorized", html)

    def test_user_profile_logged_out(self):
        """Does the user profile page show their favorited tracks and recorded melodies if logged out?"""
        with self.client as c:

            resp = c.get(
                f"/profile/{self.mainuser_id}", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Access unauthorized", html)
