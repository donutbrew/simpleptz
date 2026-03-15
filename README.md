# SimplePTZ

# PTZ Camera Controller

A browser-based PTZ camera controller for SMTAV IP cameras, optimized for iPad use during live streaming.

## Features

- Control up to 4 cameras from a single screen
- Pan, tilt, zoom, and focus with hold-to-move buttons
- Independent speed controls for pan, tilt, and zoom
- 12 preset positions per camera (save and recall)
- Camera configuration saved in browser localStorage
- No app install required — runs in Safari

## Usage

Open the GitHub Pages URL on your iPad and bookmark it:

```
https://donutbrew.github.io/simpleptz/
```

Tap the **⚙** button to configure each camera's name, IP address, and credentials. Settings persist across sessions.

## Camera Compatibility

Built for SMTAV PTZ cameras using the HTTP CGI API. Tested on cameras with the default `admin/admin` credentials on a local network.

## Network Requirements

The iPad and cameras must be on the same local network. Camera commands are sent directly from the browser to each camera IP — no data leaves your local network.

## Files

```
index.html        # Redirects to ptz/app.html
ptz/
  app.html        # Main controller UI
README.md
```

## API Reference

Control commands use the SMTAV HTTP CGI interface:

- **Pan/Tilt:** `GET /cgi-bin/ptzctrl.cgi?ptzcmd&[action]&[pan speed]&[tilt speed]`
- **Zoom:** `GET /cgi-bin/ptzctrl.cgi?ptzcmd&[zoomin|zoomout|zoomstop]&[speed]`
- **Preset:** `GET /cgi-bin/ptzctrl.cgi?ptzcmd&[poscall|posset]&[1-12]`
- **Home:** `GET /cgi-bin/ptzctrl.cgi?ptzcmd&home`

Full API docs: [smtav.com/blogs/how-to-use-the-camera/http-cgi-control](https://www.smtav.com/blogs/how-to-use-the-camera/http-cgi-control)