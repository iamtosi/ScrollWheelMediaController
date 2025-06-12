let socket = null;
let reconnectTimeout = null;

function setupWebSocket() {
  if (socket) {
    try {
      socket.close();
    } catch (e) {}
  }

  socket = new WebSocket("ws://localhost:8765");

  socket.onopen = () => {
    console.log("✅ WebSocket подключен");
  };

  socket.onmessage = (event) => {
    const command = event.data;
    if (command === "forward" || command === "rewind") {
      chrome.tabs.query({}, function (tabs) {
        for (let tab of tabs) {
          if (
            tab.url &&
            (tab.url.includes("youtube.com/watch") ||
             tab.url.includes("music.youtube.com"))
          ) {
            chrome.scripting.executeScript({
              target: { tabId: tab.id },
              func: (dir) => {
                const video = document.querySelector("video");
                if (video) {
                  video.currentTime += dir === "forward" ? 5 : -5;
                }
              },
              args: [command]
            });
          }
        }
      });
    }
  };

  socket.onclose = () => {
    console.warn("🔁 WebSocket отключён. Переподключаем через 2с...");
    reconnectTimeout = setTimeout(setupWebSocket, 2000);
  };

  socket.onerror = (err) => {
    console.warn("⚠️ Ошибка WebSocket:", err.message);
    try {
      socket.close();
    } catch (e) {}
  };
}

setupWebSocket();

chrome.alarms.create("keepAlive", { periodInMinutes: 0.5 });

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "keepAlive") {
    console.debug("⏰ Пингую, чтобы не уснул service worker");
  }
});