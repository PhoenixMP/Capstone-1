"""SQLAlchemy models for Melodic."""

from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    @classmethod
    def signup(cls, username, password):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Favorited_Track(db.Model):
    """All Spotify tracks that have favorited by any user."""

    __tablename__ = 'favorited_tracks'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    track_name = db.Column(
        db.Text,
        nullable=False,
        default='Not Available'
    )

    artist_name = db.Column(
        db.Text,
        nullable=False,
        default='Not Available'
    )

    album_name = db.Column(
        db.Text,
        nullable=False,
        default='Not Available'
    )

    track_photo = db.Column(
        db.Text,
        nullable=False,
        default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcnVvH2T5J45c9Bp3zm4R7ZwLmBBwFCTbo3w&usqp=CAU'
    )

    spotify_track_id = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )


class User_Favorited_Track(db.Model):
    """Mapping users to their favorited Spotify tracks."""

    __tablename__ = 'users_favorited_tracks'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False
    )

    track_id = db.Column(
        db.Integer,
        db.ForeignKey('favorited_tracks.id', ondelete='cascade'),
        nullable=False
    )


class Melody(db.Model):
    """All recorded melodies that have been saved by a user."""

    __tablename__ = 'melodies'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False
    )

    name = db.Column(
        db.Text,
        default='Unnamed'
    )

    timestamp = db.Column(
        db.Text,
        nullable=False
    )

    instrument = db.Column(
        db.Text,
        default='piano'
    )

    music_notes = db.Column(
        db.Text,
        nullable=False
    )

    visibility = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    users = db.relationship("User")


def connect_db(app):
    """Connect this database to provided Flask app. """

    db.app = app
    db.init_app(app)
