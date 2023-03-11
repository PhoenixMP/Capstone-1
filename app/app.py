
from flask import Flask, render_template, request, url_for, session, g, redirect, flash, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Melody, Favorited_Track, User_Favorited_Track
from forms import UserAddForm, LoginForm, UserEditForm, SearchTrackForm, SearchGenreForm, SaveMelodyForm
from secrets_1 import API_CLIENT_ID, API_SECRET_KEY
from datetime import datetime, timedelta


import requests
import os


CURR_USER_KEY = "curr_user"
AUTH_BASE_URL = "https://accounts.spotify.com/api/token"
API_SEARCH_BASE_URL = "https://api.spotify.com/v1/search"
API_REC_BASE_URL = "https://api.spotify.com/v1/recommendations"
API_TOP_BASE_URL = "https://api.spotify.com/v1/artists"
API_DISNEY_BASE_URL = "https://api.spotify.com/v1/playlists"


app = Flask(__name__)

uri = (
    os.environ.get('DATABASE_URL', 'postgres:///melodic'))
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")


connect_db(app)


# Acquire spotify API token at start of application
res = requests.post(AUTH_BASE_URL, {
    'grant_type': 'client_credentials',
    'client_id': API_CLIENT_ID,
    'client_secret': API_SECRET_KEY
})
data = res.json()
access_token = f'Bearer {data["access_token"]}'


# Spotify-Track-Id that inform the initial track recommendations
recommended_track_id = '6tHtqQ2VYGqgcjh5TAMunF'


########################################################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user and get the spotify ids of their favorite tracks . Prep the session keys to empty arrays"""
    session.clear()
    session[CURR_USER_KEY] = user.id
    session['recommended_tracks'] = []

    favorite_track = [Favorited_Track.query.get(
        track.track_id) for track in User_Favorited_Track.query.filter(User_Favorited_Track.user_id == user.id)]

    if favorite_track != None:
        session['favorite_track_ids'] = [
            track.spotify_track_id for track in favorite_track]
    else:
        session['favorite_track_ids'] = []


def do_logout():
    """Logout user, clear all session keys."""
    session.clear()


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """
    if g.user:
        flash("Invalid Page.", "danger")
        return redirect("/")

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    if g.user:
        flash("Invalid Page.", "danger")
        return redirect("/")

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            return redirect("/")

        flash("Invalid credentials.")

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You are logged out!", "success")
    return redirect('/login')

####################################################################################
# Home Page


@app.route('/')
def home():
    """Show home page with list of user-shared melodies"""
    session['last_url'] = '/'

    melodies = list(Melody.query.filter(
        Melody.visibility == True).order_by(Melody.id))
    melodies.reverse()

    return render_template("home.html", melodies=melodies)


########################################################################################################
# Spotify Tracks

@app.route('/search-tracks')
def search_form():
    """Search for a spotify track. Show forms for searching by track name, album name, and genre. If first time on page, show recommended starter tracks"""

    session['last_url'] = '/search-tracks'

    form_search = SearchTrackForm()
    form_genre = SearchGenreForm()

    if 'recommendation' not in session:
        session['recommendation'] = True

    if 'search_tracks' not in session:
        session['search_tracks'] = API_recommended_tracks(
            recommended_track_id, limit=6)

    if 'favorite_track_ids' not in session:
        session['favorite_track_ids'] = []

    return render_template('spotify/search-tracks.html', form_search=form_search, form_genre=form_genre, tracks=session['search_tracks'], recommendation=session['recommendation'], favorites=session['favorite_track_ids'])


@app.route('/search-tracks/search', methods=["POST"])
def search_for_tracks():
    """If search track form valid, return to search-track page with list of tracks. 
    Call the required function for different spotify API requests based on users search method.Store the track results in session. 
    """
    session['last_url'] = '/search-tracks'
    form_search = SearchTrackForm()

    if form_search.validate_on_submit:

        track_name = form_search.track_name.data
        artist_name = form_search.artist_name.data

        # if both track_name and artist_name fields are emtpy
        if track_name == '' and artist_name == '':
            flash(f"Please enter a song or an artist")
            return redirect('/search-tracks')

        # if searching only by track_name
        if track_name != '' and artist_name == '':
            q = f'{track_name}'
            limit = '12'
            session['search_tracks'] = API_search_by_track(q, limit)
            session['recommendation'] = False
            return redirect('/search-tracks')

        # if searching by both track_name and artist_name
        if track_name != '' and artist_name != '':
            q = f'{track_name}%20artist%3A{artist_name}'
            limit = '12'

            session['search_tracks'] = API_search_by_track(q, limit)
            session['recommendation'] = False
            return redirect('/search-tracks')

        # if searching only by artist_name
        if track_name == '' and artist_name != '':
            q = f'{artist_name}'
            limit = '1'
            artist_id = API_search_by_artist(q, limit)
            session['search_tracks'] = API_artist_top_tracks(artist_id)
            session['recommendation'] = False
            return redirect('/search-tracks')
    return redirect('/search-tracks')


@app.route('/search-tracks/genre', methods=["POST"])
def search_genre():
    """If genre form valid, return to search-track page with list of tracks. 
    Call the required function for different spotify API requests based on users search choice .Store the track results in session.
    """

    session['last_url'] = '/search-tracks'

    form_genre = SearchGenreForm()

    if form_genre.validate_on_submit:
        genre = form_genre.genre.data

        if genre == "---":  # if user selects blank option
            flash(f"Please select a genre")
            return redirect('/search-tracks')

        if genre == 'disney':  # if user selects disney
            session['search_tracks'] = API_disney_tracks()
            session['recommendation'] = False
            return redirect('/search-tracks')

        else:  # if user submits a genre
            session['search_tracks'] = API_genre_recommended_tracks(
                genre, limit=12)
            session['recommendation'] = False
            return redirect('/search-tracks')

    return redirect('/search-tracks')


@app.route('/jam/drums')
def spotify_player_drums():
    """Show spotify music player for drum playlist with keyboard instrument"""

    return render_template("spotify/spotify-player-drums.html",  favorites=session['favorite_track_ids'])


@app.route('/jam/<track_id>')
def spotify_player(track_id):
    """Show spotify music player with keyboard instrument, with list of recommended tracks based on selected track. Store Recommended tracks in session"""

    session['last_url'] = f'/jam/{track_id}'

    limit = '6'
    embed_link = f'https://open.spotify.com/embed/track/{track_id}?utm_source=generator'

    session['recommended_tracks'] = API_recommended_tracks(
        track_id, limit=limit)

    return render_template("spotify/spotify-player.html", track_id=track_id, embed_link=embed_link, tracks=session['recommended_tracks'], favorites=session['favorite_track_ids'])


########################################################################################################
# Recording


@app.route('/record')
def record_melody():
    """Show page with keyboard instrument"""
    return render_template("instrument.html")


@app.route('/get-melody', methods=['POST'])
def get_melody():
    """Route for recieving a melody object from JS as JSON if user saves a recorded melody. Save the recieved object of melody notes in session"""

    if request.method == 'POST':

        session['melody'] = str(request.get_json())

        return "OK", 200


@app.route('/save-melody', methods=['GET', 'POST'])
def save_melody():
    """Show page with for saving a recorded melody, if valid form is submitted then save melody and redirect to keyboard instrument. Clear the object of melody notes from session.   """

    if not g.user:
        flash("Log-in to save melodies.", "danger")
        return redirect("/login")
    if 'melody' not in session:
        session['melody'] = " "
    form = SaveMelodyForm()

    if form.validate_on_submit():

        melody_name = form.name.data
        melody_visibility = form.visibility.data
        now = datetime.now()
        now = now - timedelta(hours=8)
        date_time_str = now.strftime("%B-%d-%Y %H:%M")
        new_melody = Melody(user_id=g.user.id, name=melody_name,
                            music_notes=session['melody'], visibility=melody_visibility, timestamp=date_time_str)

        db.session.add(new_melody)
        db.session.commit()
        session['melody'] = "-"
        return redirect('record')
    else:
        return render_template('/users/save-melody.html', form=form)


@app.route('/delete-melody/<int:melody_id>', methods=['POST'])
def delete_melody(melody_id):
    """Delete a user's melody. If deleted form home-page, redirect back to home-page. If deleted form user page, redirect back to user page.  """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    melody = Melody.query.get_or_404(melody_id)

    if melody.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    db.session.delete(melody)
    db.session.commit()

    if session['last_url'] == '/':
        return redirect('/')
    if session['last_url'] == f'/profile/{g.user.id}':
        return redirect(f'/profile/{g.user.id}')

    return redirect('/melodies')


@app.route('/edit-melody/<int:melody_id>', methods=['POST'])
def edit_melody(melody_id):
    """Change the visibility of a users melody, then redirect back to either the user profile page or home page, depending on which page the user was last on."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    melody = Melody.query.get_or_404(melody_id)

    if melody.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    data = request.form.get('melody-visibility')
    if data == None:
        visibility = False
    else:
        visibility = True

    print(visibility)

    melody.visibility = visibility
    db.session.commit()
    if session['last_url'] == '/':
        return redirect('/')

    if session['last_url'] == f'/profile/{g.user.id}':
        return redirect(f'/profile/{g.user.id}')


########################################################################################################
# General User routes:

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profle():
    """Update profile username for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = UserEditForm(obj=g.user)

    if form.validate_on_submit():
        user = User.authenticate(g.user.username,
                                 form.password.data)
        if user:

            try:
                g.user.username = form.username.data
                db.session.commit()
                return redirect(f'profile/{g.user.id}')

            except IntegrityError:
                flash("Username already taken", 'danger')
                return render_template('users/edit-profile.html', form=form)

        else:
            flash('Incorrect Password', 'danger')
            return render_template('/users/edit-profile.html', form=form)

    else:
        return render_template('/users/edit-profile.html', form=form)


@app.route('/profile/<int:user_id>')
def user_profle(user_id):
    """Shower user profile page with their favorited tracks, and recorded melodies."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    if g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    session['last_url'] = f'/profile/{user_id}'

    favorite_tracks = [Favorited_Track.query.get(
        track.track_id) for track in User_Favorited_Track.query.filter(User_Favorited_Track.user_id == g.user.id)]
    session['last_url'] = f'/profile/{user_id}'
    favorite_tracks.reverse()

    melodies = list(Melody.query.filter(
        Melody.user_id == g.user.id).order_by(Melody.id))
    melodies.reverse()
    return render_template("users/user-profile.html", tracks=favorite_tracks, melodies=melodies)


@app.route('/track/favorite', methods=['POST'])
def toggle_favorite():
    """Recieve post request from JS with the spotify-track-id of the track a user has toggled the favorited status of. Update the user-favorited-tracks """

    if request.method == 'POST':
        data = request.get_json()
        track_id = data['trackId']

        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/")

    # If the track Id is in the session as one of the favorited_track_ids, remove track from users favorites.
    if session['favorite_track_ids'] != None and track_id in session['favorite_track_ids']:
        favorited_track = Favorited_Track.query.filter(
            Favorited_Track.spotify_track_id == track_id).first()
        track = User_Favorited_Track.query.filter(
            User_Favorited_Track.track_id == favorited_track.id).first()

        db.session.delete(track)
        db.session.commit()

        #   update favorited_track_ids in session
        favorite_tracks = [Favorited_Track.query.get(
            track.track_id) for track in User_Favorited_Track.query.filter(User_Favorited_Track.user_id == g.user.id)]

        session['favorite_track_ids'] = [
            track.spotify_track_id for track in favorite_tracks]

    else:  # If track is not in the session as one of the favorited_track_ids, add it to favorites

        # check if track is already in the favorited_tracks table. If it is, add it as a user_favorited_track for current user.
        favorited_track = Favorited_Track.query.filter(
            Favorited_Track.spotify_track_id == track_id).first()
        if favorited_track != None:
            user_favorited_track = User_Favorited_Track(
                track_id=favorited_track.id, user_id=g.user.id)
            db.session.add(user_favorited_track)
            db.session.commit()

        else:  # if track is not already in the favorited_Tracks table, add it there, and then add it as a user_favorited_track for the current user.

            for track in session['search_tracks']+session['recommended_tracks']:
                if track_id == track['track_id']:
                    favorited_track = Favorited_Track(
                        track_name=track['track_name'],
                        artist_name=track['artist_name'],
                        track_photo=track['album_image'],
                        spotify_track_id=track['track_id']
                    )

                    db.session.add(favorited_track)
                    db.session.commit()
                    user_favorited_track = User_Favorited_Track(
                        track_id=favorited_track.id, user_id=g.user.id)
                    db.session.add(user_favorited_track)
                    db.session.commit()

        # After making toggling the track's favorite status, update the user favorited_tracks_ids in the session.
        favorite_track = [Favorited_Track.query.get(
            track.track_id) for track in User_Favorited_Track.query.filter(User_Favorited_Track.user_id == g.user.id)]

        session['favorite_track_ids'] = [
            track.spotify_track_id for track in favorite_track]

    return 'OK', 200


#########################################################################################################
# definitions for Spotify API requests

def API_search_by_track(q, limit):
    """Make a request to Spotify's search API to get a list of tracks based on track name. If the auth token is no longer valid, request a new token and make the API request again."""

    res = requests.get(API_SEARCH_BASE_URL,
                       headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                'Authorization': access_token},
                       params={'q': q.replace(" ", "+"), 'type': 'track', 'limit': limit})

    data = res.json()
    check = API_check_auth(data)
    if check == False:
        res = requests.get(API_SEARCH_BASE_URL,
                           headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                    'Authorization': access_token},
                           params={'q': q.replace(" ", "+"), 'type': 'track', 'limit': limit})
        data = res.json()

    track_data = [track for track in data['tracks']['items']]
    tracks = [{"track_id": track['id'],
               "track_name":track['name'],
              "artist_name":track['artists'][0]['name'],
               "artist_id": track['artists'][0]['id'],
               "album_image":track['album']['images'][0]['url']} for track in track_data]
    return tracks


def API_search_by_artist(q, limit):
    """Make a request to Spotify's search API to get a list of tracks based on artist name. If the auth token is no longer valid, request a new token and make the API request again."""

    res = requests.get(API_SEARCH_BASE_URL,
                       headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                'Authorization': access_token},
                       params={'q': q.replace(" ", "+"), 'type': 'artist', 'limit': limit})

    data = res.json()

    check = API_check_auth(data)
    if check == False:
        res = requests.get(API_SEARCH_BASE_URL,
                           headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                    'Authorization': access_token},
                           params={'q': q.replace(" ", "+"), 'type': 'artist', 'limit': limit})

        data = res.json()

    artist_id = data['artists']['items'][0]['id']
    return artist_id


def API_artist_top_tracks(artist_id):
    """Make a request to Spotify's API for an artist's top tracks. If the auth token is no longer valid, request a new token and make the API request again."""

    res = requests.get(f'{API_TOP_BASE_URL}/{artist_id}/top-tracks',
                       headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                'Authorization': access_token},
                       params={'market': 'us'})

    data = res.json()

    check = API_check_auth(data)
    if check == False:
        res = requests.get(f'{API_TOP_BASE_URL}/{artist_id}/top-tracks',
                           headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                    'Authorization': access_token},
                           params={'market': 'us'})
        data = res.json()

    track_data = [track for track in data['tracks']]
    tracks = [{"track_id": track['id'],
               "track_name":track['name'],
              "artist_name":track['artists'][0]['name'],
               "album_image":track['album']['images'][0]['url']} for track in track_data]
    return tracks


def API_recommended_tracks(track_id, limit):
    """Make a request to Spotify's API for track recommendations based on a given track id. If the auth token is no longer valid, request a new token and make the API request again."""
    res = requests.get(API_REC_BASE_URL,
                       headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                'Authorization': access_token},
                       params={'seed_tracks': track_id, 'limit': limit, 'market': "us"})

    data = res.json()

    check = API_check_auth(data)
    if check == False:
        res = requests.get(API_REC_BASE_URL,
                           headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                    'Authorization': access_token},
                           params={'seed_tracks': track_id, 'limit': limit, 'market': "us"})

        data = res.json()

    track_data = [track for track in data['tracks']]
    tracks = [{"track_id": track['id'],
               "track_name":track['name'],
              "artist_name":track['artists'][0]['name'],
               "album_image":track['album']['images'][0]['url']} for track in track_data]
    return tracks


def API_genre_recommended_tracks(genre, limit):
    """Make a request to Spotify's API to get a list of recommended tracks based on a genre. If the auth token is no longer valid, request a new token and make the API request again."""
    res = requests.get(API_REC_BASE_URL,
                       headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                'Authorization': access_token},
                       params={'seed_genres': genre.replace(" ", "+"), 'limit': limit})

    data = res.json()

    check = API_check_auth(data)
    if check == False:
        res = requests.get(API_REC_BASE_URL,
                           headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                    'Authorization': access_token},
                           params={'seed_genres': genre.replace(" ", "+"), 'limit': limit})

        data = res.json()

    track_data = [track for track in data['tracks']]
    tracks = [{"track_id": track['id'],
               "track_name":track['name'],
              "artist_name":track['artists'][0]['name'],
               "album_image":track['album']['images'][0]['url']} for track in track_data]
    return tracks


def API_disney_tracks():
    """Make a request to Spotify's API get tracks from a pre-selected disney playlist. If the auth token is no longer valid, request a new token and make the API request again."""
    res = requests.get(f'{API_DISNEY_BASE_URL}/37i9dQZF1DX8C9xQcOrE6T/tracks',
                       headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                'Authorization': access_token},
                       params={'limit': 12, 'market': 'us'})

    data = res.json()
    check = API_check_auth(data)
    if check == False:
        res = requests.get(f'{API_DISNEY_BASE_URL}/37i9dQZF1DX8C9xQcOrE6T/tracks',
                           headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                    'Authorization': access_token},
                           params={'limit': 12, 'market': 'us'})

        data = res.json()

    track_data = [item['track'] for item in data['items']]
    tracks = [{"track_id": track['id'],
               "track_name":track['name'],
              "artist_name":track['artists'][0]['name'],
               "album_image":track['album']['images'][0]['url']} for track in track_data]
    return tracks


def API_check_auth(data):
    """Check a Spotify API resonse to determine if the access-token is still valid. Request a new access-token if the current token has expired."""
    if 'error' in data:
        if ('msg' in data['error'] and data['error']['msg'] == 'The access token expired') or ('message' in data['error'] and data['error']['message'] == 'The access token expired'):
            res = requests.post(AUTH_BASE_URL, {
                'grant_type': 'client_credentials',
                'client_id': API_CLIENT_ID,
                'client_secret': API_SECRET_KEY
            })

        data = res.json()
        global access_token
        access_token = f'Bearer {data["access_token"]}'
        return False
    return True
