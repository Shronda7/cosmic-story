🌌 COSMIC STORY — Astral Natal Chart Generator
"The cosmos is within us. We are made of star-stuff." — Carl Sagan
A beautiful, interactive natal chart application built with Kerykeion (Swiss Ephemeris) and a cosmic-themed web interface.
✨ Features
🎡 Interactive Chart Wheel — Canvas-rendered zodiac wheel with planet positions
🔥 Primal Trinity Analysis — Sun, Moon, Ascendant interpretation
⚖️ Elemental Balance — Fire/Earth/Air/Water distribution with animated bars
🪐 Complete Planet Grid — All 10 planets + Chiron, Lilith, Nodes, Angles
✨ Sacred Geometry — Major aspect detection and interpretation
🔄 Karmic Rewind — Retrograde planet analysis
🌟 Cosmic Narrative — AI-style storytelling of your chart
📱 Responsive Design — Works on desktop, tablet, and mobile
🚀 Quick Start
1. Install Dependencies
bash
Copy
pip install flask flask-cors kerykeion
2. Run the Backend
bash
Copy
python cosmic_story_backend.py
The API will start on http://localhost:5000
3. Serve the Frontend
Open index.html in your browser, or use a simple HTTP server:
bash
Copy
# Python 3
python -m http.server 8080

# Then visit http://localhost:8080
Note: The frontend includes a demo mode with mock data so you can explore the UI without the backend running. Set USE_MOCK = false in the JavaScript to connect to the real API.
🔮 API Endpoints
Table
Endpoint	Method	Description
/	GET	Serves the frontend
/api/calculate	POST	Calculate full natal chart + story
/api/chart-svg	POST	Generate SVG wheel chart
/api/timezones	GET	List available timezones
Example API Request
bash
Copy
curl -X POST http://localhost:5000/api/calculate   -H "Content-Type: application/json"   -d '{
    "name": "Alice",
    "year": 1990,
    "month": 6,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "lng": -74.0060,
    "lat": 40.7128,
    "tz_str": "America/New_York"
  }'
🏗️ Architecture
plain
Copy
COSMIC STORY/
├── cosmic_story_backend.py    # Flask API + Kerykeion engine
├── index.html                 # Frontend (HTML/CSS/JS)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
Tech Stack
Backend: Python, Flask, Kerykeion (Swiss Ephemeris)
Frontend: Vanilla HTML5, CSS3, Canvas API
Fonts: Cinzel (headers), Cormorant Garamond (body), Inter (UI)
🌍 Finding Coordinates
Use these free resources to find latitude/longitude:
LatLong.net
Google Maps (right-click → coordinates)
TimeZoneDB for timezone strings
📜 License
Kerykeion is licensed under AGPL-3.0. If you use this in a commercial project, you must:
Open-source your entire application, OR
Purchase a commercial Swiss Ephemeris license from Astrodienst, OR
Use the Swiss Ephemeris directly (free for non-commercial)
The frontend code in this project is provided as-is for educational purposes.
🌟 Future Enhancements
[ ] Synastry (relationship compatibility) charts
[ ] Transit forecasts
[ ] PDF report generation
[ ] Save/load multiple charts
[ ] Location autocomplete with geocoding
[ ] Dark/light theme toggle
[ ] Multi-language support
May the stars guide your path. 🌠
