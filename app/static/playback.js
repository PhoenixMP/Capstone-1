//playback.js file is linked to the following templates: home.html, user-profile.html
//It's function is to control the playback audio of user-saved melodies.

//define audio instances as global variables for each piano note
let piano_a = new Audio('../../static/audio//piano/a5.wav')
let piano_bb = new Audio('../../static/audio//piano/a-5.wav')
let piano_b = new Audio('../../static/audio//piano/b5.wav')
let piano_c = new Audio('../../static/audio//piano/c5.wav')
let piano_csh = new Audio('../../static/audio//piano/c-5.wav')
let piano_d = new Audio('../../static/audio//piano/d5.wav')
let piano_eb = new Audio('../../static/audio//piano/d-5.wav')
let piano_e = new Audio('../../static/audio//piano/e5.wav')
let piano_f = new Audio('../../static/audio//piano/f4.wav')
let piano_fsh = new Audio('../../static/audio//piano/f-4.wav')
let piano_g = new Audio('../../static/audio//piano/g4.wav')
let piano_gsh = new Audio('../../static/audio//piano/g-4.wav')

piano_a.volume = 0;
piano_bb.volume = 0;
piano_b.volume = 0;
piano_c.volume = 0;
piano_csh.volume = 0;
piano_d.volume = 0;
piano_eb.volume = 0;
piano_e.volume = 0;
piano_f.volume = 0;
piano_fsh.volume = 0;
piano_g.volume = 0;
piano_gsh.volume = 0;



//Define two identical song arrays that are comprised of music-note objects.This array will be read by browser upon first piano key click. It results in a chromatic scale.
let BufferSong1 =
    [{ 'noteName': 'piano_f.play()', 'time': 0 },
    { 'noteName': 'piano_fsh.play()', 'time': 25 },
    { 'noteName': 'piano_g.play()', 'time': 50 },
    { 'noteName': 'piano_gsh.play()', 'time': 75 },
    { 'noteName': 'piano_a.play()', 'time': 100 },
    { 'noteName': 'piano_bb.play()', 'time': 125 },
    { 'noteName': 'piano_b.play()', 'time': 150 },
    { 'noteName': 'piano_c.play()', 'time': 175 },
    { 'noteName': 'piano_csh.play()', 'time': 200 },
    { 'noteName': 'piano_d.play()', 'time': 225 },
    { 'noteName': 'piano_e.play()', 'time': 250 },
    { 'noteName': 'piano_eb.play()', 'time': 275 }, { 'noteName': 'stopAllAudio', 'time': 275 }]

let BufferSong2 = [{ 'noteName': 'piano_f.play()', 'time': 0 },
{ 'noteName': 'piano_fsh.play()', 'time': 25 },
{ 'noteName': 'piano_g.play()', 'time': 50 },
{ 'noteName': 'piano_gsh.play()', 'time': 75 },
{ 'noteName': 'piano_a.play()', 'time': 100 },
{ 'noteName': 'piano_bb.play()', 'time': 125 },
{ 'noteName': 'piano_b.play()', 'time': 150 },
{ 'noteName': 'piano_c.play()', 'time': 175 },
{ 'noteName': 'piano_csh.play()', 'time': 200 },
{ 'noteName': 'piano_d.play()', 'time': 225 },
{ 'noteName': 'piano_e.play()', 'time': 250 },
{ 'noteName': 'piano_eb.play()', 'time': 275 }, { 'noteName': 'stopAllAudio', 'time': 275 }]



//Initialize gobal varibles used to track conditions for audio playback
let song = []
let recording = false;
let timeStart = 0
let timeout
let timeouts = []
let audioIsPlaying = false
let buffer = true


//define global variables for user-interavtive page elements 
let playMelodyButton = document.getElementsByClassName('play-melody');
let bufferingAnnouncement = document.getElementById('melody-header');


//functions for playing the audio for each piano key when called from a music-note object
function playPiano_a() {
    piano_a.pause();
    piano_a.currentTime = 0.01;
    piano_a.play()
}

function playPiano_bb() {
    piano_bb.pause();
    piano_bb.currentTime = 0.01;
    piano_bb.play()
}

function playPiano_b() {
    piano_b.pause();
    piano_b.currentTime = 0.01;
    piano_b.play()
}

function playPiano_c() {
    piano_c.pause();
    piano_c.currentTime = 0.01;
    piano_c.play()
}

function playPiano_csh() {
    piano_csh.pause();
    piano_csh.currentTime = 0.01;
    piano_csh.play();
}

function playPiano_d() {
    piano_d.pause();
    piano_d.currentTime = 0.01;
    piano_d.play()
}

function playPiano_eb() {
    piano_eb.pause();
    piano_eb.play()
    piano_eb.currentTime = 0.01;
}

function playPiano_e() {
    piano_e.pause();
    piano_e.currentTime = 0.01;
    piano_e.play()
}

function playPiano_f() {
    piano_f.pause();
    piano_f.currentTime = 0.01;
    piano_f.play()
}

function playPiano_fsh() {
    piano_fsh.pause();
    piano_fsh.currentTime = 0.01;
    piano_fsh.play()
}

function playPiano_g() {
    piano_g.pause();
    piano_g.currentTime = 0.01;
    piano_g.play()
}

function playPiano_gsh() {
    piano_gsh.pause();
    piano_gsh.currentTime = 0.01;
    piano_gsh.play()
}


//Function to pause all audio instances 
function stopAllAudio() {
    piano_a.pause()
    piano_bb.pause()
    piano_c.pause()
    piano_csh.pause()
    piano_d.pause()
    piano_e.pause()
    piano_eb.pause()
    piano_f.pause()
    piano_fsh.pause()
    piano_g.pause()
    piano_gsh.pause()
    piano_b.pause()
}

//Function to return the volume of all audio elements
function returnAudio() {
    piano_a.volume = 1;
    piano_bb.volume = 1;
    piano_b.volume = 1;
    piano_c.volume = 1;
    piano_csh.volume = 1;
    piano_d.volume = 1;
    piano_eb.volume = 1;
    piano_e.volume = 1;
    piano_f.volume = 1;
    piano_fsh.volume = 1;
    piano_g.volume = 1;
    piano_gsh.volume = 1;
}

//Function to play the audio that results from a for-loop over the song array. 
//A setTimeout is made for each index/object in the song array, where the object noteName value is the timeout function and the object time value is the timeout time.
//All timeouts are pushed to the timeout array so that all timeouts can be cleared (ceasing all setTimeout audio).
function playSong() {
    timeouts = []
    for (let note in song) {
        timeout = setTimeout(song[note].noteName, song[note].time);
        timeouts.push(timeout)
    }
}

//Function to change the stop-button back to showing a "play" symbol when clicked, for all play buttons. 
function togglePlayButton() {
    for (let i = 0; i < playMelodyButton.length; i++) {
        playMelodyButton[i].firstChild.src = "/static/images/play-button.png"
        audioIsPlaying = false
    }
}


//Functions that are similar to "playSong", but instead they will only produce timeouts for the "buffer" song array.
//This function results in the browser playing the audio of a chromatic scale
function playBuffer2() {
    for (let note in BufferSong2) {
        setTimeout(BufferSong2[note].noteName, BufferSong2[note].time);
    }
}

function playBuffer1() {
    for (let note in BufferSong1) {
        setTimeout(BufferSong1[note].noteName, BufferSong1[note].time);
    }
}





//Click event listener for all the play-recording buttons. This button is toggled between showing a play-symbol and a stop-symbol. 
//When clicked the first time, the play-symbol changes to a stop-symbol, the song array text that's located on the target elements div is saved, the playSong function is called, 
//and a timeout is set to convert the stop-symbol back to a play-symbol when shortly after the last note of the song is played.
//If clicked before a song has finsihed playing, all timeouts for note audio are cleared, all audio is paused, and the play-button reappears.
//The first time any play-button is pushed will result in "buffering", where the browser reads a buffer arrray x3 to play the audio chomatic scale at 3 different timeouts. 
//The buffering is done to help the browser speed, where subsequently played melodies will have the audio lag less.
for (let i = 0; i < playMelodyButton.length; i++) {
    playMelodyButton[i].onclick = (e) => {


        if (buffer === true) {
            e.currentTarget.firstChild.src = "/static/images/buffering.png"
            bufferingAnnouncement.innerText = 'Buffering -- Just a Moment!'
            playBuffer1()
            setTimeout(playBuffer2, 3500)
            setTimeout(playBuffer1, 6000)
            setTimeout(togglePlayButton, 6000)
            setTimeout(() => { bufferingAnnouncement.innerText = 'Buffering Finished. Please Click again' }, 6000)
            buffer = false

        }


        else {
            stopAllAudio();
            returnAudio();
            if (audioIsPlaying === true) {
                e.currentTarget.firstChild.src = "/static/images/play-button.png"
                for (const x of timeouts) {
                    clearTimeout(x)
                }
                timeouts = []
                stopAllAudio()
                togglePlayButton()

            }
            else {
                bufferingAnnouncement.innerText = 'Listen to Shared Melodies'
                audioIsPlaying = true
                e.currentTarget.firstChild.src = "/static/images/stop-button.png"

                songData = e.currentTarget.nextElementSibling.textContent
                song = songData.split("{'song': ").pop();
                song = eval(song.slice(0, -1));
                song.forEach(note => {
                    note.noteName = eval(note.noteName)
                })

                const time = song[song.length - 1].time
                playSong()

                togglePlay = setTimeout(togglePlayButton, time + 1000)
                timeouts.push(togglePlay)
            }
        }
    }
}





