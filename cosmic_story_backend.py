#!/usr/bin/env python3
"""
🌌 COSMIC STORY - Astral Natal Chart Generator
Backend API using Kerykeion + Flask
"""

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from kerykeion import AstrologicalSubject, ChartDataFactory, ChartDrawer
from kerykeion.aspects import NatalAspectsFactory
from pathlib import Path
import json
import os
import tempfile
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# ═══════════════════════════════════════════════════════════════
# 🪐 PLANETARY DATA & SYMBOLS
# ═══════════════════════════════════════════════════════════════

PLANET_SYMBOLS = {
    "Sun": "☉", "Moon": "☽", "Mercury": "☿", "Venus": "♀", "Mars": "♂",
    "Jupiter": "♃", "Saturn": "♄", "Uranus": "♅", "Neptune": "♆", "Pluto": "♇",
    "Chiron": "⚷", "Lilith": "⚸", "North Node": "☊", "South Node": "☋",
    "Ascendant": "ASC", "Medium Coeli": "MC", "Descendant": "DSC", "Imum Coeli": "IC"
}

ZODIAC_SYMBOLS = {
    "Ari": "♈", "Tau": "♉", "Gem": "♊", "Can": "♋", "Leo": "♌", "Vir": "♍",
    "Lib": "♎", "Sco": "♏", "Sag": "♐", "Cap": "♑", "Aqu": "♒", "Pis": "♓"
}

ZODIAC_ELEMENTS = {
    "Ari": "Fire", "Leo": "Fire", "Sag": "Fire",
    "Tau": "Earth", "Vir": "Earth", "Cap": "Earth",
    "Gem": "Air", "Lib": "Air", "Aqu": "Air",
    "Can": "Water", "Sco": "Water", "Pis": "Water"
}

ZODIAC_MODALITIES = {
    "Ari": "Cardinal", "Can": "Cardinal", "Lib": "Cardinal", "Cap": "Cardinal",
    "Tau": "Fixed", "Leo": "Fixed", "Sco": "Fixed", "Aqu": "Fixed",
    "Gem": "Mutable", "Vir": "Mutable", "Sag": "Mutable", "Pis": "Mutable"
}

ASPECT_SYMBOLS = {
    "conjunction": "☌", "sextile": "⚹", "square": "□", "trine": "△", 
    "opposition": "☍", "quincunx": "⚻", "semisextile": "⚺"
}

# ═══════════════════════════════════════════════════════════════
# 🔮 INTERPRETATION DATABASE
# ═══════════════════════════════════════════════════════════════

PLANET_MEANINGS = {
    "Sun": "Your core identity, ego, and life force. The essence of who you are.",
    "Moon": "Your emotional world, instincts, and subconscious needs.",
    "Mercury": "Your mind, communication style, and how you process information.",
    "Venus": "Your love language, values, aesthetics, and what attracts you.",
    "Mars": "Your drive, ambition, passion, and how you assert yourself.",
    "Jupiter": "Your expansion, luck, wisdom, and areas of growth.",
    "Saturn": "Your discipline, fears, life lessons, and where you build mastery.",
    "Uranus": "Your uniqueness, rebellion, innovation, and sudden changes.",
    "Neptune": "Your dreams, spirituality, illusions, and creative imagination.",
    "Pluto": "Your transformation, power, depth, and evolutionary path.",
    "Chiron": "Your deepest wound and greatest gift — the healer archetype.",
    "Lilith": "Your raw, untamed feminine energy and shadow desires.",
    "North Node": "Your soul's destiny and the path you're meant to walk.",
    "South Node": "Your past life gifts and comfortable patterns to transcend."
}

SIGN_MEANINGS = {
    "Ari": "Bold, pioneering, and fiercely independent. A natural warrior spirit.",
    "Tau": "Sensual, grounded, and deeply loyal. A builder of lasting beauty.",
    "Gem": "Curious, witty, and endlessly versatile. A messenger of ideas.",
    "Can": "Nurturing, intuitive, and emotionally deep. A guardian of the heart.",
    "Leo": "Radiant, creative, and born to lead. A sovereign of self-expression.",
    "Vir": "Analytical, devoted, and precision-driven. A healer through service.",
    "Lib": "Harmonious, diplomatic, and aesthetically refined. A bridge between worlds.",
    "Sco": "Intense, transformative, and magnetically powerful. A phoenix soul.",
    "Sag": "Adventurous, philosophical, and freedom-loving. A seeker of truth.",
    "Cap": "Ambitious, disciplined, and masterfully strategic. A builder of legacy.",
    "Aqu": "Visionary, unconventional, and humanitarian. A rebel with a cause.",
    "Pis": "Empathic, dreamy, and spiritually attuned. A vessel of cosmic love."
}

HOUSE_MEANINGS = {
    1: "Self & Identity — How the world sees you; your physical body and aura.",
    2: "Values & Resources — Your money mindset, possessions, and self-worth.",
    3: "Communication & Mind — Siblings, early education, writing, and local travel.",
    4: "Home & Roots — Your foundation, family, ancestry, and emotional security.",
    5: "Creativity & Pleasure — Romance, children, art, and joyful self-expression.",
    6: "Health & Service — Daily routines, work habits, wellness, and acts of service.",
    7: "Partnerships — Marriage, business contracts, and significant others.",
    8: "Transformation & Intimacy — Shared resources, death/rebirth, and deep bonding.",
    9: "Philosophy & Expansion — Higher education, travel, spirituality, and publishing.",
    10: "Career & Legacy — Public reputation, authority, and life calling.",
    11: "Community & Vision — Friends, groups, social causes, and future dreams.",
    12: "Spirituality & Shadow — The unconscious, hidden enemies, and divine connection."
}

ASPECT_INTERPRETATIONS = {
    "conjunction": "A powerful fusion of energies. These planets work as one force in your psyche.",
    "sextile": "A harmonious opportunity. Natural talents that flow when you take initiative.",
    "square": "A dynamic tension that creates growth through challenge and conscious effort.",
    "trine": "An effortless blessing. Gifts that flow so naturally you may not even notice them.",
    "opposition": "A polarity requiring balance. Integration of seemingly opposite forces within you.",
    "quincunx": "An awkward adjustment needed. Two energies that don't understand each other easily."
}

# ═══════════════════════════════════════════════════════════════
# 🧙 CHART CALCULATION ENGINE
# ═══════════════════════════════════════════════════════════════

def calculate_chart(name, year, month, day, hour, minute, lng, lat, tz_str, 
                     houses_system="P", online=False):
    """Calculate a complete natal chart using Kerykeion."""

    subject = AstrologicalSubject(
        name=name,
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        lng=float(lng),
        lat=float(lat),
        tz_str=tz_str,
        houses_system_identifier=houses_system,
        online=online
    )

    return subject


def extract_planet_data(subject):
    """Extract all planetary positions from Kerykeion subject."""
    planets = []
    planet_names = [
        "sun", "moon", "mercury", "venus", "mars", 
        "jupiter", "saturn", "uranus", "neptune", "pluto",
        "chiron", "mean_lilith", "north_node", "south_node"
    ]

    for pname in planet_names:
        if hasattr(subject, pname):
            p = getattr(subject, pname)
            if p:
                planet_info = {
                    "name": p.get("name", pname.title()),
                    "sign": p.get("sign", ""),
                    "sign_symbol": ZODIAC_SYMBOLS.get(p.get("sign", ""), ""),
                    "position": round(p.get("position", 0), 2),
                    "element": ZODIAC_ELEMENTS.get(p.get("sign", ""), ""),
                    "modality": ZODIAC_MODALITIES.get(p.get("sign", ""), ""),
                    "house": p.get("house", None),
                    "retrograde": p.get("retrograde", False),
                    "symbol": PLANET_SYMBOLS.get(p.get("name", pname.title()), "")
                }
                planets.append(planet_info)

    # Add angles
    angles = [
        ("first_house", "Ascendant"),
        ("tenth_house", "Medium Coeli"),
        ("seventh_house", "Descendant"),
        ("fourth_house", "Imum Coeli")
    ]

    for attr, label in angles:
        if hasattr(subject, attr):
            a = getattr(subject, attr)
            if a:
                planets.append({
                    "name": label,
                    "sign": a.get("sign", ""),
                    "sign_symbol": ZODIAC_SYMBOLS.get(a.get("sign", ""), ""),
                    "position": round(a.get("position", 0), 2),
                    "element": ZODIAC_ELEMENTS.get(a.get("sign", ""), ""),
                    "modality": ZODIAC_MODALITIES.get(a.get("sign", ""), ""),
                    "house": None,
                    "retrograde": False,
                    "symbol": PLANET_SYMBOLS.get(label, ""),
                    "is_angle": True
                })

    return planets


def extract_houses(subject):
    """Extract house cusps."""
    houses = []
    for i in range(1, 13):
        attr = f"{['first', 'second', 'third', 'fourth', 'fifth', 'sixth',
                     'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth'][i-1]}_house"
        if hasattr(subject, attr):
            h = getattr(subject, attr)
            if h:
                houses.append({
                    "house": i,
                    "sign": h.get("sign", ""),
                    "sign_symbol": ZODIAC_SYMBOLS.get(h.get("sign", ""), ""),
                    "position": round(h.get("position", 0), 2),
                    "meaning": HOUSE_MEANINGS.get(i, "")
                })
    return houses


def calculate_aspects(subject):
    """Calculate natal aspects using Kerykeion."""
    aspects_factory = NatalAspectsFactory(subject)
    aspects_data = aspects_factory.get_aspects_list()

    aspects = []
    for aspect in aspects_data:
        aspects.append({
            "p1_name": aspect.get("p1_name", ""),
            "p1_symbol": PLANET_SYMBOLS.get(aspect.get("p1_name", ""), ""),
            "p2_name": aspect.get("p2_name", ""),
            "p2_symbol": PLANET_SYMBOLS.get(aspect.get("p2_name", ""), ""),
            "aspect_type": aspect.get("aspect_type", ""),
            "aspect_symbol": ASPECT_SYMBOLS.get(aspect.get("aspect_type", ""), ""),
            "orbit": round(aspect.get("orbit", 0), 2),
            "is_major": aspect.get("aspect_type", "") in ["conjunction", "sextile", "square", "trine", "opposition"]
        })

    return aspects


def generate_story(subject, planets, houses, aspects):
    """Generate the cosmic narrative interpretation."""

    story = {
        "title": f"The Celestial Blueprint of {subject.name}",
        "subtitle": f"Born under the {planets[0]['sign']} Sun on {subject.year}-{subject.month:02d}-{subject.day:02d}",
        "sections": []
    }

    # ── Section 1: The Trinity ──
    sun = next((p for p in planets if p["name"] == "Sun"), None)
    moon = next((p for p in planets if p["name"] == "Moon"), None)
    asc = next((p for p in planets if p["name"] == "Ascendant"), None)

    trinity_text = f"""
    Your cosmic signature is written in three sacred flames:

    **☉ Sun in {sun['sign']}** — {SIGN_MEANINGS.get(sun['sign'], '')}
    This is your radiant core, the eternal light that fuels your journey.

    **☽ Moon in {moon['sign']}** — {SIGN_MEANINGS.get(moon['sign'], '')}  
    This is your inner ocean, the tides that move your soul.

    **↑ Ascendant in {asc['sign']}** — {SIGN_MEANINGS.get(asc['sign'], '')}
    This is your cosmic mask, the first impression you cast upon the world.

    Together, these three form your **Primal Trinity** — the foundation of your astral identity.
    """

    story["sections"].append({
        "id": "trinity",
        "title": "🔥 The Primal Trinity",
        "content": trinity_text,
        "data": {"sun": sun, "moon": moon, "ascendant": asc}
    })

    # ── Section 2: Elemental Balance ──
    elements = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
    for p in planets:
        if p.get("element"):
            elements[p["element"]] += 1

    dominant = max(elements, key=elements.get)
    weakest = min(elements, key=elements.get)

    elemental_text = f"""
    Your chart reveals an **{dominant}-dominant** constitution with {elements[dominant]} planetary placements.

    | Element | Count | Meaning |
    |---------|-------|---------|
    | 🔥 Fire | {elements['Fire']} | Passion, inspiration, action |
    | 🌍 Earth | {elements['Earth']} | Stability, material world, practicality |
    | 💨 Air | {elements['Air']} | Intellect, communication, social connection |
    | 🌊 Water | {elements['Water']} | Emotion, intuition, psychic depth |

    Your dominant **{dominant}** gives you natural gifts in 
    {"leadership and creative vision" if dominant == "Fire" else 
     "building tangible success and grounded wisdom" if dominant == "Earth" else
     "intellectual mastery and social brilliance" if dominant == "Air" else
     "emotional intelligence and spiritual depth"}.

    Your {weakest} element ({elements[weakest]} placements) calls for conscious cultivation — 
    this is where your soul seeks growth through experience.
    """

    story["sections"].append({
        "id": "elements",
        "title": "⚖️ Elemental Alchemy",
        "content": elemental_text,
        "data": elements
    })

    # ── Section 3: House Kingdoms ──
    house_stories = []
    for planet in planets:
        if planet.get("house") and not planet.get("is_angle"):
            house_stories.append(
                f"**{planet['symbol']} {planet['name']}** dwells in your **{planet['house']}th House** — "
                f"{HOUSE_MEANINGS.get(planet['house'], '')}"
            )

    house_text = "\n\n".join(house_stories[:8])  # Top 8 placements

    story["sections"].append({
        "id": "houses",
        "title": "🏛️ The Twelve Kingdoms",
        "content": f"Your planets have claimed their thrones across the celestial houses:\n\n{house_text}",
        "data": houses
    })

    # ── Section 4: Sacred Aspects ──
    major_aspects = [a for a in aspects if a.get("is_major")]
    aspect_stories = []

    for aspect in major_aspects[:6]:  # Top 6 major aspects
        interp = ASPECT_INTERPRETATIONS.get(aspect["aspect_type"], "A significant cosmic connection.")
        aspect_stories.append(
            f"**{aspect['p1_symbol']} {aspect['p1_name']} {aspect['aspect_symbol']} {aspect['p2_symbol']} {aspect['p2_name']}** "
            f"(orb: {aspect['orbit']}°) — {interp}"
        )

    aspect_text = "\n\n".join(aspect_stories)

    story["sections"].append({
        "id": "aspects",
        "title": "✨ Sacred Geometry",
        "content": f"The angles between your planets weave the sacred geometry of your soul:\n\n{aspect_text}",
        "data": major_aspects
    })

    # ── Section 5: Retrograde Souls ──
    retrogrades = [p for p in planets if p.get("retrograde")]
    if retrogrades:
        retro_text = "\n".join([
            f"**{p['symbol']} {p['name']}** retrograde in {p['sign']} — "
            f"Your {p['name'].lower()} energy turns inward. This is a karmic review lifetime for this archetype."
            for p in retrogrades
        ])

        story["sections"].append({
            "id": "retrogrades",
            "title": "🔄 Karmic Rewind",
            "content": f"These planets move backward through your sky, carrying deep soul memories:\n\n{retro_text}",
            "data": retrogrades
        })

    return story


# ═══════════════════════════════════════════════════════════════
# 🌐 API ROUTES
# ═══════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """Main API endpoint to calculate a natal chart."""
    data = request.json

    try:
        subject = calculate_chart(
            name=data.get('name', 'Seeker'),
            year=int(data['year']),
            month=int(data['month']),
            day=int(data['day']),
            hour=int(data.get('hour', 12)),
            minute=int(data.get('minute', 0)),
            lng=float(data['lng']),
            lat=float(data['lat']),
            tz_str=data['tz_str'],
            houses_system=data.get('houses_system', 'P'),
            online=False
        )

        planets = extract_planet_data(subject)
        houses = extract_houses(subject)
        aspects = calculate_aspects(subject)
        story = generate_story(subject, planets, houses, aspects)

        return jsonify({
            "success": True,
            "data": {
                "subject": {
                    "name": subject.name,
                    "birth_date": f"{subject.year}-{subject.month:02d}-{subject.day:02d}",
                    "birth_time": f"{subject.hour:02d}:{subject.minute:02d}",
                    "coordinates": {"lat": subject.lat, "lng": subject.lng}
                },
                "planets": planets,
                "houses": houses,
                "aspects": aspects,
                "story": story
            }
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/chart-svg', methods=['POST'])
def api_chart_svg():
    """Generate an SVG wheel chart."""
    data = request.json

    try:
        subject = calculate_chart(
            name=data.get('name', 'Seeker'),
            year=int(data['year']),
            month=int(data['month']),
            day=int(data['day']),
            hour=int(data.get('hour', 12)),
            minute=int(data.get('minute', 0)),
            lng=float(data['lng']),
            lat=float(data['lat']),
            tz_str=data['tz_str'],
            houses_system=data.get('houses_system', 'P'),
            online=False
        )

        # Generate SVG using Kerykeion
        chart_data = ChartDataFactory.create_natal_chart_data(subject)
        drawer = ChartDrawer(chart_data=chart_data)

        # Save to temp file and return
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            drawer.save_svg(tmp.name)
            return send_file(tmp.name, mimetype='image/svg+xml')

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/timezones', methods=['GET'])
def api_timezones():
    """Return common timezone options."""
    timezones = [
        "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles",
        "America/Toronto", "America/Vancouver", "America/Mexico_City",
        "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Rome", "Europe/Madrid",
        "Europe/Amsterdam", "Europe/Stockholm", "Europe/Moscow",
        "Asia/Tokyo", "Asia/Shanghai", "Asia/Hong_Kong", "Asia/Singapore",
        "Asia/Seoul", "Asia/Bangkok", "Asia/Dubai", "Asia/Mumbai",
        "Australia/Sydney", "Australia/Melbourne", "Pacific/Auckland",
        "UTC"
    ]
    return jsonify({"timezones": timezones})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
