
# Melodic 
Deployed on Render: https://melodic-play.onrender.com/


### About Melodic
Melodic is a melody-making website for users to play a virtual piano with their computer's keyboard. Users can jam along using their piano-keyboard with any searched Spotify music track of their choice. They can also use their piano-keyboard to record and save their created melodies, with the option to share these melodies for other users to listen to. 

### Website Features
#### __Search Tracks__
User's can submit search requests for music tracks, and data from these searches are sent as a request to one of various Spotify Web API endpoints to receive relevant track options to select from. Search options include track and/or artist name, by genre, or a drum-playlist. 

These flexible search-options help to increase the odds that the user will find their desired track or music-type with a single search. The option for the user to select from drum-tracks rather than solely music-based tracks provides an alternative jam experience that allows for more free-style playing that requires less harmonic coordination.

#### __Track Recommendations__
When navigating to the search-track page for the first time in a session, users are provided with a list of selectable track recommendations. These recommendations are acquired from the "Get Recommendations" endpoint of the Spotify Web API, using a pre-selected and hard-coded seed-track that I chose. Any track a user selects will be the new seed-track in another API request for updated recommended tracks, and these new tracks are displayed on the jam page.

The continuously updating recommendations serve to aid the user in subsequent track selection, and can inspire the user to explore new music opportunities that are relevant to them. 

#### __Jam Along__
After selecting a track and being redirected to the jam page, users are presented with an interactive piano with playable keys. Each piano key will produce the audio of its accurately corresponding piano note when clicked. The piano keys can be clicked with a mouse or a keyboard button press, where each key is mapped to one keyboard button. Through this feature, a user can simulate playing the piano on the screen through typing on their computer keyboard. The user's selected track is also displayed on the screen as an iframe with a play-button, and the audio of the track can be played simultaneously with the audio of the played piano instrument. 

Pairing a Spotify track with a user's "piano playing" simulates the experience of an entertaining musical jam session.

#### __Optional Sign-Up/Log-In__
The majority of this website's functionality is accessible to users who do not have an account or are not logged in. Requiring an account can be a burdensome deterrent for a user that discourages them from utilizing a website. Any feature where there is no functional or security benefit to requiring an account will not require one. However, users do have the option make an account and log in to gain the features of saving and sharing their recorded piano melodies, or favoriting Spotify tracks. 

Placing just a few of the website's features behind a sign-up requirement helps to increase the scope of potential users by catering to different intentions of use. 

#### __Favorite Tracks__
All music tracks that are displayed to logged in accountholders have a toggleable heart icon. When clicked, these icons toggle between empty hearts and hearts with a red fill. A heart with a red fill indicates that a track has been favorited. All favorited tracks are displayed on a users' profile page, and clicking one will direct the user back to the jam page with its iframe. 

This feature makes it easier for users to remember tracks that they enjoyed jamming along with and may want to return to later. 

#### __Record/Save/Playback Melody__
This website also includes a page that contains only the playable piano, without any tracks or other audio sources. The piano functions in the same way that it does on the jam page with the added functionality of recording and playing back the melodies that they produce on the piano. Users who are logged in also have the option to save their recorded melody. Saved melodies are named and displayed on a users' profile page, where users will have the option to delete, play back the audio of, or to toggle the visibility of their melodies. 

The ability for users to record and save melodies allows them to create a snapshot of their progress and to enjoy the melody again at a later date without having to remember how to play it. 

#### __Share Saved Melodies__ 
Users have the option to toggle the visibility of each of their saved melodies. Melodies that are visible appear on the home page for any website user (with or without an account) to view  and play their audio. A user with a shared melody can toggle the visibility off while viewing it on the homepage, and doing so will remove that melody from the homepage until the visibility is toggled back on from the user's profile page. 

This feature is one of the first that a user is presented with when visiting the website. It provides a kind of social element with users sharing their created melodies with each other, and it can motivate new users to create an account to record and contribute their own melody to the home page. 

### User Flow Diagram
Created with Lucidchart
![images not avaialble](/md-images/UserFlow.jpeg)
### Database Schema
Created with GenMyModel Database Diagram Online
![images not avaialble](/md-images/DatabaseDiagram.jpeg)

### Spotify Web API

[General Spotify Web API](https://developer.spotify.com/documentation/web-api/)

[Client Credentials Flow](https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/)

This website utilizes the Client Credentials flow with the Spotify Web API. Requests are made to a variety of different endpoints depending on which form the user is submitting for their track search. The search-track page and the jam page both make requests to the "Get Recommendations" endpoint to show suggested tracks to the user based on previously selected tracks, using a track id as the query parameter. 
If a user submits a search for a track name, with or without an artist name included, requests are made to the Get Track endpoint, with the track name (along with the artist name, if provided) as the query parameter. 
If a user submits a request for only an artist name, requests are made to first the Get Artist endpoint, and with that artist id as the query parameter a request is made to the Get Artist's Top Tracks endpoint. 
If a user selects one of the genre options (not including Disney), requests are made to the Get Recommendations endpoint with the genre name as the "seed_genre" for the query parameter.
If a user selects the Disney genre option, a request is made to the Get Playlist Items using a hard-coded predetermined playlist id as the query parameter. 
No API calls are made if a user chooses the "Play Drum Tracks" option. The playlist of drum tracks is generated from an iframe provided by the general Spotify website.  

### Tech Stack
Front End:
-HTML5
-CSS
-JavaScript
Back End:
-Python3
-PostgreSQL
-Flask

### Additional Notes

#### __Melody Recording/Playback Logic__
The audio for melodies is produced by the browser reading a "song" array that contains instructions for playing the piano's music notes. Each object in the array has two key-value pairs - one for indicating which note is to be played, and one for indicating the time to wait after the previous note was played. When a user clicks the record button, each subsequently pressed piano key results in a music note object being pushed into the array, until the user clicks the stop-recording button. To play back the recorded melody, a for loop sets a timeout for each object in the song array, resulting in a cascade of audio notes playing with the same melody as the user produced. When saved by a user, these "song" arrays are stored on the database. They can be played back in the same way upon a user's request. 

This method of recording, saving, and reproducing audible melodies replaces any need for the creation of new unique audio files, and it allows for a simple and efficient way for melodies to be sent to and retrieved from the database. 

A challenge that resulted from this method of audio playback came from either a delay in setting or retrieving the timeouts for playing the music note audio. I noticed that the first two or three attempts to play back a melody on a freshly rendered browser window resulted in an inaccurate sounding melody. By the third or fourth attempt, the melody playback for any other melody on the page would be accurate. The workaround introduced to promote melody accuracy was a buffer function that occurs on the first click of a melody playback button on a newly rendered window. The browser plays a chromatic scale using timeouts, three times in a row. By the third time, any problem with the accuracy of timeouts is mostly resolved, and any subsequent playbacks of any melodies on the page sound accurate. 



#### __CSS Credit__
The virtual piano CSS utlized code from user Philip Zalstrow at CodePen
https://codepen.io/zastrow/pen/kxdYdk

The login/signup and search-track buttons utilized code from user foxiesen at CodePen
https://codepen.io/foxeisen/pen/bqZxLa





