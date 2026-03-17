# 🍩 Simple PTZ

A browser-based PTZ camera controller for SMTAV IP cameras, optimized for iPad use during live streaming. No app install required — just open a URL in Safari.

## Features

- Control any number of cameras from a single screen (default: 4)
- Three pan/tilt control modes: 4-way D-pad, 8-way D-pad, or joystick
- Zoom and manual focus with hold-to-move buttons
- Independent speed controls for pan (1–24), tilt (1–20), and zoom (1–7)
- 12 preset positions per camera — save and recall with one tap
- User-definable camera names displayed large on each camera button
- Per-camera online/offline indicator — pings cameras every 10 seconds
- Light and dark mode toggle
- All settings and preferences saved automatically in the browser
- Camera commands stay entirely on your local network
- Works as a PWA — installable to iPad Home Screen for offline use

## Usage

Open the GitHub Pages URL on your iPad and bookmark it:

```
https://donutbrew.github.io/simpleptz/
```

Tap **⚙** to configure camera names, IP addresses, and credentials. Tap **☀/🌙** to toggle light/dark mode.

### Selecting a camera

Tap any camera button to make it the active camera. All pan/tilt/zoom/focus commands go to the selected camera. A small dot at the bottom of each button shows online (green) or offline (red) status, updated every 10 seconds.

### Pan and tilt

PTZ stands for Pan, Tilt, Zoom:

- **Pan** = left/right (horizontal rotation)
- **Tilt** = up/down (vertical rotation)
- **Zoom** = in/out

Use the **4-WAY / 8-WAY / JOY** toggle to switch between control modes. All buttons are hold-to-move — press and hold to move, release to stop.

The **8-way** mode adds diagonal buttons (↖ ↗ ↙ ↘) which send the camera's native diagonal commands (`leftup`, `rightup`, `leftdown`, `rightdown`).

The **joystick** mode lets you drag in any direction. Drag distance from center scales speed proportionally against the current pan/tilt speed slider values. The joystick snaps back to center on release and sends a stop command immediately.

Control mode preference is saved and restored on every load.

### Zoom and focus

Hold **TELE** to zoom in, **WIDE** to zoom out. Hold **NEAR** or **FAR** to adjust focus manually.

> **Note on focus:** Most PTZ cameras default to autofocus on power-up. The NEAR/FAR buttons send manual focus commands but do not automatically switch the camera into manual focus mode first. If the buttons appear to have no effect, the camera may be overriding them with autofocus. A future update will add an AF toggle to handle this properly.

### Speed sliders

Set pan, tilt, and zoom speeds independently. Having separate pan and tilt speeds is useful because:
- The tilt motor is typically slower than pan (the API reflects this: pan max is 24, tilt max is 20)
- For live streaming, you may want a faster pan across a stage but a slower tilt when following someone standing up
- The joystick uses these sliders as maximum speed caps

Speed slider values are saved and restored on every load.

### Presets

In **CALL** mode, tap a preset number to move the camera to that saved position. Switch to **SET** mode to save the current camera position to a preset slot.

Presets are stored on the camera itself, not in the app — they survive power cycles and work from any controller. The app simply sends `poscall` and `posset` commands to the camera's internal memory.

Preset mode (CALL vs SET) is saved and restored on every load.

### HOME

Returns the camera to its configured home position.

## Settings and Persistence

All settings are stored in your browser's `localStorage` — a small key-value store built into every modern browser. This means:

- **Settings survive closing the tab, restarting Safari, and rebooting your iPad.** They are not session-only.
- **Settings are per-browser and per-origin.** If you open the app in a different browser or from a different URL, it will start with the defaults. Always open from the same bookmarked URL to keep settings consistent.
- **Nothing is sent to any server.** Camera IPs, names, and credentials live only in your browser on your device.
- **Clearing Safari's website data will erase settings.** Go to Settings → Safari → Advanced → Website Data if you ever need to reset to defaults.

The following are saved to localStorage:

| Key | What it stores |
|---|---|
| `ptz_cameras` | Camera count, names, IPs, credentials |
| `ptz_theme` | Light or dark mode |
| `ptz_ctrl_mode` | Active control mode (dpad4 / dpad8 / joy) |
| `ptz_pan_speed` | Pan speed slider value |
| `ptz_tilt_speed` | Tilt speed slider value |
| `ptz_zoom_speed` | Zoom speed slider value |
| `ptz_preset_mode` | Preset mode (call / set) |
| `ptz_banner_dismissed` | Whether the PWA install banner has been dismissed |

## Camera Compatibility

Built for SMTAV PTZ cameras using the HTTP CGI API. Works with any camera that supports the SMTAV CGI command set. Default credentials are `admin` / `admin`.

## Network Requirements

Your iPad and cameras must be on the same local network. Camera commands are sent directly from Safari to each camera IP — no data leaves your network, and the app works without internet access once loaded.

The app is hosted as a static file (GitHub Pages, Netlify, etc.) — the page itself loads from the internet on first use, but all PTZ commands go directly to local IPs and the Service Worker caches the app for offline use thereafter.

## Offline Use and PWA

Simple PTZ is a Progressive Web App (PWA). Adding it to your iPad Home Screen is strongly recommended if you plan to use it on a local-only network without internet access.

### Why this matters

Safari aggressively suspends and discards background tabs to save memory. If you switch away from the app during a live stream and come back, Safari may have unloaded it and will try to reload — which fails if you're offline. Running it as a Home Screen app gives it its own process, separate from Safari's tab pool, making suspension much less likely.

### Add to Home Screen

1. Open the app URL in Safari
2. Tap the **Share** button (box-with-arrow icon)
3. Tap **Add to Home Screen**
4. Tap **Add**

A prompt appears automatically the first time you open the app on an iOS device. Tap ✕ to dismiss — it won't show again.

### Service Worker cache

The app includes a Service Worker (`sw.js`) that caches itself on first load. After the initial visit:

- The app loads instantly from local cache on every subsequent open
- It works fully offline — no internet connection needed to load the UI
- Camera commands still go directly to camera IPs on your local network as normal
- When you push an update to GitHub, the Service Worker fetches the new version in the background and activates it on next launch

To force a cache refresh after an update, bump `CACHE_VERSION` in `sw.js` (e.g. `simpleptz-v1` → `simpleptz-v2`). The Service Worker only cleans up caches prefixed with `simpleptz-` so it won't affect any other apps sharing the same GitHub Pages origin.

### App icon

The manifest references `icon-192.png` and `icon-512.png` — add these to the `app/` directory. A 512×512 PNG of the donut logo works well. iOS will use it as the Home Screen icon.

## Repo Structure

```
index.html          # Redirects to app/index.html
app/
  index.html        # Main controller UI
  sw.js             # Service Worker (offline cache)
  manifest.json     # PWA manifest
  icon-192.png      # Home Screen icon (192×192)
  icon-512.png      # Home Screen icon (512×512)
README.md
```

## API Reference

Uses the SMTAV HTTP CGI interface — all commands are plain HTTP GET requests:

| Function | URL format |
|---|---|
| Pan/Tilt | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&[up\|down\|left\|right]&[pan speed]&[tilt speed]` |
| Diagonal | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&[leftup\|rightup\|leftdown\|rightdown]&[pan speed]&[tilt speed]` |
| Stop movement | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&ptzstop&0&0` |
| Zoom | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&[zoomin\|zoomout\|zoomstop]&[speed]` |
| Focus | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&[focusin\|focusout\|focusstop]&[speed]` |
| Focus lock | `GET /cgi-bin/param.cgi?ptzcmd&lock_mfocus` |
| Autofocus | `GET /cgi-bin/param.cgi?ptzcmd&unlock_mfocus` |
| Recall preset | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&poscall&[1–12]` |
| Save preset | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&posset&[1–12]` |
| Home | `GET /cgi-bin/ptzctrl.cgi?ptzcmd&home` |
| Device info (used for online ping) | `GET /cgi-bin/param.cgi?get_device_conf` |

Full API docs: [smtav.com/blogs/how-to-use-the-camera/http-cgi-control](https://www.smtav.com/blogs/how-to-use-the-camera/http-cgi-control)

---

*Built by donutbrew — the donut hole is a camera aperture.*
