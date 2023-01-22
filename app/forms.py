"""Forms for Melodic."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


genres = ['---', 'classical', 'funk',
          'electronic', 'jazz', 'pop', 'blues', 'disney']


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[
                           DataRequired(), Length(min=6)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[Length(min=6)], render_kw={
                             "placeholder": "Password"})
    password_confirm = PasswordField('Repeat Password', validators=[
                                     DataRequired(), Length(min=6), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})


class UserEditForm(FlaskForm):
    """Form for editting a users."""

    username = StringField('Edit Username', validators=[
                           DataRequired(), Length(min=6)], render_kw={"placeholder": "New Username"})
    password = PasswordField(
        'Enter Password for Validation', validators=[Length(min=6)], render_kw={"placeholder": "Password"})


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()], render_kw={
                           "placeholder": "Username"})
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)], render_kw={"placeholder": "Password"})


class SearchTrackForm(FlaskForm):
    """Form for searching for a Spotify track via track name or artist name."""

    track_name = StringField('Track Name', render_kw={
                             "placeholder": "Track Name"})
    artist_name = StringField('Artist Name', render_kw={
                              "placeholder": "Artist Name"})


class SearchGenreForm(FlaskForm):
    """Form for searching for a Spotify track via selecting the genre."""
    genre = SelectField('Or, select a Genre:', choices=genres)


class SaveMelodyForm(FlaskForm):
    """Form for adding a new user-saved melody."""

    name = StringField('Name your Melody', validators=[
                       DataRequired()], render_kw={"placeholder": "Melody Name"})
    visibility = BooleanField('Make Melody Visible to Public')
