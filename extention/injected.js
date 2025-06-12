// injected.js
window.addEventListener("message", (event) => {
    if (event.source !== window) return;
  
    const { type, direction } = event.data;
    if (type === "YT_CONTROL") {
      const video = document.querySelector("video");
      if (video) {
        video.currentTime += direction === "forward" ? 5 : -5;
      }
    }
  });
  