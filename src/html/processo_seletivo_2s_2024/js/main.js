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


document.addEventListener('DOMContentLoaded', function () {
    const row = document.querySelector('.row');
    let isDragging = false;
    let startPos = 0;
    let currentTranslate = 0;
    let prevTranslate = 0;
    let animationID;
    let currentIndex = 0;

    row.addEventListener('touchstart', touchStart);
    row.addEventListener('touchend', touchEnd);
    row.addEventListener('touchmove', touchMove);
    row.addEventListener('mousedown', touchStart);
    row.addEventListener('mouseup', touchEnd);
    row.addEventListener('mousemove', touchMove);
    row.addEventListener('mouseleave', touchEnd);

    function touchStart(event) {
      isDragging = true;
      startPos = getPositionX(event);
      animationID = requestAnimationFrame(animation);
      row.classList.add('grabbing');
    }

    function touchEnd() {
      isDragging = false;
      cancelAnimationFrame(animationID);
      const movedBy = currentTranslate - prevTranslate;

      if (movedBy < -100 && currentIndex < row.children.length - 1) currentIndex++;
      if (movedBy > 100 && currentIndex > 0) currentIndex--;

      setPositionByIndex();
      row.classList.remove('grabbing');
    }

    function touchMove(event) {
      if (isDragging) {
        const currentPosition = getPositionX(event);
        currentTranslate = prevTranslate + currentPosition - startPos;
      }
    }

    function getPositionX(event) {
      return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
    }

    function animation() {
      setSliderPosition();
      if (isDragging) requestAnimationFrame(animation);
    }

    function setSliderPosition() {
      row.style.transform = `translateX(${currentTranslate}px)`;
    }

    function setPositionByIndex() {
      currentTranslate = currentIndex * -row.children[0].clientWidth;
      prevTranslate = currentTranslate;
      setSliderPosition();
    }

    setPositionByIndex(); // Set initial position to show the edge of the next video
  });