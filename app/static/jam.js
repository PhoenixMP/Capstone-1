//jam.js file is linked to the following templates: spotify-player.html, spotify-player-drums.html
//It's function is to control the audio and playability for the piano

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


//define global variables for user-interavtive page elements 
const keyboardHelp = document.getElementById('keyboard');
const viewKeyboardIcon = document.getElementById('view-keyboard');
const jamCue = document.getElementById("jam-cue")
keyboardHelp.style.visibility = 'hidden';

//define global variables for each key on the interactive keyboard piano 
const bKey = document.getElementById('b');
const bbKey = document.getElementById('bb');
const aKey = document.getElementById('a');
const gsKey = document.getElementById('gs');
const gKey = document.getElementById('g');
const fsKey = document.getElementById('fs');
const fKey = document.getElementById('f');
const eKey = document.getElementById('e');
const ebKey = document.getElementById('eb');
const dKey = document.getElementById('d');
const csKey = document.getElementById('cs');
const cKey = document.getElementById('c');

//Define a song array that is comprised of music-note objects.This array will be read by browser upon first piano key click. It results in a chromatic scale.
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
    { 'noteName': 'piano_eb.play()', 'time': 275 },
    { 'noteName': 'returnAudio()', 'time': 2500 }]



//Initialize gobal varibles used to track conditions for audio playback
let song = [];
let timeStart = 0
let timeout
let timeouts = []
let audioIsPlaying = false
let buffer = true


//functions for animating/playing the audio for each piano key after clicked by a user
function playPiano_a() {
    aKey.classList.add("active");
    setTimeout(() => {
        aKey.classList.remove("active")
    }, 500)
    piano_a.pause();
    piano_a.currentTime = 0.01;
    piano_a.play()
}

function playPiano_bb() {
    bbKey.classList.add("active");
    setTimeout(() => {
        bbKey.classList.remove("active")
    }, 500)
    piano_bb.pause();
    piano_bb.currentTime = 0.01;
    piano_bb.play()
}

function playPiano_b() {
    bKey.classList.add("active");
    setTimeout(() => {
        bKey.classList.remove("active")
    }, 500)
    piano_b.pause();
    piano_b.currentTime = 0.01;
    piano_b.play()
}

function playPiano_c() {
    cKey.classList.add("active");
    setTimeout(() => {
        cKey.classList.remove("active")
    }, 500)
    piano_c.pause();
    piano_c.currentTime = 0.01;
    piano_c.play()
}

function playPiano_csh() {
    csKey.classList.add("active");
    setTimeout(() => {
        csKey.classList.remove("active")
    }, 500)
    piano_csh.pause();
    piano_csh.currentTime = 0.01;
    piano_csh.play();
}

function playPiano_d() {
    dKey.classList.add("active");
    setTimeout(() => {
        dKey.classList.remove("active")
    }, 500)
    piano_d.pause();
    piano_d.currentTime = 0.01;
    piano_d.play()
}

function playPiano_eb() {
    ebKey.classList.add("active");
    setTimeout(() => {
        ebKey.classList.remove("active")
    }, 500)
    piano_eb.pause();
    piano_eb.play()
    piano_eb.currentTime = 0.01;
}

function playPiano_e() {
    eKey.classList.add("active");
    setTimeout(() => {
        eKey.classList.remove("active")
    }, 500)
    piano_e.pause();
    piano_e.currentTime = 0.01;
    piano_e.play()
}

function playPiano_f() {
    fKey.classList.add("active");
    setTimeout(() => {
        fKey.classList.remove("active")
    }, 500)
    piano_f.pause();
    piano_f.currentTime = 0.01;
    piano_f.play()
}

function playPiano_fsh() {
    fsKey.classList.add("active");
    setTimeout(() => {
        fsKey.classList.remove("active")
    }, 500)
    piano_fsh.pause();
    piano_fsh.currentTime = 0.01;
    piano_fsh.play()
}

function playPiano_g() {
    gKey.classList.add("active");
    setTimeout(() => {
        gKey.classList.remove("active")
    }, 500)
    piano_g.pause();
    piano_g.currentTime = 0.01;
    piano_g.play()
}

function playPiano_gsh() {
    gsKey.classList.add("active");
    setTimeout(() => {
        gsKey.classList.remove("active")
    }, 500)
    piano_gsh.pause();
    piano_gsh.currentTime = 0.01;
    piano_gsh.play()
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


//Function that is similar to "playSong", but instead it will only produce timeouts for the "buffer" song array.
//This function results in the browser playing the audio of a chromatic scale
function playBuffer1() {
    for (let note in BufferSong1) {
        setTimeout(BufferSong1[note].noteName, BufferSong1[note].time);
    }
    enableClickEvents();
}

//Click event listener set on the view-keyboard icon. Toggles the display for the an image that illustrates which keyboard keys are associated with which piano key.
viewKeyboardIcon.addEventListener('click', () => {
    if (keyboardHelp.style.visibility === 'hidden') {
        keyboardHelp.style.visibility = 'visible'
    }
    else {
        keyboardHelp.style.visibility = 'hidden'
    }
})


//Click event listeners added to all piano key audio elements. When a key is pressed, the function for playing the note audio is called. 
function enableClickEvents() {
    bKey.addEventListener('click', (evt) => {
        playPiano_b()
    })

    bbKey.addEventListener('click', (evt) => {
        playPiano_bb()
    })

    aKey.addEventListener('click', (evt) => {
        playPiano_a()
    })

    gsKey.addEventListener('click', (evt) => {
        playPiano_gsh()
    })

    gKey.addEventListener('click', (evt) => {
        playPiano_g()
    })

    fsKey.addEventListener('click', (evt) => {
        playPiano_fsh()
    })

    fKey.addEventListener('click', (evt) => {
        playPiano_f()
    })

    eKey.addEventListener('click', (evt) => {
        playPiano_e()
    })

    ebKey.addEventListener('click', (evt) => {
        playPiano_eb()
    })

    dKey.addEventListener('click', (evt) => {
        playPiano_d()
    })

    csKey.addEventListener('click', (evt) => {
        playPiano_csh()
    })

    cKey.addEventListener('click', (evt) => {
        playPiano_c()
    })
}


//Keydown event listeners for each key that corresponds to a piano note element. If pressed, the "click" on that piano piano note element is simulated.
//If no key has been pushed yet, the first push will result in "buffering", where the browser reads the buffer arrray to play the audio chomatic scale. 
//The buffering is done to help the browser speed, where subsequently played notes will have the audio lag less.
window.addEventListener('keydown', function (e) {

    if (buffer === true) {

        jamCue.innerText = 'Buffering -- Just a Moment!'
        playBuffer1()
        setTimeout(() => { jamCue.innerText = '( Buffering Finished -- Click in browser window to jam along)' }, 2000)

        buffer = false

    } else {



        // keyboard stroke "a", piano note F
        if (
            e.key == "a" || e.key == "A") {
            fKey.click()
        }


        // keyboard stroke "w", piano note F#
        if (
            e.key == "w" || e.key == "W") {
            fsKey.click()


        }

        // keyboard stroke "s", piano note G
        if (
            e.key == "s" || e.key == "S") {
            gKey.click()

        }

        // keyboard stroke "e", piano note G#
        if (
            e.key == "e" || e.key == "E") {
            gsKey.click()

        }

        // keyboard stroke "d", piano note A
        if (
            e.key == "d" || e.key == "D") {
            aKey.click()

        }

        // keyboard stroke "r", piano note Bb
        if (
            e.key == "r" || e.key == "R") {
            bbKey.click()

        }

        // keyboard stroke "f", piano note B
        if (
            e.key == "f" || e.key == "F") {
            bKey.click()

        }

        // keyboard stroke "g", piano note C
        if (
            e.key == "g" || e.key == "G") {
            cKey.click()

        }

        // keyboard stroke "y", piano note C#
        if (
            e.key == "y" || e.key == "Y") {
            csKey.click()

        }

        // keyboard stroke "h", piano note D
        if (
            e.key == "h" || e.key == "H") {
            dKey.click()


        }

        // keyboard stroke "u", piano note Eb
        if (
            e.key == "u" || e.key == "U") {
            ebKey.click()

        }


        // keyboard stroke "j", piano note E
        if (
            e.key == "j" || e.key == "J") {
            eKey.click()

        }
    }

});

