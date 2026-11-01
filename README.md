# FieldOps Studio

FieldOps Studio is a browser-based mapping tool for planning field operations. It lets a user draw zones and place pins on either a live interactive map or a custom uploaded image (such as a floor plan or blueprint), then export the result as a PNG image.

## Overview

The application is served by a small FastAPI backend that returns a single static HTML page. All application logic, styling, and interactivity live client-side in that page. There is no database or persistent storage; all zones and pins exist only in the browser session and are lost on page reload.

## Project Structure

```
.
├── main.py       FastAPI server that serves the frontend
└── index.html    Single-page application (HTML, CSS, JavaScript)
```

## Requirements

- Python 3.8 or later
- Packages: `fastapi`, `uvicorn`

Install dependencies with:

```
pip install fastapi uvicorn
```

## Running the Application

From the project directory, run:

```
python main.py
```

By default the server starts on `http://127.0.0.1:8000`. The host and port can be overridden with environment variables:

```
HOST=0.0.0.0 PORT=9000 python main.py
```

Alternatively, the app can be run directly with uvicorn:

```
uvicorn main:app --reload
```

Once running, open the printed URL in a browser to load FieldOps Studio.

## Backend Behavior (main.py)

The backend exposes a single route:

- `GET /` — Reads `index.html` from the working directory and returns it as an HTML response. If the file is missing, it returns a 404 response with a simple fallback message.

The server has no other routes, no API endpoints, and no data persistence layer. Its only responsibility is serving the frontend file.

## Frontend Features (index.html)

The frontend is a single HTML file that uses the following external libraries, loaded via CDN:

- Tailwind CSS for styling
- Leaflet for interactive mapping
- html2canvas for exporting the map view as an image
- Font Awesome for icons
- Google Fonts (Inter) for typography

### Map Mode

The default view is an interactive Leaflet map. Users can:

- Search for a location by name using the OpenStreetMap Nominatim search API
- Fly to specific latitude and longitude coordinates entered manually
- Zoom and pan the map normally

### Custom Image Mode

Users can upload their own image (a floor plan, blueprint, or custom map) using either the header upload button or the sidebar "Custom Image Mode" card. Once an image is loaded, it replaces the map tiles so zones and pins can be placed directly on the custom image. A "Show Map" button returns to the standard map view.

### Zones

Zones are polygon areas drawn on the map or image. Preset zone categories include:

- Assembly Point
- Medical Hub
- Water Station
- Emergency Corridor
- Restricted Zone
- Custom Zone (with a user-selectable color)

To draw a zone, the user selects a category, clicks at least three points on the map to define the polygon, then double-clicks to finish. A modal then prompts for a zone name and optional description before saving. Saved zones appear in the sidebar list and can be deleted individually.

### Pins

Pins are single-point markers. Preset pin types include:

- First Aid
- Water Truck
- Volunteer Desk
- Custom Pin (with a user-selectable color)

Clicking a pin type and then clicking a location on the map opens a modal to name the pin and set its status (Active, Depleted, or Inactive). Saved pins appear in the sidebar list and can be deleted individually.

### Export

The "Export PNG" button uses html2canvas to capture the current map or image view, including all drawn zones and pins, and downloads it as a PNG file named `fieldops-export-<timestamp>.png`.

### Other Interface Details

- A toast notification system provides feedback for actions such as saving, deleting, or export status.
- The Escape key cancels the current drawing action and closes open modals or search results.
- The sidebar displays a running count of active zones and pins, along with the current map zoom level.

## Data Persistence

All zones, pins, and the uploaded image exist only in browser memory for the current session. Refreshing or closing the page discards all data. There is no backend storage of any operational data.

## External Services

The application depends on the following third-party services being reachable from the browser:

- OpenStreetMap tile servers (for map tiles, via Leaflet)
- Nominatim (`nominatim.openstreetmap.org`) for location name search
- Various CDNs for Tailwind CSS, Leaflet, html2canvas, Font Awesome, and Google Fonts

An internet connection is required for the map and search features to function. Custom Image Mode can be used without a network connection once the page and its assets have loaded, since it does not depend on map tiles or search.

## Notes and Limitations

- No authentication or access control is implemented.
- No server-side validation, storage, or API beyond serving the static page.
- The application is intended for single-user, single-session planning rather than multi-user collaboration.
