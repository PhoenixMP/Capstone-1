//favorites.js is linked in the following templates: user-profile.html, search-tracks.html, spotify-player.html
//The function of this file is to toggle tracks between favorited/unfavorited for logged-in users. 
//Clicked "hearts" will toggle between filled-in red hearts, and empty hearts. A heart-click results in post request sent to python with the corresponding spotify-track-id, 
//where python will update the favorited status of the track accordingly.

let favoriteButton = document.getElementsByClassName("fa");


for (var i = 0; i < favoriteButton.length; i++) {
    favoriteButton[i].onclick = (e) => {

        console.log('hello')
        e.currentTarget.classList.toggle("fa-heart-o")
        e.currentTarget.classList.toggle("fa-heart")


        let trackId = e.currentTarget.id



        fetch('/track/favorite', {

            // Declare what type of data we're sending
            headers: {
                'Content-Type': 'application/json'
            },

            // Specify the method
            method: 'POST',

            // A JSON payload
            body: JSON.stringify({
                trackId
            })
        }).then(function (response) { // At this point, Flask has printed our JSON
            return response.text();
        }).then(function (text) {

            console.log('POST response: ');

            // Should be 'OK' if everything was successful
            console.log(text);


        });
        if (e.currentTarget.classList.contains('user-page')) {
            e.currentTarget.parentElement.remove()
        }
    };
}
