# 🍩 Simple PTZ

A browser-based PTZ camera controller for SMTAV IP cameras, optimized for iPad use during live streaming. No app install required — just open a URL in Safari.

## Features

- Control any number of cameras from a single screen (default: 4)
- Pan, tilt, zoom, and focus with hold-to-move buttons
- Independent speed controls for pan (1–24), tilt (1–20), and zoom (1–7)
- 12 preset positions per camera — save and recall with one tap
- User-definable camera names
- Light and dark mode toggle
- All settings saved automatically in the browser — no account needed
- Camera commands stay entirely on your local network

## Usage

Open the GitHub Pages URL on your iPad and bookmark it:

```
https://[username].github.io/[repo-name]/
```

Tap **⚙** to configure camera names, IP addresses, and credentials. Tap **☀/🌙** to toggle light/dark mode.

### Controls

| Control | How it works |
|---|---|
| Camera buttons | Tap to select the active camera |
| D-pad | Hold to move, release to stop |
| Tele / Wide | Hold to zoom, release to stop |
| Near / Far | Hold to adjust focus, release to stop |
| Speed sliders | Set pan, tilt, and zoom speeds independently |
| Presets | In **CALL** mode, tap to go to a preset. Switch to **SET** mode to save the current position. |
| HOME | Return camera to home position |

## Settings and Persistence

All settings are stored in your browser's `localStorage` — a small key-value store built into every modern browser. This means:

- **Settings survive closing the tab, restarting Safari, and rebooting your iPad.** They are not session-only.
- **Settings are per-browser and per-origin.** If you open the app in a different browser or from a different URL, it will start with the defaults. Bookmarking the same URL and always opening from that bookmark keeps everything consistent.
- **Nothing is sent to any server.** Camera IPs, names, and credentials live only in your browser on your device.
- **Clearing Safari's website data will erase settings.** Go to Settings → Safari → Advanced → Website Data if you ever need to reset to defaults.

Settings stored include: camera count, names, IP addresses, credentials, and light/dark mode preference.

## Camera Compatibility

Built for SMTAV PTZ cameras using the HTTP CGI API. Works with any camera that supports the SMTAV CGI command set. Default credentials are `admin` / `admin`.

## Network Requirements

Your iPad and cameras must be on the same local network. Camera commands are sent directly from Safari to each camera IP — no data leaves your network, and the app works without internet access once loaded.

The app is hosted as a static file (GitHub Pages, Netlify, etc.) — the page itself loads from the internet, but all PTZ commands go directly to local IPs.

## Repo Structure

```
index.html        # Redirects to ptz/app.html
ptz/
  app.html        # Main controller UI
README.md
```

## API Reference

Uses the SMTAV HTTP CGI interface — all commands are plain HTTP GET requests:

| Function | URL format |
|---|---|
| Pan/Tilt | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&[up\|down\|left\|right]&[pan speed]&[tilt speed]` |
| Stop movement | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&ptzstop&0&0` |
| Zoom | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&[zoomin\|zoomout\|zoomstop]&[speed]` |
| Focus | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&[focusin\|focusout\|focusstop]&[speed]` |
| Recall preset | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&poscall&[1–12]` |
| Save preset | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&posset&[1–12]` |
| Home | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&home` |

Full API docs: [smtav.com/blogs/how-to-use-the-camera/http-cgi-control](https://www.smtav.com/blogs/how-to-use-the-camera/http-cgi-control)
