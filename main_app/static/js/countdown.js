document.addEventListener("DOMContentLoaded", () => {
  const countdownElements = document.querySelectorAll('.countdown');

  countdownElements.forEach(elem => {
    const startTime = new Date(elem.getAttribute('data-start')).getTime();
    const endTime = new Date(elem.getAttribute('data-end')).getTime();
    let interval;

    function updateCountdown() {
      const now = new Date().getTime();

      let targetTime;
      let isBeforeStart = now < startTime;
      let isActive = now >= startTime && now < endTime;

      if (isBeforeStart) {
        targetTime = startTime;
        if (!elem.previousElementSibling?.classList.contains('countdown-label')) {
          elem.insertAdjacentHTML('beforebegin', '<p class="countdown-label">Starts in:</p>');
        }
      } else if (isActive) {
        targetTime = endTime;
        if (!elem.previousElementSibling?.classList.contains('countdown-label')) {
          elem.insertAdjacentHTML('beforebegin', '<p class="countdown-label">Ends in:</p>');
        }
      } else {
        // Auction ended
        elem.innerHTML = "";  // Empty it (or you can choose to hide it)
        clearInterval(interval);
        return;
      }

      const distance = targetTime - now;

      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);

      elem.innerHTML = `
        <div class="countdown-pill">
          <div><strong>${days}</strong><span>Days</span></div>
          <span class="dot">•</span>
          <div><strong>${hours}</strong><span>Hour</span></div>
          <span class="dot">•</span>
          <div><strong>${minutes}</strong><span>Minutes</span></div>
          <span class="dot">•</span>
          <div><strong>${seconds}</strong><span>Seconds</span></div>
        </div>
      `;
    }

    updateCountdown();
    interval = setInterval(updateCountdown, 1000);
  });
});
