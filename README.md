# ScrollWheel Media Controller

Control audio/video playback in Chrome using the **volume wheel** on your keyboard.

This tool connects a Python script that listens to the scroll wheel input with a Chrome extension that controls playback. It allows precise seeking (±5 seconds) in any media tab.

---

## How it Works

1. A small Python script (`p.py`) listens for scroll wheel input.
2. When enabled (via the **Home key**), it sends HTTP requests locally.
3. A Chrome extension receives those requests and adjusts the currently playing media (±5 seconds per tick).

---

## Features

- Toggle control mode with **Home** key
- **No global hotkeys** — just the wheel
- Works only when media is playing in Chrome
- Fully **local** — no internet or external server

---

## Setup

1. **Install the Chrome extension:**
   - Load the `/extension/` folder as an unpacked extension in Chrome.

2. **Run the Python script:**
   ```bash
   start.bat

3. Use it:
- Play a video or audio in Chrome.
- Press the Home key to toggle control mode.
- Use the volume wheel to seek ±5 seconds.

--- 

## Notes 
- p.py must stay running in the background.
- Works best with YouTube, SoundCloud, and other media sites.
- Only affects active Chrome tab with audio/video.