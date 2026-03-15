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

## Offline Use and PWA

Simple PTZ is a Progressive Web App (PWA). Adding it to your iPad Home Screen is strongly recommended if you plan to use it on a local-only network without internet access.

### Why this matters

Safari aggressively suspends and discards background tabs to save memory. If you switch away from the app during a live stream and come back, Safari may have unloaded it and will try to reload — which fails if you're offline. Running it as a Home Screen app gives it its own process, separate from Safari's tab pool, making suspension much less likely.

### Add to Home Screen

1. Open the app URL in Safari
2. Tap the **Share** button (⎋ box-with-arrow icon)
3. Tap **Add to Home Screen**
4. Tap **Add**

A prompt will also appear automatically the first time you open the app on an iOS device (tap ✕ to dismiss and never show again).

### Service Worker cache

The app includes a Service Worker (`sw.js`) that caches itself on first load. After the initial visit:

- The app loads instantly from local cache on every subsequent open
- It works fully offline — no internet connection needed to load the UI
- Camera commands still go directly to camera IPs on your local network as normal
- When you push an update to GitHub, the Service Worker fetches the new version in the background and activates it on next launch

To force a cache refresh (e.g. after updating the app), bump `CACHE_VERSION` in `sw.js`.

### App icon

The manifest references `icon-192.png` and `icon-512.png` — you'll need to add these to the `app/` directory. Create a 512×512 PNG of the donut logo for best results on all devices. iOS will use it as the Home Screen icon.



```
index.html        # Redirects to app/index.html
app/
  index.html      # Main controller UI
  sw.js           # Service Worker (offline cache)
  manifest.json   # PWA manifest
  icon-192.png    # Home Screen icon (192×192)
  icon-512.png    # Home Screen icon (512×512)
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
