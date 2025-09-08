const circularCountdown = ({
  containerSelector = ".countdown-container",
  duration = 30,
  transition = "linear",
  color = "#c39fe0",
  size = 200,
  initialPosition = "up",
}) => {
  const countdownContainer = document.querySelector(containerSelector);
  if (!countdownContainer) return;

  countdownContainer.innerHTML = `
    <svg id="progress-wrapper" width="${size}" height="${size}" viewBox="0 0 500 500">
      <circle cx="250" cy="250" r="200" stroke="${color}" stroke-width="25" fill="transparent" id="progress" />
    </svg>
    <span class="seconds" id="seconds"></span>
  `;

  countdownContainer.style.position = "relative";

  const span = countdownContainer.querySelector(".seconds");

  span.style.position = "absolute";
  span.style.color = "#e8deee";
  span.style.fontWeight = "900";
  span.style.top = "50%";
  span.style.left = "50%";
  span.style.transform = "translate(-50%, -50%)";

  const progressWrapper = countdownContainer.querySelector("#progress-wrapper"),
    progress = countdownContainer.querySelector("#progress"),
    timeSpan = countdownContainer.querySelector("#seconds");

  // Render seconds and countdown
  let timeLeft = duration;
  timeSpan.innerHTML = timeLeft;

  // Adjust font size and circle size
  timeSpan.style.fontSize = `${size / 5}px`;
  progressWrapper.style.width = size + "px";
  progressWrapper.style.height = size + "px";

  // Set initial rotation
  if (initialPosition === "up") {
    progressWrapper.style.transform = "rotate(270deg)";
  } else if (initialPosition === "left") {
    progressWrapper.style.transform = "rotate(180deg)";
  } else if (initialPosition === "down") {
    progressWrapper.style.transform = "rotate(90deg)";
  }

  // Animation
  let length = progress.getTotalLength();
  progress.style.strokeDasharray = length;
  progress.style.strokeDashoffset = 0;
  progress.style.stroke = color;

  // Animate stroke offset over duration seconds
  let startTime = null;
  const animate = (timestamp) => {
    if (!startTime) startTime = timestamp;
    const elapsed = (timestamp - startTime) / 1000;
    if (elapsed < duration) {
      const progressOffset = length * (elapsed / duration);
      progress.style.strokeDashoffset = progressOffset;
      timeSpan.innerHTML = Math.ceil(duration - elapsed);
      requestAnimationFrame(animate);
    } else {
      progress.style.strokeDashoffset = length;
      timeSpan.innerHTML = `<i class="fa-solid fa-check"></i>`;
    }
  };

  requestAnimationFrame(animate);
};
