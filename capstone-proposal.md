
# Musical Keyboard for Melody Experimentation

## Website Goal:
To entertain users by allowing them to experiment with their musical creativity and live-play melodies, and provide a place for users to record and save melodies they create.


## Website Demographics:
Anyone who is interested in playing music, particularly through a novel medium. This could be people who have a musical background and those who do not, as the musical keyboard will be simple and straightforward to use (and will have instructions for use). 

## Website Data:
I plan to use an API that provides song audio for users to search, filter through, favorite and play the songs on the website. 


## Approach:
#### Database schema:
I will store registered users in my database. Login authentication information, favorited songs, as well as saved keyboard-instrument melodies (and potentially sound settings) will be stored for each user. 

#### Potential API issues:
There may be a limited number of requests available, limited means for filtering songs, or issues with both playing the requested song file at the same time as the user plays their keyboard instrument. 

#### Is there any sensitive information you need to secure? 
User login passwords

#### App Functionality:
Users will be able to play melodies on their keyboard instrument, and then record, save, and play-back the melodies they create. Users can select a song through a music/song API, and play melodies on their keyboard instrument live while the song is playing to “jam along”. They may favorite a song to easily access and remember later. 

#### User Flow:
Website visitors will not be required to register/login to be able to play the keyboard instrument, or to record/playback melodies. Registration/login will be required for users to select, play and favorite songs through the song API, and to save any keyboard instrument melodies that they record. 

#### Beyond CRUD:
The ability to play a keyboard instrument on the website, along with users recording/saving melodies for future playback are features that are beyond CRUD. I can suggest songs from the song API to users based on what they previously searched (same artist, genre, tempo, maybe even song key). If there is time, I can implement features that allow users to adjust the settings of their keyboard instrument, such as having different tones, or maybe to convert the instrument into a drum kit. 
