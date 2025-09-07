document.addEventListener("DOMContentLoaded", () => {
  const countdownElements = document.querySelectorAll('.countdown');

  countdownElements.forEach(elem => {
    const timeString = elem.getAttribute('data-time')

    const targetTime = new Date(timeString.replace(' ', 'T')).getTime();

    function updateCountdown() {
      const now = new Date().getTime();
      const distance = targetTime - now;

      if (distance < 0) {
        elem.innerHTML = "EXPIRED"
        clearInterval(interval)
        return
      }

      const days = Math.floor(distance / (1000 * 60 * 60 * 24))
      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
      const seconds = Math.floor((distance % (1000 * 60)) / 1000)

      elem.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`
    }

    updateCountdown(); 
    const interval = setInterval(updateCountdown, 1000)
  })
})
