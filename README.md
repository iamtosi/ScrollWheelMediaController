# ScrollWheel Media Controller

This tool allows you to seek (rewind/forward) audio or video in Chrome using the volume dial on your keyboard.

### How it works:
- A small Python app listens for scroll wheel input.
- When active (toggle via Home key), it sends local HTTP requests.
- A Chrome extension (included) receives those requests and controls the active media tab.
- Media jumps forward/backward by 5 seconds per tick.

### Features:
- Toggle mode with Home key
- No global hotkeys, just wheel control
- Works only when media is playing in Chrome
- Fully local – no internet connection required

### Setup:
1. Install the Chrome extension (`extension/` folder).
2. Run the Python script (start.bat).
3. Play audio or video in Chrome and toggle control mode with the Home key.
