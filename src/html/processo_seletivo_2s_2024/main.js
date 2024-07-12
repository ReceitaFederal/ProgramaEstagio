let videoBanner = document.getElementById('video-banner'),
    topico1 = document.getElementById('topico1'),
    topico2 = document.getElementById('topico2'),
    topico3 = document.getElementById('topico3');

// A função eventoTempo retorna outra função que será usada como o manipulador do evento click.
function eventoTempo(tempo) {
    return function(event) {
        event.preventDefault();
        videoBanner.play();
        videoBanner.pause();
        videoBanner.currentTime = tempo;
        videoBanner.play();
    }
}

topico2.addEventListener("click", eventoTempo(10), false);
topico3.addEventListener("click", eventoTempo(25), false);



// only in to demonstrate video
topico1.addEventListener("click", function () {
    if (videoBanner.paused) {
        videoBanner.play();
    } else {
        videoBanner.pause();
    }
}, false);